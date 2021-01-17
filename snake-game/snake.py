#!/usr/bin/env python3

import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

class Cons:

    BOARD_WIDTH = 600
    BOARD_HEIGHT = 600
    DELAY = 100
    DOT_SIZE = 30
    MAX_RAND_POS = 19

class Board(Canvas):

    def __init__(self):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
            background="black", highlightthickness=0)

        self.initGame()
        self.pack()


    def initGame(self):
        '''initializes game'''

        self.inGame = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.loadImages()
        self.createBoard()
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)

    def loadImages(self):
        '''loads images from the disk'''


        try:
            self.idot = Image.open("30pxdot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("30pxsnakehead.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("30pxapple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)
            # self.image = Image.open("grassbackground.jpg")
            # self.backgroundImage = ImageTk.PhotoImage(self.image)
            # self.create_image(0,0,image = self.backgroundImage,anchor = NW)

        except IOError as e:

            print(e)
            sys.exit(1)


    def createObjects(self):
        '''creates objects on Canvas'''

        self.create_text(48, 12, text="Score: {0}".format(self.score),
                         tag="score", fill="white", font =('Gothic', 15,'bold'))
        self.create_image(self.appleX, self.appleY, image=self.apple,
            anchor=NW, tag="apple")
        self.create_image(60, 60, image=self.head, anchor=NW,  tag="head")
        self.create_image(60 - Cons.DOT_SIZE, 60, image=self.dot, anchor=NW, tag="dot")
        self.create_image(60 - (2*Cons.DOT_SIZE), 60, image=self.dot, anchor=NW, tag="dot")


    def checkAppleCollision(self):
        '''checks if the head of snake collides with apple'''

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        dot = self.find_withtag("dot")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if apple[0] == ovr:
                #print('i')
                self.score += 1
                x, y = self.coords(dot[-1])
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()


    def moveSnake(self):
        '''moves the Snake object'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head

        z = 0
        while z < len(items)-1:

            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1

        self.move(head, self.moveX, self.moveY)


    def checkCollisions(self):
        '''checks for collisions'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False


        if x1 < 0:
            self.inGame = False

        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.inGame = False


    def locateApple(self):
        '''places the apple object on Canvas'''

        apple = self.find_withtag("apple")
        dots = self.find_withtag("dot")

        self.delete(apple[0])
        #TODO: create apple position such that it does not generate on top of the snake

        flag = False

        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE

        self.create_image(self.appleX, self.appleY, anchor=NW,
                          image=self.apple, tag="apple")



    def onKeyPressed(self, e):
        '''controls direction variables with cursor keys'''

        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:

            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:

            self.moveX = Cons.DOT_SIZE
            self.moveY = 0

        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.moveY <= 0:

            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:

            self.moveX = 0
            self.moveY = Cons.DOT_SIZE


    def onTimer(self):
        '''creates a game cycle each timer event'''

        self.drawScore()
        self.checkCollisions()

        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(Cons.DELAY, self.onTimer)
        else:
            self.gameOver()


    def drawScore(self):
        '''draws score'''

        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))


    def gameOver(self):
        '''deletes all objects and draws game over message'''

        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
            text="GAME OVER \nSCORE: {0}".format(self.score), fill="red",font=('Gothic',30,'bold'))

    def createBoard(self):
        color = '#006400'
        for i in range(0,Cons.BOARD_WIDTH,Cons.DOT_SIZE):
            for j in range(0,Cons.BOARD_HEIGHT,Cons.DOT_SIZE):
                self.create_rectangle(i,j,i+30,j+30,fill=color,width=0)
                if color == '#006400':
                    color = '#008000'
                else:
                    color = '#006400'

            if color == '#006400':
                color = '#008000'
            else:
                color = '#006400'

class Snake(Frame):

    def __init__(self):
        super().__init__()

        self.master.title('Snake')
        self.board = Board()
        self.pack()


def main():

    root = Tk()
    nib = Snake()
    root.mainloop()


if __name__ == '__main__':
    main()