import math
from OpenGL.GL import *
from OpenGL.GLU import *
from Constants import *
import pygame

def draw(scene):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in scene:
                cube.draw()

def draw_circle(x, y, size, color = (255, 255, 0)):
        glColor(color)
        glBegin(GL_TRIANGLE_FAN)
        for i in range(0, 360, 1):
                glVertex3f(x - (world_size/2) + math.cos(i)*size/2, y  - (world_size/2) + math.sin(i)*size/2, 0)
        glEnd()
def draw_end():
        pygame.display.flip()
