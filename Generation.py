from OpenGL.GL import *
from OpenGL.GLU import *
from Objects import Cube, Quadcopter
import pygame
from pygame.locals import *
from Constants import *
import numpy as np
from NN import neural_network_model

pygame.init()
display = (600, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(90, (display[0]/display[1]), 0.1, 100)
glTranslatef(0.5, 0.5, -(world_size/2))
pygame.display.set_caption('Maze is running')

def world_generation():
        world = np.zeros((world_size, world_size), dtype = int)
        #30% - obstacle generation
        for i in range(world_size):
                for j in range(world_size):
                        if(np.random.randint(0, 100) < obstacle_prob*100):
                                world[i][j] = 1
        return world
def scene_generation(world, brain = False):
        boat = Quadcopter(world)
        scene = []
        for i in range(0, world_size):
                for j in range(0, world_size):
                        scene.append(Cube(i - (world_size/2), j - (world_size/2), 1))
                        scene[-1].paint(world[i][j])
        if brain:
                return {"world": world,"scene": scene,"boat": boat, "score": inf}
        return {"world": world,"scene": scene,"boat": boat,"brain": init_brain(),"score": inf}

def init_brain():
        return neural_network_model(input_l_s)

def generate(mode = "Neural", person = False):
        if mode == "Neural":
                if person:
                        return scene_generation(world_generation(), brain = True)
                return scene_generation(world_generation())
        elif mode == "user":
                return scene_generation(world_generation(), brain = True)

                
