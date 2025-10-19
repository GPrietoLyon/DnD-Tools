import json
import numpy as np

def get_spell_list_for_class(Class):

    spell_path="./5etools/5etools-src/data/spells/"
    spell_source="./5etools/5etools-src/data/generated/gendata-spell-source-lookup.json"
    spell_index=spell_path+"index.json"


    # Open spell index
    with open(spell_index, "r") as f:
        spell_index_data = json.load(f)
    #open spell source class
    with open(spell_source, "r") as f:
        spell_source_data = json.load(f)

    spell_index_keys=list(spell_index_data.keys())

    # Loop through each book in the spell index
    Spell_info=[]
    for book in spell_index_keys:
        if book=="XPHB" or book=="BMT" or book=="EGW":
            continue
        book_lc = book.lower()
        spell_source_book = spell_source_data[book_lc]


        book_file=spell_path+spell_index_data[book]
        with open(book_file, "r") as f:
            spell_data = json.load(f)
            spell_data=spell_data["spell"]
        

        for spell in spell_data:
            name_source=spell["name"].lower()

            ssb = spell_source_book.get(name_source, {})
            if ssb.get('class', {}).get('PHB', {}).get(Class) is True:
                pass
                
            elif Class in ssb.get('classVariant', {}).get('PHB', {}):
                pass
                
            else:
                continue

            Spell_info.append([spell["name"],spell["level"]])

            # sort by level then by name (case-insensitive)
    Spell_info.sort(key=lambda item: (item[1], item[0].lower()))

    np.save(Class+"_Spell_List.npy", Spell_info)
    return Spell_info