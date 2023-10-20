from card_type_reader import *
from typing import List, Dict
import pandas as pd
import numpy as np


def get_card_mapping_data(file_path: str)->Dict[str, Dict[str, int]]:
    """
    Reads a Lua script from the specified file and extracts a mapping of card data.

    Args:
        file_path: The path to the Lua script file (default should be 'data\type_mapping\constant.lua').

    Returns:
        Dict[str, Dict[str, int]]: A dictionary containing a mapping of card data [subgroup_name, [name, data]].
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    # Remove Lua comments and parse the Lua script to extract card data mapping
    lines = remove_comments_lua(lines)
    return categorize_strings(lines)

class cards_data():
    def __init__(self, cards_data_path: str = 'data/cards_text/datas.csv',
                       cards_text_path: str = 'data/cards_text/texts.csv',
                       cards_data_mapping_path: str = 'data/type_mapping/constant.lua'):
        self.cards_data = pd.read_csv(cards_data_path, delimiter='|')
        self.cards_text = pd.read_csv(cards_text_path, delimiter='|')
        self.cards_data_mapping = get_card_mapping_data(cards_data_mapping_path)
    
    def get_id_list(self)->np.array:
        return self.cards_data.get('id')

    def read_card(self, card_loc: int)->str:
        data = self.cards_data.iloc[card_loc]
        text = self.cards_text.iloc[card_loc]
        map = self.cards_data_mapping['Types of cards']
        
        return 'in testing'
    
if __name__ == '__main__':
    cd = cards_data()
    cd.read_card(0)