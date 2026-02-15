# modules/exercise_artifacts/code/instrumentation.py
"""
External instrumentation utilities for DNN testing.
Provides activation capture via PyTorch forward hooks without modifying the SuT.

Usage Example:
    from mnist_model import load_trained_model
    from instrumentation import forward_and_capture

    model = load_trained_model("path/to/weights.pt")
    
    with torch.no_grad():
        output, activations = forward_and_capture(model, x, names=['conv1', 'conv2', 'fc1'])
    
    # output: model output tensor
    # activations: OrderedDict {'conv1': tensor, 'conv2': tensor, 'fc1': tensor}
"""

from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn


def forward_and_capture(
    model: nn.Module,
    x: torch.Tensor,
    names: Optional[List[str]] = None,
    layer_types: Optional[tuple] = None,
    to_cpu: bool = True,
) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
    """
    Run forward pass and collect intermediate activations using forward hooks.
    
    Args:
        model: The neural network model (not modified).
        x: Input tensor [B, C, H, W] or [B, features].
        names: List of layer names to capture (from model.named_modules()).
               If None and layer_types is None, captures nothing.
        layer_types: Tuple of nn.Module types to capture (e.g., (nn.Conv2d, nn.Linear)).
                     Ignored if names is provided.
        to_cpu: If True, move activations to CPU to avoid GPU memory growth.
    
    Returns:
        Tuple of (output, activations):
            - output: Model output tensor
            - activations: OrderedDict mapping layer_name -> activation tensor (detached)
    
    Raises:
        ValueError: If a requested name doesn't exist in the model.
    """
    activations = OrderedDict()
    hooks = []
    
    # Build name -> module mapping
    name_to_module = dict(model.named_modules())
    
    # Determine which modules to capture
    if names is not None:
        # Validate requested names
        for name in names:
            if name not in name_to_module:
                raise ValueError(f"Layer '{name}' not found in model. "
                                 f"Available: {list(name_to_module.keys())}")
        target_modules = [(n, name_to_module[n]) for n in names]
    elif layer_types is not None:
        # Capture by type
        target_modules = [(n, m) for n, m in model.named_modules() 
                          if isinstance(m, layer_types) and n]
    else:
        # Default: capture nothing (user must specify)
        target_modules = []
    
    # Create hook function factory
    def make_hook(name: str):
        def hook(module, input, output):
            act = output.detach()
            if to_cpu:
                act = act.cpu()
            activations[name] = act
        return hook
    
    # Register hooks
    for name, module in target_modules:
        h = module.register_forward_hook(make_hook(name))
        hooks.append(h)
    
    try:
        # Run forward pass
        output = model(x)
    finally:
        # Always remove hooks
        for h in hooks:
            h.remove()
    
    return output, activations


def forward_and_capture_relu(
    model: nn.Module,
    x: torch.Tensor,
    to_cpu: bool = True,
) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
    """
    Forward pass for MnistCNN that returns output and post-ReLU activations.
    
    For models using F.relu() in forward(), hooks on Conv2d/Linear capture PRE-relu outputs.
    This function applies ReLU to get POST-relu activation values.
    
    Args:
        model: The MnistCNN model.
        x: Input tensor.
        to_cpu: If True, move activations to CPU.
    
    Returns:
        Tuple of (output, activations):
            - output: Model output [B, 10]
            - activations: OrderedDict {'conv1': tensor, 'conv2': tensor, 'fc1': tensor}
    """
    import torch.nn.functional as F
    
    # Run forward and capture raw layer outputs
    output, raw = forward_and_capture(model, x, names=['conv1', 'conv2', 'fc1'], to_cpu=to_cpu)
    
    # Apply ReLU to get post-activation values
    activations = OrderedDict()
    for name, act in raw.items():
        activations[name] = F.relu(act)
    
    return output, activations
