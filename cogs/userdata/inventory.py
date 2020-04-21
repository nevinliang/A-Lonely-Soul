from random import randint
from random import choice

class Inv:

    ITEMS = ['map', \

            'coins', \

            'woodenchest', 'ironchest', 'goldchest', 'diamondchest', 'firechest', \

            'driftwood', 'granite', 'hardwood', 'polishedgranite', 'cloth', 'leather', \
            'water', 'spring', 'pen', 'meat', 'pebbles', 'plastic', 'paper', \

            'glass', 'obsidian', 'gold', 'iron', 'steel', 'diamond', 'fire', 'ice'\
            
            'woodensword', 'ironsword', 'steelsword', 'goldenhilt', 'diamondsword', 'flamesword']


    def __init__(self):
        self.list = {}


    def print(self):
    	retstr = ""
    	for item in self.list.keys():
    		if self.list[item] > 0:
    			retstr += item + ':' + str(self.list[item]) + '\n'
    	return retstr

    
    def add_inv(self, obj, amt=1):
        if obj not in Inv.ITEMS:
            return False
        elif obj not in self.list.keys():
            self.list[obj] = 1
        else:
            self.list[obj] += amt


    def del_inv(self, obj, amt=1):
        if obj not in Inv.ITEMS:
            return False
        elif obj not in self.list.keys():
            return False
        elif self.list[obj] < amt:
            return False
        else:
            self.list[obj] -= amt
            return True


    def open_chest(self, chest):
        if self.del_inv(chest):
            if chest == 'woodenchest':
                self.add_inv('coins', 400)
                self.add_inv('driftwood', randint(2, 5))
                self.add_inv('hardwood', randint(1, 2))
                return 'You have received some coins, some driftwood, and some hardwood'
            elif chest == 'ironchest':
                self.add_inv('coins', 1000)
                self.add_inv('granite', randint(1, 3))
                self.add_inv('iron', randint(1, 5))
                self.add_inv('pebbles', (10, 20))
                return 'You have received some coins, some driftwood, some iron, and some pebbles'
        else:
            return 'That is either not a real chest or you dont have that.'
            

    def mix(self, objs):
        things = {}
        for term in objs:
            item, amt = term.split()
            print(item, amt)
            if item not in Inv.ITEMS or not amt.isdigit():
                return None
            things[item] = int(amt)

        # woodensword
        if things['driftwood'] == 3 and things['granite'] == 1:
            if not self.del_inv('driftwood', 3) or not self.del_inv('granite', 1):
                return None
            self.add_inv('woodensword', 1)
            return 'woodensword'
        # map
        elif things['paper'] == 2 and things['pen'] == 1:
        	if not self.del_inv('paper', 2) or not self.del_inv('pen', 1):
        		return None
        	self.add_inv('map', 1)
        	return 'map'

        # not a valid recipe
        return None

