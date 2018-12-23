from pykeyboard import *
import pygame

class Handler:
    def __init__(self, game):
        self.game = game

    def give_me_game(self):
        return self.game

    def give_me_food(self):
        return self.game.food

    def give_me_snake(self):
        return self.game.snake

    def give_me_player(self):
        return self.game.player

class SnakeAi:

    def __init__(self,handler):
        self.keyboard = PyKeyboard()
        self.handler = handler

    def analyze(self):
        food = self.handler.give_me_food()
        snake = self.handler.give_me_snake()
        head = snake.body[-1]
        if food.y < head[1]:
            self.keyboard.tap_key(self.keyboard.up_key)
        elif food.y > head[1]:
            self.keyboard.tap_key(self.keyboard.down_key)

        elif food.x > head[0]:
            self.keyboard.tap_key(self.keyboard.right_key)

        elif food.x < head[0]:
            self.keyboard.tap_key(self.keyboard.left_key)

    def change_direction(self):
        self.keyboard.tap_key(self.keyboard.down_key)
