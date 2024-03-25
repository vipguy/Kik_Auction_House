import random

def split_id(id_tag):
    try:  
        gen_cat, spec_cat, quality, status = id_tag.split('-')
        return gen_cat, spec_cat, quality, status
    except ValueError:
        return False
    
def is_valid_id(id_tag):
    try:  
        if not id_tag[0] == '#':
            return False
        else:
            gen_cat, spec_cat, quality, status = split_id(id_tag)
            if gen_cat == False:
                return False
            if spec_cat == False:
                return False
            if quality == False:
                return False
            if status == False:
                return False
            else:
                return True
    except ValueError:
        return False

def generate_id(gen_cat= random.randint(1,9), spec_cat = random.randint(1,9), quality = random.randint(1,9), status = random.randint(1,9)):
    id_tag = f"#0{gen_cat}-0{spec_cat}-0{quality}-0{status}"
    return id_tag

def define_id( gen_cat, spec_cat, quality, status):
    gen_cat = gen_cat[1:]
    print(f'gen_cat: {gen_cat}, spec_cat: {spec_cat}, quality: {quality}, status: ({status})')
    if gen_cat == '00' and not spec_cat == '00':
        return f' somthing in your id tag is wrong: #{gen_cat}-{spec_cat}-{quality}-{status}  refer to this list of examples:     #00-00-00-00 correct     #01-01-00-00 correct    #00-01-01-01-01 incorrect     #00-00-01-01-01 incorrect'
    if spec_cat == '00':
        if gen_cat == '00':
            return '''
general categories:    
    01 = Weapons 
    02 = Armor 
    03 = Equipment 
    04 = Accessories 
    05 = Consumables 
    06 = Relics/Artifacts 
    07 = Currency 
    08 = Mounts/Pets 
    09 = Materials/Resources 
    10 = Enchantments 
    11 = Services/Contracts 
    12 = Artwork/Decorative 
'''
        elif gen_cat == '01':
            return '''
weapons:  
    01 = Swords 
    02 = Axes 
    03 = polearms
    04 = Bows 
    05 = Crossbows 
    06 = Wands 
    07 = Staves 
    08 = Maces 
    09 = Daggers 
    10 = Throwing 
    11 = Firearms 
    12 = Whips 
    13 = Chains 
    14 = Claws 
    15 = shields 
'''            

        elif gen_cat == '02':
            return '''
armor:  
    01 = headwear 
    02 = Chestwear 
    03 = Legwear 
    04 = footwear 
    05 = handwear 
    06 = armwear 
    07 = facewear 
    08 = shoulderwear 
    09 = Cloaks 
'''
            
        elif gen_cat == '03':
            return '''
equipment:  
    01 = Tools 
    02 = Instruments 
    03 = Devices 
    04 = Machines 
    05 = Amulets 
    06 = Runes 
'''

        elif gen_cat == '04':
            return '''
accessories:  
    01 = Rings 
    02 = Necklaces 
    03 = Bracelets 
    04 = Earrings 
    05 = Brooches 
    06 = Belts 
    07 = Sashes 
    08 = Pendants 
'''
        elif gen_cat == '05':
            return '''
consumables:  
    01 = Potions 
    02 = Elixirs 
    03 = Food 
    04 = Drinks 
    05 = Herbs 
    06 = Spices 
    07 = Oils 
    08 = Incense 
    09 = Scrolls 
    10 = Books 
'''
        elif gen_cat == '06':
            return '''
relics/artifacts:  
    01 = Artifacts 
    02 = Relics 
    03 = Treasures 
    04 = Antiques 
    05 = Heirlooms 
    
'''
        elif gen_cat == '07':
            return '''
currency:  
    01 = Gold 
    02 = Silver 
    03 = Copper 
    04 = Platinum 
    05 = Electrum  
    07 = Jewels 
    08 = Pearls 
    09 = Diamonds 
    10 = Crystals 
'''
        elif gen_cat == '08':
            return '''
mounts/pets:  
    01 = Horses 
    02 = Dogs 
    03 = Cats 
    04 = Birds 
    05 = Reptiles 
    06 = Insects 
    07 = Fish 
    08 = Mammals 
    09 = Mythical 
    10 = Dragons 
'''
        elif gen_cat == '09':
            return '''
materials/resources:  
    01 = Metals 
    02 = Woods 
    03 = Leathers 
    04 = Fabrics 
    05 = Stones 
    06 = Gems 
    07 = Ores 
    08 = Minerals 
    09 = Plants 
    10 = Essences 
'''
        elif gen_cat == '10':
            return '''
enchanted items:  
    01 = Enchantments 
    02 = Curses 
    03 = Blessings 
    04 = Hexes 
    05 = Charms 
    06 = Jinxes 
    07 = Runes 
    08 = Sigils 
'''
        elif gen_cat == '11':
            return '''
services/contracts:  
    01 = Services 
    02 = Contracts 
    03 = Agreements 
    04 = Deals 
    05 = Pacts 
    06 = Oaths 
    07 = Promises 
    08 = Vows 
    09 = Bonds 
    10 = Arrangements 
''' 
    
    elif quality == '00':
        return '''
quality:  
    01 = All 
    02 = Common 
    03 = Uncommon 
    04 = Rare 
    05 = Epic 
    06 = Legendary
    07 = Mythical 
it is important to note that certain items have a minimum quality level, for example a common, uncommon, or rare artifact is not a thing.
quality levels can also be refered to as teirs. (t1,t2,ETC..) just not in the id tag.
'''
    elif status == '00':
        return '''
status:  
    01 = All
    02 = in aucton 
    03 = in storage 
    04 = destroyed
    05 = out of stock
    im not sure what other statuses there could be, but if you have an idea let me know.
''' 
    else:
        print('end')
        set = [(' end')]
        if quality == '01':
            set.append('quality_All')
        if status == '01':
            set.append('status_All')
        return set
    
# print(define_id('00','00','00','00','00'))