from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Constants import *
from Draw import draw_circle, draw_end
import numpy as np
import pygame

win_const = []
init_pos_c = []

def shift(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    return e

class Cube():
        x = 0
        y = 0
        size = 2
        def __init__(self, x_, y_, size_):
                self.x = x_
                self.y = y_
                self.size = size_
        def paint(self, color_id):
                if color_id == 0:
                        self.color = (0, 0, 0)
                elif color_id == 1:
                        self.color = (255, 255, 255)
                elif color_id == 2:
                        self.color = (255, 0, 0)
                elif color_id == 3:
                        self.color = (0, 255, 0)
        def vertices(self):
                return(
                    (self.size/2 + self.x, -self.size/2 + self.y),
                    (self.size/2 + self.x, self.size/2 + self.y),
                    (-self.size/2 + self.x, -self.size/2 + self.y),
                    (-self.size/2 + self.x, self.size/2 + self.y)
                    )
        edges = (
            (0,1),
            (0,2),
            (3,1),
            (3,2)
            )
        surfaces = (
                (1,0,2,3)
                )
        color = (0, 225, 255)

        def draw(self):
                vert = self.vertices()
                glColor(self.color)
                glBegin(GL_QUADS)
                for vertex in self.surfaces:
                        glVertex2fv(vert[vertex])
                glEnd()

class Quadcopter:
        x = inf
        y = inf
        prev_data = np.ones(input_l_s)*(-1)
        prev_var = 6
        win = [0]
        moves = []
        init_pos = []
        def __init__(self, world):
                counter = 0
                self.moves = []
                while True:
                        a, b = np.random.randint(0, world_size, size = (2))
                        if not world[a][b] == 1:
                                if counter == 0:
                                    global init_pos_c
                                    if len(init_pos_c) == 0:
                                        self.x = a
                                        self.y = b
                                        self.init_pos = [a, b]
                                        init_pos_c = [a, b]
                                    else:
                                        self.x = init_pos_c[0]
                                        self.y = init_pos_c[1]
                                        self.init_pos = init_pos_c
                                    counter += 1
                                elif counter == 1:
                                    global win_const
                                    if len(win_const) == 0:
                                        if not (a == self.x and b == self.y):
                                                world[a][b] = 2
                                                win_bool = True
                                                win_const = [a, b]
                                                self.win = [a, b]
                                                counter += 1
                                    else:
                                        counter += 1
                                        self.win = win_const
                                    if counter == 2:
                                        break
        def get_aim(self):
                return ((self.win[0] - self.x)**2 + (self.win[1] - self.y)**2)**0.5
        def mission_distance(self, x, y):
                return ((self.win[0] - x)**2 + (self.win[1] - y)**2)**0.5
        def run(self, world, clock, brain, fps, mode = "robot"):
                if mode == "human":
                    if draw_user:
                        draw_circle(self.x, self.y, 1)
                        draw_end()
                elif fps <= 30:
                    if mode == "educatable":
                        draw_circle(self.x, self.y, 1, color = blue)
                    else:
                        draw_circle(self.x, self.y, 1)
                    draw_end()
                if world[self.x][self.y] == 1:
                        return "break", self.moves
                elif world[self.x][self.y] == 2:
                        return "win", self.moves
                mission_distance = [1/(self.x - self.win[0] + 1/inf), 1/(self.y - self.win[1] + 1/inf)]
                sensors = [0, 0, 0, 0]
                sensors[0] = [1/(i - 1 + 1/inf) for i in range(1, min(sight_length + 1, world_size - self.x)) if world[self.x + i][self.y] == 1]
                sensors[1] = [1/(i - 1 + 1/inf) for i in range(1, min(sight_length + 1, self.x + 1)) if world[self.x - i][self.y] == 1]
                sensors[2] = [1/(i - 1 + 1/inf) for i in range(1, min(sight_length + 1, world_size - self.y)) if world[self.x][self.y + i] == 1]
                sensors[3] = [1/(i - 1 + 1/inf) for i in range(1, min(sight_length + 1, self.y + 1)) if world[self.x][self.y - i] == 1]
                for i in range(4):
                        if len(sensors[i]) == 0:
                            if i == 0:
                                sensors[i] = 1/(world_size - self.x - 1 + 1/inf)
                            if i == 1:
                                sensors[i] = 1/(self.x + 1/inf)
                            if i == 2:
                                sensors[i] = 1/(world_size - self.y - 1 + 1/inf)
                            if i == 3:
                                sensors[i] = 1/(self.y + 1/inf)
                        else:
                                sensors[i] = sensors[i][0]
                self.prev_data = shift(self.prev_data, 6)
                arr = np.array(mission_distance + sensors)
                for i in range(6):
                    self.prev_data[i] = arr[i]
                move = [[0, 0, 0, 0]]
                if mode == "human":
                    temp = []
                    for i in range(input_l_s):
                        temp.append(self.prev_data[user_view[i]])
                    print(np.array(temp).reshape(1,input_l_s,1))
                    found = False
                    while not found:
                        for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == 119:
                                            move[0][2] = 1
                                            found = True
                                            break
                                        if event.key == 97:
                                            move[0][1] = 1
                                            found = True
                                            break
                                        if event.key == 115:
                                            move[0][3] = 1
                                            found = True
                                            break
                                        if event.key == 100:
                                            move[0][0] = 1
                                            found = True
                                            break
                else:
                    move = brain[0].predict(self.prev_data.reshape(1,input_l_s,1))
                temp = [0, 0, 0, 0]
                var = np.argmax(move[0])
                temp[var] = 1
                self.moves.append([np.ndarray.tolist(self.prev_data.reshape(1,input_l_s,1))[0], temp])
                if var == 0:
                        if self.prev_var == 1:
                                return "break", self.moves
                        self.x += 1
                        if self.x >= world_size:
                            return "break", self.moves
                elif var == 1:
                        if self.prev_var == 0:
                                return"break", self.moves
                        self.x -= 1
                        if self.x < 0:
                            return "break", self.moves
                elif var == 2:
                        if self.prev_var == 3:
                                return "break", self.moves
                        self.y += 1
                        if self.y >= world_size:
                            return "break", self.moves
                elif var == 3:
                        if self.prev_var == 2:
                                return "break", self.moves
                        self.y -= 1
                        if self.y < 0:
                            return "break", self.moves
                #elif var == 4:
                        #if self.prev_var == 4:
                        #        return 1
                self.prev_var = var
                return 0, self.moves
