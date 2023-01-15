
def flatten_dict(dictionary, keystring=''):
    """
    Function to flatten python dictionaries

    Inputs:
    dictionary - dict: 

    Returns:

    """
    if type(dictionary) == dict:
        keystring = keystring + '_' if keystring else keystring
        for k in dictionary:
            yield from flatten_dict(dictionary[k], keystring + str(k))
    else:
        yield keystring, dictionary