from Tkinter import *
import random
import copy
import tools
import pygame
import pykeyboard


class Player:
    def __init__(self,handler):
        self.handler = tools.Handler(self)
        self.handler=handler
        self.username=raw_input("Please enter your name:")
        self.score=0
    def showUserName(self):
        return self.username
    def showScore(self):
        return self.score
    def updateScore(self):
        self.score=self.score+1
    def renewScore(self):
        self.score=0
    def ChangeUser(self):
        self.username=raw_input("Please enter your name:")

class Food:
    def __init__(self, handler):
        self.x = random.randrange(0,40,1)
        self.y = random.randrange(0,30,1)
        self.handler = handler

    def render(self, canvas):
        assert isinstance(canvas, Canvas)
        canvas.create_oval(self.x * 20, self.y * 20, self.x * 20 + 20, self.y * 20 + 20, fill = "#ee00ff")

class Snake:
    body = [[0,0], [1,0], [2,0],[3,0]]
    length = 4
    direction = "Right"
    def __init__(self, handler):
        self.tail = self.body[0]
        self.handler = handler
        self.player = Player(self.handler)

    #It's note necessary to follow these functions.
    #You can program as you wish
    def move(self):
        if self.direction == "Right":
            head = self.body[-1]
            self.body.append([head[0] + 1, head[1]])
        if self.direction == "Left":
            head = self.body[-1]
            self.body.append([head[0] - 1, head[1]])
        if self.direction == "Up":
            head = self.body[-1]
            self.body.append([head[0], head[1] - 1])
        if self.direction == "Down":
            head = self.body[-1]
            self.body.append([head[0], head[1] + 1])
        self.tail = copy.deepcopy(self.body[0])
        del self.body[0]

    def grow(self):
        self.body.insert(1, copy.deepcopy(self.tail))
        head = self.body[-1]
        head.append(1)
        self.length = self.length+1
        self.player.updateScore()


    def update(self):
        self.move()
        food = self.handler.give_me_food()
        if self.body[-1] == [food.x, food.y]:
            self.handler.give_me_game().generate_new_food()
            self.grow()

    def render(self, canvas):
        assert isinstance(canvas, Canvas)
        for seg in self.body:
            canvas.create_oval(seg[0] * 20, seg[1] * 20, seg[0]*20 + 20, seg[1]*20 + 20, fill = "#33FFAA")

    def change_direction(self, direction):
        self.direction = direction

    def renew(self):
        self.length=4
        self.body = [[0,0], [1,0], [2,0],[3,0]]
        self.direction = "Right"

class Display:
    frame = None
    canvas = None
    ball = None

    def __init__(self):
        username='a'
        socre=0
        self.frame = Tk()
        self.canvas = Canvas(self.frame, width=800, height=600, bg="#545454")
        self.canvas.pack()
        self.handler = tools.Handler(self)
        self.snake = Snake(self.handler)
        self.food = Food(self.handler)
        self.player=Player(self.handler)
        #This allow the frame to capture the keyboard event.
        self.frame.bind("<KeyPress>", self.print_key_info)
        pygame.mixer.init()
        self.eat_sound = pygame.mixer.Sound(file='C:\Python27\eat_effect.wav')
        #to create a state
        self.state = "Menu"

        #AI part
        self.ai = tools.SnakeAi(self.handler)


    def print_key_info(self, event):
        if event.keysym == "Up":
            self.snake.change_direction("Up")

        elif event.keysym == "Down":
            self.snake.change_direction("Down")

        elif event.keysym == "Left":
            self.snake.change_direction("Left")

        elif event.keysym == "Right":
            self.snake.change_direction("Right")
        elif event.keysym == 's':
            self.state = "Game"
        elif event.keysym =='r':
            self.state = "Menu"
        elif event.keysym =='c':
            self.player.ChangeUser()
        else:
            print "Dude, you clicked the wrong buttong"


    def run(self):
        self.canvas.delete(ALL)
        pygame.mixer.pre_init(44100, 16, 2, 1024 * 4)
        pygame.init()
        #Insert the code here:
        if self.state == "Menu":
            self.canvas.delete(ALL)
            self.canvas.create_rectangle(200,450,600,350,fill = "#8b98Ea")
            self.canvas.create_text(400,400,text=self.player.showUserName()+" has the highest score: "+ str(self.player.showScore()))
            self.canvas.create_rectangle(200,350,600,250,fill="#8b98Ea")
            self.canvas.create_text(400,300, text = "snake game, press s to start")
            #self.player.renewScore()
        if self.state =="Game":
            self.update()
            head = self.snake.body[-1]
            for x in range(0, self.snake.length - 1):
                if (head == self.snake.body[x]):
                    self.canvas.delete(ALL)
                    self.canvas.create_rectangle(300, 300, 500, 500, fill="#8b98Ea")
                    self.canvas.create_text(400, 400, text="you are dead, please practice more")
                    self.snake.renew()
                    self.state="Menu"
                    break
            if(head[0]==800)or(head[1]==600):
                self.canvas.delete(ALL)
                self.canvas.create_rectangle(300, 300, 500, 500, fill="#8b98Ea")
                self.canvas.create_text(400, 400, text="you are dead, please practice more")
                self.snake.renew()
                self.state = "Menu"
                print"aaaa"
            if self.snake.body[-1] == [self.food.x, self.food.y]:
                print"Should generate new food!"
            self.render(self.canvas)
            self.ai.analyze()
        #End of inserting
        self.frame.after(30, self.run)

    def update(self):
        self.snake.update()

    def render(self, canvas):
        self.snake.render(canvas)
        self.food.render(canvas)

    def generate_new_food(self):

        self.eat_sound.play()
        self.food = Food(self.handler)



game = Display()
game.run()
game.frame.mainloop()