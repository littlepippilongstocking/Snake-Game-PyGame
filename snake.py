"""
Dilyana Koleva, August 2022
Snake Game with PyGame
"""

import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, direction_x=1, direction_y=0, colour=(255, 0, 0)):
        self.pos = start
        self.direction_x = 1
        self.direction_y = 0
        self.colour = colour

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.pos = (self.pos[0] + self.direction_x, self.pos[1] + self.direction_y)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.colour, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))

        if eyes:
            centre = distance // 2
            radius = 3
            eye1 = (i * distance + centre - radius, j * distance + 8)
            eye2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), eye1, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, colour, pos):
        self.colour = colour
        self.head = Cube(pos)
        self.body.append(self.head)

        # Direction for x and y
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    # Adding a key (pos of head) and it will be set to the new position
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    # Adding a key (pos of head) and it will be set to the new position
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    # Adding a key (pos of head) and it will be set to the new position
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    # Adding a key (pos of head) and it will be set to the new position
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

        # For each object grab the position and check if in turns list
        for i, cube in enumerate(self.body):
            position = cube.pos[:]
            if position in self.turns:
                turn = self.turns[position]
                # Move snake to appropriate location
                cube.move(turn[0], turn[1])
                # If on last cube, remove turn
                if i == len(self.body) - 1:
                    self.turns.pop(position)
            # Checks if we have reached the edge of the screen
            else:
                # Moving left
                if cube.direction_x == -1 and cube.pos[0] <= 0:
                    # Go to the right side of the screen
                    cube.pos = (cube.rows - 1, cube.pos[1])

                # Moving right
                elif cube.direction_x == 1 and cube.pos[0] >= cube.rows - 1:
                    # Go to the left side of the screen
                    cube.pos = (0, cube.pos[1])

                # Moving down
                elif cube.direction_y == 1 and cube.pos[1] >= cube.rows - 1:
                    # Go to the top of the screen
                    cube.pos = (cube.pos[0], 0)

                # Moving up
                elif cube.direction_y == -1 and cube.pos[1] <= 0:
                    # Go to the bottom of the screen
                    cube.pos = (cube.pos[0], cube.rows - 1)

                else:
                    cube.move(cube.direction_x, cube.direction_y)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


def drawGrid(w, rows, surface):
    size = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size
        y = y + size

        # Draws line during loop
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda x: x.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    height = 500

    rows = 20

    window = pygame.display.set_mode((width, height))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), colour=(0, 255, 0))
    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), colour=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda x: x.pos, s.body[x + 1:])):
                print("Score: ", len(s.body))
                message_box("You lost. Play again.")
                s.reset((10, 10))
                break

        redrawWindow(window)


main()
