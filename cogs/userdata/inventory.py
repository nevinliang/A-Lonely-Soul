from random import randint
from random import choice


class Inv:
    ITEMS = ['map', 'woodenchest', 'ironchest', 'goldchest', 'diamondchest', 'firechest', 'driftwood', 'granite', 'hardwood',
             'polishedgranite', 'cloth', 'leather', 'water', 'spring', 'pen', 'meat', 'pebbles', 'plastic', 'paper', 'glass',
             'obsidian', 'gold', 'iron', 'steel', 'diamond', 'fire', 'ice', 'woodensword', 'ironsword', 'steelsword',
             'goldenhilt', 'diamondsword', 'flamesword', 'book']

    def __init__(self):
        self.list = {}
        self.coins = 0

    def print(self):
        retstr = ""
        for item in self.list.keys():
            if self.list[item] > 0:
                retstr += item + ':' + str(self.list[item]) + '\n'
        if retstr == "":
            retstr = 'What a noob. You have nothing.'
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
                self.coins += 400
                self.add_inv('driftwood', randint(2, 5))
                self.add_inv('cloth', randint(1, 2))
                return 'You have received 400 coins, some driftwood, and some cloth'
            elif chest == 'ironchest':
                self.coins += 1000
                self.add_inv('granite', randint(1, 3))
                self.add_inv('iron', randint(1, 5))
                self.add_inv('pebbles', randint(10, 20))
                return 'You have received 1000 coins, some driftwood, some iron, and some pebbles'
            elif chest == 'goldchest':
                self.coins += 2000
                self.add_inv('gold', randint(2, 4))
                self.add_inv('iron', randint(3, 8))
                self.add_inv('obsidian', randint(1, 2))
                self.add_inv('plastic', randint(5, 15))
                self.add_inv(choice(Inv.ITEMS), 1)
                return 'You have received 2000 coins, some gold, some iron, some obsidian, some uh...plastic? and a mystery item'
            elif chest == 'diamondchest':
                self.coins += 5000
                self.add_inv('diamond', randint(1, 3))
                self.add_inv('ice', randint(2, 6))
                self.add_inv('plastic', randint(20, 30))
                self.add_inv('glass', randint(10, 15))
                self.add_inv('water', randint(10, 20))
                self.add_inv(choice(Inv.ITEMS), 1)
                return 'You have received 5000 coins, some diamond, ice, plastic, glass, water, and a mystery item'
            elif chest == 'firechest':
                self.coins += 10000
                self.add_inv('fire', randint(1, 2))
                self.add_inv('gold', randint(4, 9))
                self.add_inv('iron', randint(10))
                self.add_inv('obsidian', randint(3, 4))
                self.add_inv('hardwood', randint(5, 8))
                return 'You have received 10000 coins, some gold, iron, hardwood, obsidian and ... FIRE'
        else:
            return 'That is either not a real chest or you dont have that.'

    def mix(self, objs):
        things = {}
        for term in objs:
            item, amt = term.split()
            if item not in Inv.ITEMS or not amt.isdigit():
                return None
            things[item] = int(amt)

        def check(a, b):
            return a in things.keys() and b in things.keys()

        if check('driftwood', 'granite') and things['driftwood'] == 3 and things['granite'] == 1:
            return self.mix_help('driftwood', 3, 'granite', 1, 'woodensword', 1)
        elif check('paper', 'pen') and things['paper'] == 1 and things['pen'] == 1:
            return self.mix_help('paper', 1, 'pen', 1, 'map', 1)
        elif check('driftwood', 'pebbles') and things['driftwood'] == 2 and things['pebbles'] == 5:
            return self.mix_help('driftwood', 2, 'pebbles', 5, 'hardwood', 1)

        # not a valid recipe
        return None

    # helper methods
    def mix_help(self, item1, amt1, item2, amt2, sitem, samt):
        if not self.del_inv(item1, amt1) or not self.del_inv(item2, amt2):
            return None
        self.add_inv(sitem, samt)
        return sitem