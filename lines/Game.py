class Game:
    x = None
    y = None
    color = None
    jump = None
    name = None

    def SetJump(self):
        self.jump = 1 - self.jump

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.jump = 0


class Ball(Game):
    def __init__(self, x, y, color):
        Game.__init__(self, x, y, color)
        self.name = 'Ball'


class Next(Game):
    def __init__(self, x, y, color):
        Game.__init__(self, x, y, color)
        self.name = 'Next'


class Empty(Game):
    def __init__(self, x, y, color):
        Game.__init__(self, x, y, color)
        self.name = 'Empty'

