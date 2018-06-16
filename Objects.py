from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from Constants import *
from Draw import draw_circle, draw_end
import numpy as np

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
        prev_data = np.ones(5*game_time+5)*(-1)
        prev_var = 6
        win = [0]
        init_pos = []
        def __init__(self, world):
                counter = 0
                while True:
                        a, b = np.random.randint(0, world_size, size = (2))
                        if not world[a][b] == 1:
                                if counter == 0:
                                        self.x = a
                                        self.y = b
                                        self.init_pos = [a, b]
                                        counter += 1
                                elif counter == 1:
                                        world[a][b] = 2
                                        self.win = [a, b]
                                        if not (a == self.x and b == self.y):
                                                counter += 1
                                if counter == 2:
                                        break
        def get_aim(self):
                return ((self.win[0] - self.x)**2 + (self.win[1] - self.y)**2)**0.5
        def mission_distance(self, x, y):
                return ((self.win[0] - x)**2 + (self.win[1] - y)**2)**0.5
        def run(self, world, clock, brain, fps):
                if fps <= 30:
                        draw_circle(self.x, self.y, 1)
                        draw_end()
                if world[self.x][self.y] == 1:
                        return "break"
                elif world[self.x][self.y] == 2:
                        return "win"
                mission_distance = [self.mission_distance(self.x, self.y)]
                sensors = [inf, inf, inf, inf]
                sensors[0] = [i for i in range(1, world_size) if world[(self.x + i)%(world_size - 1)][self.y] == 1]
                sensors[1] = [i for i in range(1, world_size) if world[(self.x - i)%(world_size - 1)][self.y] == 1]
                sensors[2] = [i for i in range(1, world_size) if world[self.x][(self.y + i)%(world_size - 1)] == 1]
                sensors[3] = [i for i in range(1, world_size) if world[self.x][(self.y - i)%(world_size - 1)] == 1]
                for i in range(4):
                        if len(sensors[i]) == 0:
                                sensors[i] = inf
                        else:
                                sensors[i] = sensors[i][0]
                self.prev_data = shift(self.prev_data, 5)
                for i in range(5):
                        self.prev_data[i] = np.array(mission_distance + sensors)[i]
                move = brain[0].predict(self.prev_data.reshape(1,input_l_s,1))
                var = np.argmax(move[0])
                if var == 0:
                        #if self.prev_var == 1:
                        #        return 1
                        self.x += 1
                        self.x = self.x%(world_size)
                elif var == 1:
                        #if self.prev_var == 0:
                        #        return 1
                        self.x -= 1
                        self.x = self.x%(world_size)
                elif var == 2:
                        #if self.prev_var == 3:
                        #        return 1
                        self.y += 1
                        self.y = self.y%(world_size)
                elif var == 3:
                        #if self.prev_var == 2:
                        #        return 1
                        self.y -= 1
                        self.y = self.y%(world_size)
                #elif var == 4:
                        #if self.prev_var == 4:
                        #        return 1
                self.prev_var = var
                return 0
