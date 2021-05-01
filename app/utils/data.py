from typing import Any, Dict, List, Text, Union


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


def filter_duplicate_dicts_by_key(
    dictionaries: List[Dict], key: Any
) -> List[Dict]:
    """
    Removes duplicate dictionary entries from list.

    Parameters
    ----------
    dictionaries : list of dict
        list of dictionaries
    key : any hashable item
        unique key

    Returns
    -------
    list of dict
        list with removed enries
    """
    unique_keys = []
    dictionaries = [
        (d, unique_keys.append(d[key]))
        for d in dictionaries if d[key] not in unique_keys
    ]
    return [*map(lambda x: x[0], dictionaries)]
