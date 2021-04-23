from typing import Dict, List, Text, Union


def select_dict_keys(
    dictionary: Union[Dict, List[Dict]], keys: List[Text]
) -> Union[Dict, List[Dict]]:
    """
    Returns subset of dictionary.

    Parameters
    ----------
    dictionary : dict or list of dict
        dictionaries to filter keys
    keys : list of str
        keys to select

    Returns
    -------
    dict or list of dict
        dictionaries with subset of keys
    """
    if isinstance(dictionary, list):
        return [*map(lambda d: select_dict_keys(d, keys), dictionary)]
    else:
        return {k: dictionary.get(k) for k in keys}


def rename_dict_keys(
    dictionary: Union[Dict, List[Dict]], keys: Dict
) -> Union[Dict, List[Dict]]:
    """
    Returns subset of dictionary.

    Parameters
    ----------
    dictionary : dict or list of dict
        dictionaries to filter keys
    keys : list of str
        keys to select

    Returns
    -------
    dict or list of dict
        dictionaries with subset of keys
    """
    if isinstance(dictionary, list):
        return [*map(lambda d: rename_dict_keys(d, keys), dictionary)]
    else:
        dictionary = dictionary.copy()
        for old, new in keys.items():
            dictionary[new] = dictionary.pop(old)
        return dictionary
