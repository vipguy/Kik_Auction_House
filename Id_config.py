def split_id(id_tag):
    try:  
        gen_cat, spec_cat, quality, status, quantity = id_tag.split('-')
        return gen_cat, spec_cat, quality, status, quantity
    except ValueError:
        return False
    
def is_valid_id(id_tag):
    id     

def define_id( gen_cat, spec_cat, quality, status, quantity):
    if gen_cat == '00' and not spec_cat == '00':
        return f' somthing in your id tag is wrong: #{gen_cat}-{spec_cat}-{quality}-{status}-{quantity}\n refer to this list of examples:\n    #00-00-00-00-00 correct\n    #01-01-00-00-00 correct\n   #00-01-01-01-01 incorrect\n    #00-00-01-01-01 incorrect'
    if spec_cat == '00':
        if gen_cat == '00':
            return '''
            'general categories: \n  
                01 = Weapons\n
                02 = Armor\n
                03 = Equipment\n
                04 = Accessories\n
                05 = Consumables\n
                06 = Relics/Artifacts\n
                07 = Currency\n
                08 = Mounts/Pets\n
                09 = Materials/Resources\n
                10 = Enchantments\n
                11 = Services/Contracts\n
                12 = Artwork/Decorative\n'
            '''
        elif gen_cat == '01':
            return '''
            'weapons: \n
                01 = Swords\n
                02 = Axes\n
                03 = Spears\n
                04 = Bows\n
                05 = Crossbows\n
                06 = Wands\n
                07 = Staves\n
                08 = Maces\n
                09 = Daggers\n
                10 = Throwing\n
                11 = Firearms\n
                12 = Whips\n
                13 = Chains\n
                14 = Claws\n
                15 = shields\n
            '''            

        elif gen_cat == '02':
            return '''
            'armor: \n
                01 = headwear\n
                02 = Chestwear\n
                03 = Legwear\n
                04 = footwear\n
                05 = handwear\n
                06 = armwear\n
                07 = facewear\n
                08 = shoulderwear\n
                09 = Cloaks\n
            '''
            
        elif gen_cat == '03':
            return '''
            'equipment: \n
                01 = Tools\n
                02 = Instruments\n
                03 = Devices\n
                04 = Machines\n
                05 = Amulets\n
                06 = Runes\n
            '''

        elif gen_cat == '04':
            return '''
            'accessories: \n
                01 = Rings\n
                02 = Necklaces\n
                03 = Bracelets\n
                04 = Earrings\n
                05 = Brooches\n
                06 = Belts\n
                07 = Sashes\n
                08 = Pendants\n
            '''
        elif gen_cat == '05':
            return '''
            'consumables: \n
                01 = Potions\n
                02 = Elixirs\n
                03 = Food\n
                04 = Drinks\n
                05 = Herbs\n
                06 = Spices\n
                07 = Oils\n
                08 = Incense\n
                09 = Scrolls\n
                10 = Books\n
            '''
        elif gen_cat == '06':
            return '''
            'relics/artifacts: \n
                01 = Artifacts\n
                02 = Relics\n
                03 = Treasures\n
                04 = Antiques\n
                05 = Heirlooms\n
                
            '''
        elif gen_cat == '07':
            return '''
            'currency: \n
                01 = Gold\n
                02 = Silver\n
                03 = Copper\n
                04 = Platinum\n
                05 = Electrum\n
                06 = Gems\n
                07 = Jewels\n
                08 = Pearls\n
                09 = Diamonds\n
                10 = Crystals\n
            '''
        elif gen_cat == '08':
            return '''
            'mounts/pets: \n
                01 = Horses\n
                02 = Dogs\n
                03 = Cats\n
                04 = Birds\n
                05 = Reptiles\n
                06 = Insects\n
                07 = Fish\n
                08 = Mammals\n
                09 = Mythical\n
                10 = Dragons\n
            '''
        elif gen_cat == '09':
            return '''
            'materials/resources: \n
                01 = Metals\n
                02 = Woods\n
                03 = Leathers\n
                04 = Fabrics\n
                05 = Stones\n
                06 = Crystals\n
                07 = Ores\n
                08 = Minerals\n
                09 = Plants\n
                10 = Animals\n
            '''
        elif gen_cat == '10':
            return '''
            'enchanted items: \n
                01 = Enchantments\n
                02 = Curses\n
                03 = Blessings\n
                04 = Hexes\n
                05 = Charms\n
                06 = Jinxes\n
                07 = Runes\n
                08 = Sigils\n
            '''
        elif gen_cat == '11':
            return '''
            'services/contracts: \n
                01 = Services\n
                02 = Contracts\n
                03 = Agreements\n
                04 = Deals\n
                05 = Pacts\n
                06 = Oaths\n
                07 = Promises\n
                08 = Vows\n
                09 = Bonds\n
                10 = Arrangements\n
            ''' 
    
    elif quality == '00':
        return '''
        'quality: \n
            01 = Common\n
            02 = Uncommon\n
            03 = Rare\n
            04 = Epic\n
            05 = Legendary\n
            06 = Mythical\n
            07 = All\n
        it is important to note that certain items have a minimum quality level, for example a common, uncommon, or rare artifact is not a thing.
        quality levels can also be refered to as teirs. (t1,t2,ETC..) just not in the id tag.
        '''
    elif status == '00':
        return '''
        'status: \n
            01 = destroyed\n
            02 = in aucton\n
            03 = in storage\n
            04 = All\n
            im not sure what other statuses there could be, but if you have an idea let me know.
        ''' 
    else:   
        return 'id tag is correct'
    
