
def find_dict_keys_with_matching_values(input_dict, target_set):
    """
    Efficiently return dictionary keys whose any value is in the target set.
    
    Args:
        input_dict (dict): Dictionary with set/list values
        target_set (set): Set of target values to match
    
    Returns:
        set: Keys whose values intersect with target_set
    """
    return {key for key, values in input_dict.items() 
            if set(values).intersection(target_set)}