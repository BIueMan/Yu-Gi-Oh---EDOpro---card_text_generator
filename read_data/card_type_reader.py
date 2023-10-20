from typing import List, Dict
from collections import defaultdict

def remove_lua_comments(strings: List[str]) -> List[str]:
    """
    Removes comments from Lua code

    Args:
        strings (List[str]): List of strings representing Lua code.

    Returns:
        List[str]: List of strings with comments removed.
    """
    for idx, line in enumerate(strings):
        strings[idx] = line.split('--')[0]
    
    return strings

def exec_code_and_collect_vars(code: List[str]) -> Dict[str, int]:
    """
    Executes a script and collects variables into a dictionary.

    Args:
        code (List[str]): List of strings representing Lua/python code.

    Returns:
        Dict[str, int]: A dictionary containing variable names as keys and their values as values.
    """
    param_dict = {}
    exec('\n'.join(code[:-2]), globals(), param_dict)
    return param_dict

def achieve_type_by_name(type: Dict[str, int]) -> Dict[str, Dict[str, int]]:
    """
    Achieves the type of a card by name.

    Args:
        type (Dict[str, int]): A dictionary where keys are variable names and values are integers.

    Returns:
        Dict[str, Dict[str, int]]: A nested dictionary where keys are categories and values are sub-dictionaries
        containing variables and their values.
    """
    result = defaultdict(dict)

    for name, value in type.items():
        parts = name.split('_')
        if len(parts) > 1:
            category, subcategory = parts[0], '_'.join(parts[1:])
            result[category][subcategory] = value

    return result