import pygame
import numpy as np
import math
from Generation import generate
from Draw import draw
from Constants import *
from tqdm import tqdm
from NN import populate

##        0 - void
##        1 - obst
##        2 - aim
##        3 - markers

def predict_move(array):
        return np.random.randint(0, 100, 4)/100
        #no prediction yet [x1, x2, x3, x4]

def run(quad, world, clock, brain, fps):
        return quad.run(world, clock, brain, fps)
def game_over():
        pygame.quit()
        quit()

def mainloop():
        clock = pygame.time.Clock()
        #[world, scene, boat, brain, score]
        population = []
        for i in range(n_persons):
                population.append(generate())
        user = generate(mode = "user")
        step_counter = 0
        fps = 0
        while 1:
                step_counter += 1
                for i in range(n_persons):
                        for t in range(inf):
                                if fps <= 30:
                                        draw(population[i]["scene"])
                                else:
                                        fps = inf - 1
                                status = run(population[i]["boat"], population[i]["world"], clock, population[i]["brain"], fps)
                                for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                                pygame.quit()
                                                quit()
                                        if event.type == pygame.KEYUP:
                                                if event.key == 276:
                                                        status = "skip"
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                if event.button == 4:
                                                        fps += 1
                                                elif event.button == 5:
                                                        fps-=1
                                                        fps = min(max(0, fps), 30)
                                clock.tick(1 + fps)
                                if(t == game_time or status):
                                        population[i]["score"] = population[i]["boat"].get_aim()**2
                                        if status == "break" or status == "skip":
                                                population[i]["score"] += 100
                                        break
                for t in range(inf):
                        if fps <= 30:
                                if draw_user:
                                        draw(user["scene"])
                        else:
                                fps = inf - 1
                        status = 0#user_run(user)
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                        #clock.tick(1 + fps)
                        if(t == game_time or status):
                                #user["score"] = user["boat"].get_aim()**2
                                if status == "break":
                                        user["score"] += 10
                                break

                #clock.tick(1 + fps/2)
                print("Step {}: (MAX_FPS = {})".format(step_counter, fps + 1))
                populate(population)
                #print(population[0][3][0].get_weights(population[0][3][1].W))
                for i in range(n_persons):
                        population[i] = {**generate(person = True), **dict.fromkeys(["brain"], population[i]["brain"])}
                user = generate(mode = "user")

mainloop()
