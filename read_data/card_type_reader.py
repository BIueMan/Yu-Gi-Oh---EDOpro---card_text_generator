from typing import List, Dict

def remove_comments_lua(strings: List[str]) -> List[str]:
    """
    Removes comments from Lua code in a list of strings.

    Args:
        strings (List[str]): List of strings representing Lua code.

    Returns:
        List[str]: List of strings with comments removed.
    """
    for idx, line in enumerate(strings):
        split_list = line.split('--')
        strings[idx] = line if not split_list[0].strip() else split_list[0]
    
    return strings

def string_to_dict(strings: List[str], categorize: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Converts a list of string representations of key-value pairs to a dictionary.
    
    Example:
    ```python
    data = [
        "apple = 0x1A",
        "banana = 0x2B"
    ]
    result = string_to_dict(data)
    # result will be {'apple': 26, 'banana': 43}
    ```

    Args:
        strings (List[str]): List of strings with key-value pairs.

    Returns:
        Dict[str, int]: Dictionary with keys and integer values.
    """
    combine_data = {}
    for key in categorize.keys():
        combine_data.update(categorize[key])
        
    result_dict = {}
    
    for line in strings:
        parts = line.split("=")
        if len(parts) == 2:
            name = parts[0].strip()
            value = parts[1].strip()
            try:
                value = int(value,16)
            except:
                splitted = value.split("|")
                value = 0
                for value_name in splitted: value |= {**combine_data, **result_dict}[value_name]
                
            result_dict[name] = value

    return result_dict

def categorize_strings(strings: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Categorizes and converts a list of strings containing Lua code into a nested dictionary.
    
    Example:
    ```python
    lua_code = [
        "-- Fruit data",
        "apple = 0x1A",
        "banana = 0x2B",
        "-- Colors",
        "red = 0xFF0000",
        "green = 0x00FF00"
    ]
    result = categorize_strings(lua_code)
    # result will be {'Fruit data': {'apple': 26, 'banana': 43}, 'Colors': {'red': 16711680, 'green': 65280}}
    ```

    Args:
        strings (List[str]): List of Lua code strings.

    Returns:
        Dict[str, Dict[str, int]]: Nested dictionary with categories and key-value pairs.
    """
    categorize = {}
    current_key = None
    current_lines = []

    for line in strings:
        if line.startswith("--"):
            if current_key:
                categorize[current_key] = string_to_dict(current_lines, categorize)
            current_key = line[2:].strip()
            current_lines = []
        else:
            current_lines.append(line.strip())

    if current_key:
        categorize[current_key] = current_lines

    return categorize