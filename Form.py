from tkinter import *
from PIL import Image, ImageTk
import Field


class Pictures:
    Empty = Image.open('pictures/empty.png')
    Path = Image.open('pictures/path.png')
    Ball = [[], [], []]

    def __init__(self):
        for i in range(0, 8):
            self.Ball[0].append(Image.open('pictures/' + str(i + 1) + 's.png'))
            self.Ball[1].append(Image.open('pictures/' + str(i + 1) + 'n.png'))
            self.Ball[2].append(Image.open('pictures/' + str(i + 1) + 'b.png'))


def new_game():
    print('new gane')
    app.Map.Places()
    app.game = Field.GameHistory()
    for i in range(0, int(app.Map.max)):
        app.MAP.append([])
        for j in range(0, int(app.Map.max)):
            app.MAP[i].append(app.Map.Map[i][j])

    size = (Field.size_field, Field.size_field)
    app.img = Image.open("pictures/field.png")
    app.img.thumbnail(size)
    render = ImageTk.PhotoImage(app.img)
    app.initil = Label(window, image=render)
    app.initil.place(x=10, y=10)
    app.initil.image = render
    app.initil.bind('<Button-1>', func_img)
    app.Paint()
    for y in range(0, app.Map.max):
        for x in range(0, app.Map.max):
            if app.Map.Map[x][y].name == 'Next':
                app.MAP[x][y] = Field.Next(app.Map.Map[x][y].x, app.Map.Map[x][y].y, app.Map.Map[x][y].color)
            if app.Map.Map[x][y].name == 'Empty':
                app.MAP[x][y] = Field.Empty(app.Map.Map[x][y].x, app.Map.Map[x][y].y, app.Map.Map[x][y].color)
            if app.Map.Map[x][y].name == 'Ball':
                app.MAP[x][y] = Field.Ball(app.Map.Map[x][y].x, app.Map.Map[x][y].y, app.Map.Map[x][y].color)
                app.MAP[x][y].jump = app.Map.Map[x][y].jump
    for y in range(0, app.Map.max):
        for x in range(0, app.Map.max):
            app.Draw(x, y, app.Map.Map[x][y].color, app.Map.Map[x][y].name, app.Map.Map[x][y].jump)


def undo():
    print('undo')
    if app.Status == Field.Status.wait or app.Status == Field.Status.ball_mark:
        if not app.game.History.isEmpty():
            app.Map.RestoreState(app.game.History.pop())
            app.Paint()


def next():
    if not app.Status == Field.Status.end and (app.Status == Field.Status.wait or app.Status == Field.Status.ball_mark):
        print('next')
        app.game.History.push(app.Map.SaveState())
        print('Save state')
        app.Map.Status = Field.Status.next_balls
        app.Paint()


