class coordinates:
    def __init__(self, x, y,owner,distance):
        self.x = x
        self.y = y
        self.owner = owner
        self.distance = distance
    def __repr__(self):
        return repr((self.x, self.y, self.owner, self.distance))

    def __eq__(self, other):
        return isinstance(other,coordinates) and self.x == other.x and  self.y == other.x and self.owner == other.owner

    def __hash__(self):
        return hash((self.x, self.y, self.owner, self.distance))