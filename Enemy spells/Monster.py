import json
import numpy as np
import re

def get_spells(spell_page):
    dic=spell_page.get('spells')
    if dic==None:
        return []
    spells=[spell.replace('{@spell ', '').replace('}', '') for level in dic.values() for spell in level.get('spells', [])]
    return spells

def get_daily(spell_page):
    dic=spell_page.get('daily')
    if dic==None:
        return []
    daily = []
    for lst in dic.values():
        for item in lst:
            s = item.get('entry') if isinstance(item, dict) else item
            if isinstance(s, str):
                m = re.search(r'\{([^}]*)\}', s)
                daily.append(re.sub(r'^@spell\s+', '', m.group(1)) if m else s)
            else:
                daily.append(item)
    return daily

def get_at_will(spell_page):
    dic=spell_page.get('will')
    if dic==None:
        return []
    wills = []
    for will in dic:
        s = will.get('entry') if isinstance(will, dict) else will
        if isinstance(s, str):
            m = re.search(r'\{([^}]*)\}', s)
            val = m.group(1) if m else s
            val = re.sub(r'^@spell\s+', '', val).strip()
            wills.append(val)
        else:
            wills.append(s)
    return wills

def monster_spells():
    monster_path="./5etools/5etools-src/data/bestiary/"
    monster_index=monster_path+"index.json"

    with open(monster_index, "r") as f:
        monster_index_data = json.load(f)


    monster_index_keys=list(monster_index_data.keys())
    Monster_spells=[]
    for book in monster_index_keys:
        if book=="XPHB" or book=="XMM" or book=="XDMG":
            continue
        book_file=monster_path+monster_index_data[book]
        with open(book_file, "r") as f:
            monster_data = json.load(f)



        # Load book monsters
        book_file=monster_path+monster_index_data[book]
        with open(book_file, "r") as f:
            monster_data = json.load(f)

        for mon in monster_data["monster"]:
            
            temp=mon.get("spellcasting")
            if temp==None:
                continue

            spells=get_spells(temp[0])
            #print(spells)
            at_will=get_at_will(temp[0])
            #print(at_will)
            daily=get_daily(temp[0])
            #print(daily)
            all_items = list(spells + at_will + daily)
            #print(all_items)
            #print("-------")
            #print(all_items)
            Monster_spells.append(all_items)

    return Monster_spells