import random
import json
from lib.body import Body
from lib.mutually_exclusive_item import Mutually_Exclusive_Item

def get_inventory():
    bracelet = Mutually_Exclusive_Item("bracelet", ["wrists"])
    watch = Mutually_Exclusive_Item("watch", ["wrists"])
    dress1 = Mutually_Exclusive_Item("longsleeve_blue_dress", ["torso", "legs", "arms"])
    dress2 = Mutually_Exclusive_Item("longsleeve_gray_dress", ["torso", "legs", "arms"])
    short_top = Mutually_Exclusive_Item("short_top", ["torso"])
    long_top = Mutually_Exclusive_Item("long_top", ["torso", "arms"])
    pants = Mutually_Exclusive_Item("pants", ["legs"])
    shorts = Mutually_Exclusive_Item("shorts", ["legs"])
    shoes = Mutually_Exclusive_Item("shoes", ["feet"])
    sandals = Mutually_Exclusive_Item("sandals", ["feet"])
    onesie = Mutually_Exclusive_Item("onesie", ["torso", "legs", "arms", "feet"])

    outfit_inventory = [
        bracelet, watch, dress1, dress2, short_top, 
        long_top, pants, shorts, shoes, sandals, onesie
    ]

    return outfit_inventory

def create_dict_inventory(inventory): 
    dict_inventory = { 
        "head": [], 
        "neck": [], 
        "torso": [], 
        "arms": [], 
        "wrists": [], 
        "hands": [], 
        "legs": [], 
        "feet": [] 
    }
    # For each mutually exclusive body part the item has, add it to that list in the dictionary
    for item in inventory:
        for part in item.exclusives:
            dict_inventory[part].append(item)
    return dict_inventory

def generate_outfit(dict_inventory):
    new_body = Body()
    # For every body part we have items for, try to add an item
    for body_part, items_for_body_part in dict_inventory.items():
        # Only check lists that are non-empty (we have items for that body part)
        if items_for_body_part:
            random.shuffle(items_for_body_part)
            for item in items_for_body_part:
                can_apply = True
                for exclusive in item.exclusives:
                    if getattr(new_body, exclusive) is not None:
                        # Some other item is already there
                        can_apply = False
                        break
                if can_apply:
                    # Set each body part in the exclusives list to this item
                    for exclusive in item.exclusives:
                        setattr(new_body, exclusive, item)
                    # Break so we don't try to apply more than one item to a body part
                    break
    return new_body

if __name__ == '__main__':
    inventory = get_inventory()
    dict_inventory = create_dict_inventory(inventory)
    outfitted_body = generate_outfit(dict_inventory)
    for attr, value in vars(outfitted_body).items():
        if value is not None:
            print(attr, '=', value.name)