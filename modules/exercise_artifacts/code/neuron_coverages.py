import torch


def neuron_coverage(activations, threshold=0):
    """
    Calculate neuron coverage from activations.
    A neuron is "covered" if its activation > threshold.
    
    Args:
        activations: Dict of layer activations {name: tensor}
        threshold: Activation threshold (default 0 for ReLU)
    
    Returns:
        coverage: float (0.0 ~ 1.0)
        details: Dict with per-layer coverage info
    """
    total_neurons = 0
    covered_neurons = 0
    details = {}
    
    for name, act in activations.items():
        flat_act = act.view(act.size(0), -1)  # [batch, num_neurons]
        num_neurons = flat_act.shape[1]
        num_covered = (flat_act > threshold).any(dim=0).sum().item()  # covered if any input activates
        
        details[name] = {'covered': num_covered, 'total': num_neurons}
        total_neurons += num_neurons
        covered_neurons += num_covered
    
    coverage = covered_neurons / total_neurons if total_neurons > 0 else 0.0
    return coverage, details


def top_k_neuron_coverage(activations, k=0.1, per_filter=True):
    """
    Calculate Top-k Neuron Coverage.
    A neuron is "covered" if it is among the top-k most activated neurons 
    for at least one test input.
    
    Args:
        activations: Dict of layer activations {name: tensor}
        k: Ratio of top neurons to consider (0.0 ~ 1.0).
           e.g., k=0.1 means top 10% of neurons.
        per_filter: If True, pick top-k% within each filter (for conv layers).
                    If False, pick top-k% across entire layer.
    
    Returns:
        coverage: float (0.0 ~ 1.0)
        details: Dict with per-layer coverage info
    """
    total_neurons = 0
    covered_neurons = 0
    details = {}
    
    for name, act in activations.items():
        batch_size = act.size(0)
        
        # Check if conv layer (4D: batch, channels, h, w) or fc layer (2D: batch, neurons)
        if act.dim() == 4 and per_filter:
            # Conv layer: pick top-k% per filter
            # Shape: [batch, channels, h, w] -> [batch, channels, h*w]
            num_filters = act.size(1)
            spatial_size = act.size(2) * act.size(3)
            act_per_filter = act.view(batch_size, num_filters, spatial_size)
            
            # Calculate actual k from ratio (at least 1)
            layer_k = max(1, int(k * spatial_size))
            num_neurons = num_filters * spatial_size
            
            # Track covered neurons per filter
            covered_mask = torch.zeros(num_filters, spatial_size, dtype=torch.bool)
            
            # For each filter, find top-k spatial positions
            _, top_indices = act_per_filter.topk(layer_k, dim=2)  # [batch, filters, k]
            
            for b in range(batch_size):
                for f in range(num_filters):
                    covered_mask[f, top_indices[b, f]] = True
            
            num_covered = covered_mask.sum().item()
            details[name] = {
                'covered': num_covered, 
                'total': num_neurons, 
                'k': layer_k,
                'k_ratio': k,
                'filters': num_filters,
                'per_filter': True
            }
        else:
            # FC layer or per_filter=False: flatten and pick top-k% across all
            flat_act = act.view(batch_size, -1)
            num_neurons = flat_act.shape[1]
            
            # Calculate actual k from ratio (at least 1)
            layer_k = max(1, int(k * num_neurons))
            
            _, top_indices = flat_act.topk(layer_k, dim=1)
            
            covered_mask = torch.zeros(num_neurons, dtype=torch.bool)
            for b in range(batch_size):
                covered_mask[top_indices[b]] = True
            
            num_covered = covered_mask.sum().item()
            details[name] = {
                'covered': num_covered, 
                'total': num_neurons, 
                'k': layer_k,
                'k_ratio': k,
                'per_filter': False
            }
        
        total_neurons += num_neurons
        covered_neurons += num_covered
    
    coverage = covered_neurons / total_neurons if total_neurons > 0 else 0.0
    return coverage, details