class Main(Frame):
    Map = Field.Field()
    game = Field.GameHistory()
    step = 0
    initil = None
    img = "pictures/field.png"
    Status = None
    MAP = []

    def __init__(self, window):
        super().__init__(window)
        self.p = Pictures()
        self.game = Field.GameHistory()
        self.Map.Places()
        self.init_main()
        self.Paint()
        for y in range(0, self.Map.max):
            for x in range(0, self.Map.max):
                if self.Map.Map[x][y].name == 'Next':
                    self.MAP[x][y] = Field.Next(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                if self.Map.Map[x][y].name == 'Empty':
                    self.MAP[x][y] = Field.Empty(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                if self.Map.Map[x][y].name == 'Ball':
                    self.MAP[x][y] = Field.Ball(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                    self.MAP[x][y].jump = self.Map.Map[x][y].jump
        for y in range(0, self.Map.max):
            for x in range(0, self.Map.max):
                self.Draw(x, y, self.Map.Map[x][y].color, self.Map.Map[x][y].name, self.Map.Map[x][y].jump)
        self.timer_Tick()

    def DrawNext(self, i, c):
        ball = self.p.Ball[1][c - 1].copy()
        size = (50, 50)
        ball.thumbnail(size)
        self.newballimg.paste(ball, (i * 50, 0))
        self.newballimgrender = ImageTk.PhotoImage(self.newballimg)
        self.newball = Label(window, image=self.newballimgrender)
        self.newball.place(x=560, y=420)
        self.newball.image = self.newballimgrender

    def timer_Tick(self):
        if not self.Map.Status == Field.Status.end:
            self.Map.tick()
            if self.Status != Field.Status.wait:
                self.Paint()

            if self.Map.Status == Field.Status.next_balls:
                self.Paint()
                self.Map.Status = Field.Status.wait
                for i in range(0, 3):
                    self.DrawNext(i, self.Map.Next_balls_mas[i].color)
            self.Score.config(text=('Счет: ' + str(int(self.Map.Score))))
            if self.Map.Status == Field.Status.end:
                self.Map.ShowNextBalls()
                self.Paint()

        self.Status = self.Map.Status
        self.after(100, self.timer_Tick)

    def Paint(self):
        for y in range(0, self.Map.max):
            for x in range(0, self.Map.max):
                if self.Map.Status == Field.Status.ball_mark and \
                        self.Map.marked_ball.x == x and self.Map.marked_ball.y == y:
                    self.Map.Map[x][y].SetJump()
                if self.MAP[x][y].jump != self.Map.Map[x][y].jump or self.MAP[x][y].name != self.Map.Map[x][y].name or\
                        self.MAP[x][y].color != self.Map.Map[x][y].color:
                    self.Draw(x, y, self.Map.Map[x][y].color, self.Map.Map[x][y].name, self.Map.Map[x][y].jump)
        for y in range(0, self.Map.max):
            for x in range(0, self.Map.max):
                if self.Map.Map[x][y].name == 'Next':
                    self.MAP[x][y] = Field.Next(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                if self.Map.Map[x][y].name == 'Empty':
                    self.MAP[x][y] = Field.Empty(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                if self.Map.Map[x][y].name == 'Ball':
                    self.MAP[x][y] = Field.Ball(self.Map.Map[x][y].x, self.Map.Map[x][y].y, self.Map.Map[x][y].color)
                    self.MAP[x][y].jump = self.Map.Map[x][y].jump

    def Draw(self, x, y, c, name, j):

        if name == 'Next':
            ball = self.p.Ball[0][c - 1]
        if name == 'Ball':
            if j == -1:
                ball = self.p.Ball[0][c - 1]
            elif j == 1:
                ball = self.p.Ball[2][c - 1]
            elif c == 0:
                ball = self.p.Path
            else:
                ball = self.p.Ball[1][c - 1]
        if name == 'Empty':
            ball = self.p.Empty

        self.img.paste(ball, (x * 60, y * 60))
        self.render = ImageTk.PhotoImage(self.img)
        self.initil = Label(window, image=self.render)
        self.initil.place(x=10, y=10)
        self.initil.image = self.render
        self.initil.bind('<Button-1>', func_img)


    def init_main(self):
        size = (850, 565)
        phon = Image.open("pictures/background.jpg")
        phon.thumbnail(size)
        ren = ImageTk.PhotoImage(phon)
        lable = Label(window, image=ren)
        lable.place(x=-2, y=-2)
        lable.image = ren

        btn_step_back = Button(text='шаг назад', command=undo, bg='#d7d8c0', bd=5, width='8')
        btn_step_back.place(x=560, y=12)

        btn_new_game = Button(text='новая игра', command=new_game, bg='#d7d8c0', bd=5, width='9')
        btn_new_game.place(x=640, y=12)

        btn_step_back = Button(text='Следующие шарики', command=next, bg='#d7d8c0', bd=5, width='20')
        btn_step_back.place(x=560, y=370)

        self.Score = Label(text='Счет: 0')
        self.Score.place(x=560, y=50)

        Text = Label(text='   Цель игры - собрать как можно больше линий из пяти и более шариков одного цвета.\n'
                          '   Нажмите '
                          'на шарик, что бы выбрать его, а затем нажмите на место куда хотите его переместить.\n'
                          '   Радужные  шарики выступают универсальным цветом, который может заменить любой другой в'
                          'ряду.', width='17', height='16', wraplength='160', justify='left', font="Arial 11")
        Text.place(x=560, y=80)

        for i in range(0, int(self.Map.max)):
            self.MAP.append([])
            for j in range(0, int(self.Map.max)):
                self.MAP[i].append(self.Map.Map[i][j])

        size = (Field.size_field, Field.size_field)
        self.img = Image.open("pictures/field.png")
        self.img.thumbnail(size)
        render = ImageTk.PhotoImage(self.img)
        self.initil = Label(window, image=render)
        self.initil.place(x=10, y=10)
        self.initil.image = render

        size = (150, 50)
        self.newballimg = Image.open('pictures/nextball.png')
        self.newballimg.thumbnail(size)
        newballimgrender = ImageTk.PhotoImage(self.newballimg)
        self.newball = Label(window, image=newballimgrender)
        self.newball.place(x=560, y=420)
        self.newball.image = newballimgrender

        for i in range(0, 3):
            self.DrawNext(i, self.Map.Next_balls_mas[i].color)


def func_img(event):
    x = event.x
    y = event.y
    if app.Map.Status == Field.Status.wait or app.Map.Status == Field.Status.ball_mark:
        app.Map.Click(x, y)
    if app.Map.Status == Field.Status.path_show:
        app.game.History.push(app.Map.SaveState())
        print('Save state')


if __name__ == "__main__":
    window = Tk()
    app = Main(window)
    app.pack()
    window.title("Lines")
    window.geometry("730x565")
    window.resizable(False, False)
    window.mainloop()
