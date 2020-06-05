import random

from Game import *


size_field = 540
size_map = 9  # 9
size_cell = size_field / size_map   # 60


class Status:
    init = 0
    wait = 1
    ball_mark = 2
    path_show = 3
    line_strip = 4
    next_balls = 5
    end = 6


class IField:  # интерфейс типа
    Step = None
    Score = None
    Next_balls_mas = []
    Map = []
    Status = None


class FieldClone(IField):  # клон состояния игры
    def __init__(self, clone):
        self.Step = clone.Step
        self.Score = clone.Score
        self.Status = Status.wait
        self.Next_balls_mas = []
        for i in range(0, int(Field.maxnewball)):
            self.Next_balls_mas.append(Next(clone.Next_balls_mas[i].x, clone.Next_balls_mas[i].y,
                                            clone.Next_balls_mas[i].color))
        self.Map = []
        for x in range(0, int(Field.max)):
            self.Map.append([])
            for y in range(0, int(Field.max)):
                if clone.Map[x][y].name == 'Next':
                    self.Map[x].append(Next(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color))
                if clone.Map[x][y].name == 'Empty':
                    self.Map[x].append(Empty(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color))
                if clone.Map[x][y].name == 'Ball':
                    self.Map[x].append(Ball(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color))


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class GameHistory(IField):  # контейнер снимков игры
    History = Stack()


