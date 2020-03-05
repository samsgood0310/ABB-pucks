class Puck:
    """
    Puck class

    contains:
    puck number
    puck position
    puck angle
    """

    def __init__(self, nr, pos, ang, height=0):

        try:
            nr = str(nr)
            self.nr = nr
        except ValueError:
            print("Puck number has to be a string")

        try:
            pos = list(pos)
            if len(pos) == 2:
                self.pos = pos
            else:
                raise TypeError
        except TypeError:
            print("Position has to be a list of [x, y]")

        try:
            ang = int(ang)
            self.ang = ang
        except TypeError:
            print("Puck angle has to be an integer")

        try:
            height = int(height)
            self.height = height
        except TypeError:
            print("Puck height has to be an integer")

    def __eq__(self, other):
        if not isinstance(other, Puck):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.nr == other.nr

    def update_puck(self, puckpos, puckang, puckheight):
        try:
            puckpos = list(puckpos)
            if len(puckpos) == 2:
                self.pos = puckpos
            else:
                raise TypeError
        except TypeError:
            print("Position has to be a list of [x, y]")

        try:
            puckang = int(puckang)
            self.ang = puckang
        except TypeError:
            print("Puck angle has to be an integer")

        try:
            puckheight = int(puckheight)
            self.height = puckheight
        except TypeError:
            print("Puck height has to be an integer")

    def set_position(self, puckpos):
        try:
            puckpos = list(puckpos)
            if len(puckpos) == 2:
                self.pos = puckpos
            else:
                raise TypeError
        except TypeError:
            print("Position has to be a list of [x, y]")

    def set_angle(self, puckang):
        try:
            puckang = float(puckang)
            self.ang = puckang
        except TypeError:
            print("Puck angle has to be a number")
        if puckang > 180:
            self.ang -= 360
        elif puckang < -180:
            self.ang += 360

    def set_height(self, puckheight):
        try:
            puckheight = int(puckheight)
            self.height = puckheight
        except TypeError:
            print("Puck height has to be an integer")

    def set_pucknr(self, pucknr):
        try:
            pucknr = int(pucknr)
            self.nr = pucknr
        except TypeError:
            print("Puck number has to be an integer")

    def get_puck(self):
        return self.nr, self.pos, self.ang, self.height

    def get_pucknr(self):
        return self.nr

    def get_puckpos(self):
        return self.pos

    def get_puckang(self):
        return self.ang

    def get_puckheight(self):
        return self.height

    def get_xyz(self):
        return self.pos + [self.height]