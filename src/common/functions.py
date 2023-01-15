from collections.abc import MutableMapping

def flatten_dict(
                d: MutableMapping,
                parent_key: str = '',
                sep: str ='',
                camelCase: bool = True) -> MutableMapping:
    """
    Function to flatten python dictionaries

    Inputs:
    d - dict: dictionary to flatten
    parent_key - str: Key to use for top level of dictionary
    sep - str: Separate to use between levels
    camelCase - bool: Whether to uppercase 1st characters
    of lower-level keys

    Returns:
    flattened_dict - dict: The flattened dictionary
    """

    items = []
    for k, v in d.items():
        # Make keys camelCase - continue example set in response keys
        k_cased = k[0].upper() + k[1:] if camelCase else k
        new_key = parent_key + sep + k_cased if parent_key else k

        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)