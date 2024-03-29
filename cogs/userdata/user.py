from .inventory import Inv


class User:
    DIR_MOVE = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
    USER_LIST = {}

    def __init__(self, id, pos=None, inv=Inv()):
        if pos is None:
            pos = [0, 0]
        User.USER_LIST[id] = self
        self.pos = pos
        self.inv = inv
        self.wait = {}

    # helper methods (other cogs want to add inventory to user)
    def add_inv(self, obj):
        self.inv.add_inv(obj)

    def del_inv(self, obj):
        self.inv.del_inv(obj)

    # actual returning methods
    def move(self, dir):
        [x, y] = self.pos
        x += User.DIR_MOVE[dir][0]
        y += User.DIR_MOVE[dir][1]
        self.pos = [x, y]
        return True

    def getinv(self):
        return self.inv.print()

    def mix(self, objs):
        return self.inv.mix(objs)

    def use(self, obj):
        if obj.endswith('chest'):
            return self.inv.open_chest(obj)
        else:
            return "That isn't a valid item :/"
