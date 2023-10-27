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
            code = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    # Remove Lua comments and parse the Lua script to extract card data mapping
    code = remove_lua_comments(code)
    params = exec_code_and_collect_vars(code)
    return achieve_type_by_name(params)

class cards_data():
    def __init__(self, cards_data_path: str = 'data/cards_text/datas.csv',
                       cards_text_path: str = 'data/cards_text/texts.csv',
                       cards_data_mapping_path: str = 'data/type_mapping/constant.lua',
                       cards_script_path: str = 'data/EDOpro_script/official/'):
        self.cards_data = pd.read_csv(cards_data_path, delimiter='|')
        self.cards_text = pd.read_csv(cards_text_path, delimiter='|')
        self.cards_data_mapping = get_card_mapping_data(cards_data_mapping_path)
        self.cards_script_path = cards_script_path
    
    def get_id_list(self)->np.array:
        return self.cards_data.get('id')

    def read_card(self, card_loc: int)->str:
        data = self.cards_data.iloc[card_loc]
        text = self.cards_text.iloc[card_loc]
        map = self.cards_data_mapping['TYPE']
        
        # get data about the card
        atk = data.get('atk')
        deff = data.get('def')
        level = data.get('level')
        race = data.get('race')
        
        race_map = self.cards_data_mapping['RACE']
        race_list = [key for key in race_map.keys() if race_map[key] & data.get('race')  and key != 'ALL']
        attribute_map = self.cards_data_mapping['ATTRIBUTE']
        attribute_list = [key for key in attribute_map.keys() if attribute_map[key] & data.get('attribute')  and key != 'ALL']
        type_map = self.cards_data_mapping['TYPE']
        types_list = [key for key in type_map.keys() if type_map[key] & data.get('type') and key != 'ALL']
        
        def card_layout() -> str:
            # add card type
            card_layout = ""
            card_layout += "card_name: {}\n".format(text.iloc[1])
            card_layout += "type: [{}]\n".format(', '.join(types_list))
            if 'MONSTER' in types_list:
                card_layout += "race: [{}]\n".format(', '.join(race_list))
                card_layout += "attribute: [{}]\n".format(', '.join(attribute_list))
                card_layout += "level: {}\n".format(level)
                card_layout += "atk: {}\n".format(atk)
                card_layout += "def: {}\n".format(deff)
            card_layout += "\n"
            
            # add main text effects
            card_layout += "card_effect:\n{}\n\n".format(text.iloc[2])
            
            # add subtitle effects
            for i, subtitle in enumerate(text.iloc[3:]):
                if not isinstance(subtitle, str):
                    break
                card_layout += "subtitle_{}:\n{}\n\n".format(i+1, subtitle)
            
            return card_layout
                
        return card_layout()
    
    def get_card_scripe(self, card_id: int) -> str:
        script_location = self.cards_script_path + 'c' + str(card_id) + '.lua'
        try:
            with open(script_location, 'r', encoding='utf-8') as file:
                return '\n'.join(file.read().split('\n')[1:])
        except IOError:
            print("Couldn't open card script {}".format(script_location))
        
    
if __name__ == '__main__':
    cd = cards_data()
    card_layout = cd.read_card(0)
    card_script = cd.get_card_scripe(cd.get_id_list()[0])
    print(card_layout)
    print(card_script)