class Field(IField):
    Status = Status.init
    __Field = None
    marked_ball = None
    destin_ball = None
    size_map = size_map
    max = 9
    maxcolor = 9
    maxnewball = 3
    path_step = None
    paths = None
    Next_balls_mas = []
    strips = []
    strip_step = []
    strip = []
    path = []
    Step = None
    Score = None
    Map = []
    Fmap = []

    def SaveState(self):
        return FieldClone(self)

    def RestoreState(self, clone):  # восстанавливаем состояние
        self.Step = clone.Step
        self.Score = clone.Score
        self.Status = clone.Status
        for i in range(0, int(Field.maxnewball)):
            self.Next_balls_mas[i] = Next(clone.Next_balls_mas[i].x, clone.Next_balls_mas[i].y,
                                            clone.Next_balls_mas[i].color)
        for x in range(0, int(Field.max)):
            for y in range(0, int(Field.max)):
                if clone.Map[x][y].name == 'Next':
                    self.Map[x][y] = Next(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color)
                if clone.Map[x][y].name == 'Empty':
                    self.Map[x][y] = Empty(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color)
                if clone.Map[x][y].name == 'Ball':
                    self.Map[x][y] = Ball(clone.Map[x][y].x, clone.Map[x][y].y, clone.Map[x][y].color)

    def __new__(cls):  # синглтон
        if not hasattr(cls, 'instance'):
            cls.instance = super(Field, cls).__new__(cls)
        return cls.instance

    def Places(self):
        self.Step = 0
        self.Status = Status.wait
        self.Map = []
        self.Next_balls_mas = []
        for i in range(0, 49):
            self.path.append(0)
            self.strip.append(0)
        for i in range(0, self.maxnewball):
            self.Next_balls_mas.append(None)
        for i in range(0, int(self.max)):
            self.Map.append([])
            self.Fmap.append([])
            for j in range(0, int(self.max)):
                self.Map[i].append(Empty(i, j, 0))
                self.Fmap[i].append(0)
        self.SelectNextBalls()
        self.ShowNextBalls()
        self.SelectNextBalls()
        self.Score = 0

    def Click(self, x, y):
        x = int(x / size_cell)
        y = int(y / size_cell)
        if self.Map[x][y].name == 'Ball':
            if self.Status == Status.ball_mark:
                X = self.marked_ball.x
                Y = self.marked_ball.y
                self.Map[X][Y] = Ball(self.marked_ball.x, self.marked_ball.y,
                                                                        self.marked_ball.color)
            self.marked_ball = Ball(x, y, self.Map[x][y].color)
            self.Status = Status.ball_mark
        if self.Status == Status.ball_mark:
            self.StepBall(x, y)

    def StepBall(self, x, y):
        if self.Status == Status.ball_mark:
            if self.Map[x][y].name == 'Empty' or self.Map[x][y].name == 'Next':
                if self.Map[x][y].name == 'Empty':
                    self.destin_ball = Empty(x, y, self.Map[x][y].color)
                if self.Map[x][y].name == 'Next':
                    self.destin_ball = Next(x, y, self.Map[x][y].color)
                if self.FindPath():
                    self.Status = Status.path_show

    def SelectNextBalls(self):
        for i in range(0, int(self.maxnewball)):
            self.Next_balls_mas[i] = self.SelectNextBall(random.randint(1, self.maxcolor - 1))

    def SelectNextBall(self, color):
        loap = 200
        next = Next(0, 0, color)
        while loap > 0:
            next.x = random.randint(0, self.max - 1)
            next.y = random.randint(0, self.max - 1)
            if loap == 1:
                next.x = -1
                return next
            if not (self.Map[next.x][next.y].name == "Ball" or self.Map[next.x][next.y].name == "Next"):
                break
            loap -= 1
        self.Map[next.x][next.y] = next
        return next

    def ShowNextBalls(self):
        for i in range(0, int(self.maxnewball)):
            next = Next(self.Next_balls_mas[i].x, self.Next_balls_mas[i].y, self.Next_balls_mas[i].color)
            if next.x < 0:
                break
            if self.Map[next.x][next.y].name == "Ball":
                next = self.SelectNextBall(next.color)
                if next.x < 0:
                    return
            B = Ball(next.x, next.y, next.color)
            self.Map[next.x][next.y] = B
        if self.FindStritLines():
            self.Status = Status.line_strip
        elif self.IsMapFull():
            self.Status = Status.end

    def FindPath(self):
        for i in range(0, int(self.max)):
            for j in range(0, int(self.max)):
                self.Fmap[i][j] = 0
        self.Fmap[self.marked_ball.x][self.marked_ball.y] = 1
        added = True
        found = False
        nr = 1
        while added:
            added = False
            for x in range(0, int(self.max)):
                for y in range(0, int(self.max)):
                    if self.Fmap[x][y] == nr:
                        self.MarkPath(x + 1, y, nr + 1)
                        self.MarkPath(x - 1, y, nr + 1)
                        self.MarkPath(x, y + 1, nr + 1)
                        self.MarkPath(x, y - 1, nr + 1)
                        added = True
            if self.Fmap[self.destin_ball.x][self.destin_ball.y] > 0:
                found = True
                break
            nr += 1
        if not found:
            return False
        px = self.destin_ball.x
        py = self.destin_ball.y
        self.paths = nr
        while nr >= 0:

            B = Empty(px, py, 0)
            if self.Map[px][py].name == "None":
                B = Empty(px, py, 0)
            if self.Map[px][py].name == "Next":
                B = Next(px, py, self.Map[px][py].color)
            self.path[nr] = B
            if self.IsPath(px + 1, py, nr):
                px += 1
            elif self.IsPath(px - 1, py, nr):
                px -= 1
            elif self.IsPath(px, py + 1, nr):
                py += 1
            elif self.IsPath(px, py - 1, nr):
                py -= 1
            nr -= 1
        self.path_step = 0
        return True

    def MarkPath(self, x, y, k):
        if x < 0 or x >= self.max:
            return
        if y < 0 or y >= self.max:
            return
        if self.Map[x][y].name == "Ball":
            return
        if self.Fmap[x][y] > 0:
            return
        self.Fmap[x][y] = k

    def IsPath(self, x, y, k):
        if x < 0 or x >= self.max:
            return False
        if y < 0 or y >= self.max:
            return False
        return self.Fmap[x][y] == k

    def PathShow(self):
        if self.path_step == 0:
            for nr in range(1, self.paths + 1):
                B = Ball(self.path[nr].x, self.path[nr].y, 0)
                self.Map[self.path[nr].x][self.path[nr].y] = B
            self.path_step += 1
            return
        moving_ball = self.path[self.path_step - 1]
        self.Map[moving_ball.x][moving_ball.y] = moving_ball
        moving_ball = self.path[self.path_step]
        self.Map[moving_ball.x][moving_ball.y] = Ball(moving_ball.x, moving_ball.y, self.marked_ball.color)
        self.path_step += 1
        if self.path_step > self.paths:
            N = Empty(self.marked_ball.x, self.marked_ball.y, 0)
            self.Map[self.marked_ball.x][self.marked_ball.y] = N
            B = Ball(self.destin_ball.x, self.destin_ball.y, self.marked_ball.color)
            self.Map[self.destin_ball.x][self.destin_ball.y] = B
            if self.FindStritLines():
                self.Status = Status.line_strip
            else:
                self.Status = Status.next_balls

    def FindStritLines(self):
        self.strips = 0
        for x in range(0, self.max):
            for y in range(0, self.max):
                self.CheckLine(x, y, 1, 0)
                self.CheckLine(x, y, 1, 1)
                self.CheckLine(x, y, 0, 1)
                self.CheckLine(x, y, -1, 1)
        if self.strips == 0:
            return False
        if self.strips > 5:
            self.Score += (self.strips / 5 + 4)
        else:
            self.Score += self.strips
        self.strip_step = 5
        return True

    def CheckLine(self, X, Y, sx, sy):
        p = 5
        if X < 0 or X >= self.max:
            return
        if Y < 0 or Y >= self.max:
            return
        if X + (p - 1) * sx < 0 or X + (p - 1) * sx >= self.max:
            return
        if Y + p * sy < 0 or Y + (p - 1) * sy >= self.max:
            return
        Color = self.Map[X][Y].color
        if Color <= 0:
            return
        if Color == 8:
            for k in range(0, p):
                if self.Map[X + k * sx][Y + k * sy].color != Color and self.Map[X + k * sx][Y + k * sy].color > 0:
                    Color = self.Map[X + k * sx][Y + k * sy].color
                    break
        for k in range(0, p):
            if (self.Map[X + k * sx][Y + k * sy].color != Color and self.Map[X + k * sx][Y + k * sy].color != 8) or \
                    self.Map[X + k * sx][Y + k * sy].name == "Next":
                return
        for k in range(0, p):
            self.strip[self.strips] = Ball(X + k * sx, Y + k * sy, Color)
            self.strips += 1

    def StritLines(self):
        if self.strip_step <= 0:
            for j in range(0, self.strips):
                none = Empty(self.strip[j].x, self.strip[j].y, 0)
                self.Map[self.strip[j].x][self.strip[j].y] = none
            self.Status = Status.wait
            return
        self.strip_step -= 1
        for j in range(0, self.strips):
            if self.strip_step == 3:
                self.Map[self.strip[j].x][self.strip[j].y] = Ball(self.strip[j].x, self.strip[j].y, self.strip[j].color)
                self.Map[self.strip[j].x][self.strip[j].y].SetJump()
            elif self.strip_step == 2:
                self.Map[self.strip[j].x][self.strip[j].y] = Ball(self.strip[j].x, self.strip[j].y, self.strip[j].color)
            elif self.strip_step == 1:
                self.Map[self.strip[j].x][self.strip[j].y] = Next(self.strip[j].x, self.strip[j].y, self.strip[j].color)
            elif self.strip_step == 0:
                self.Map[self.strip[j].x][self.strip[j].y] = Empty(self.strip[j].x, self.strip[j].y,self.strip[j].color)

    def IsMapFull(self):
        for x in range(0, self.max):
            for y in range(0, self.max):
                if self.Map[x][y].name == "Empty" or self.Map[x][y].name == "Next":
                    return False
        return True

    def tick(self):
        if self.Status == Status.init:
            self.Places()
            return
        if self.Status == Status.wait:
            return
        if self.Status == Status.ball_mark:
            return
        if self.Status == Status.path_show:
            self.PathShow()
        if self.Status == Status.line_strip:
            self.StritLines()
            return
        if self.Status == Status.next_balls:
            self.ShowNextBalls()
            self.SelectNextBalls()
            self.Step += 1
        if self.Status == Status.end:
            return
