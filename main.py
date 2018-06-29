import pygame
import numpy as np
import math
from Generation import generate
from Draw import draw
from Constants import *
import os
from tqdm import tqdm
from NN import populate
##        0 - void
##        1 - obst
##        2 - aim
###        3 - markers

def cls():
        os.system('cls' if os.name=='nt' else 'clear')

def run(quad, world, clock, brain, fps, mode = "robot"):
        return quad.run(world, clock, brain, fps, mode)

def game_over():
        pygame.quit()
        quit()

def mainloop():
        f = open('logs.txt', 'w')
        f.write("Logs" + '\n')
        f.close()
        clock = pygame.time.Clock()
        #[world, scene, boat, brain, score]
        population = []
        for i in range(n_persons):
                population.append(generate())
        educatable = generate(mode = "educatable")
        user = generate(mode = "user")
        step_counter = 0
        fps = 0
        training_data = []
        for _ in range(60000):
                step_counter += 1
                wins = 0
                for i in range(n_persons):
                        for t in range(inf):
                                if not draw_all:
                                        fps = inf - 1
                                if fps <= 30:
                                        draw(population[i]["scene"])
                                else:
                                        fps = inf - 1
                                status, moves = run(population[i]["boat"], population[i]["world"], clock, population[i]["brain"], fps)
                                for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                                pygame.quit()
                                                quit()
                                        if event.type == pygame.KEYUP:
                                                if event.key == 276:
                                                        status = "skip"
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                if event.button == 4:
                                                        fps += 10
                                                elif event.button == 5:
                                                        fps-=10
                                                        fps = min(max(0, fps), 30)
                                clock.tick(1 + fps)
                                if(t == game_time or status):
                                        population[i]["score"] = 1/(population[i]['boat'].get_aim() + 1/inf)
                                        if status == "break" or status == "skip":
                                                population[i]["score"] *= 0.1
                                        if status == "win":
                                                for i in moves:
                                                        training_data.append(i)
                                                wins += 1
                                        break
                if user_play:
                        for t in range(inf):
                                if draw_user:
                                        draw(user["scene"])
                                cls()
                                print("Step {}: (MAX_FPS = {}), win rate = {}".format(step_counter, fps + 1, wins))# / n_persons))
                                print("Your Turn.")
                                status, moves = run(user['boat'], user['world'], clock, None, fps, mode = "human")
                                for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                                pygame.quit()
                                                quit()
                                if(t == game_time or status):
                                                user["score"] = 1/(user['boat'].get_aim() + 1/inf)
                                                if status == "break" or status == "skip":
                                                        user["score"] *= 0.1
                                                        print("You Break!")
                                                if status == "win":
                                                        for i in moves:
                                                                training_data.append(i)
                                                        print("You Win!")
                                                print("Finish")
                                                break
                if education_play:
                        for t in range(inf):
                                if not draw:
                                        fps = inf - 1
                                if fps <= 30:
                                        draw(educatable["scene"])
                                else:
                                        fps = inf - 1
                                status, moves = run(educatable["boat"], educatable["world"], clock, educatable["brain"], fps, mode = 'educatable')
                                for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                                pygame.quit()
                                                quit()
                                        if event.type == pygame.KEYUP:
                                                if event.key == 276:
                                                        status = "skip"
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                if event.button == 4:
                                                        fps += 10
                                                elif event.button == 5:
                                                        fps-=10
                                                        fps = min(max(0, fps), 30)
                                clock.tick(1 + fps)
                                if(t == game_time or status):
                                        educatable["score"] = 1/(educatable['boat'].get_aim() + 1/inf)
                                        if status == "break" or status == "skip":
                                                educatable["score"] *= 0.1
                                        if status == "win":
                                                for i in moves:
                                                        training_data.append(i)
                                                wins += 1
                                        break
                        if len(training_data):
                                X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
                                y = [i[1] for i in training_data]
                                np.random.shuffle(training_data)
                                educatable['brain'][0].fit({'input': X}, {'targets': y}, n_epoch=500, show_metric=True, run_id='boat', snapshot_epoch=False, snapshot_step = inf)
                                cls()
                print("Step {}: (MAX_FPS = {}), win rate = {}".format(step_counter, fps + 1, wins))# / n_persons))
                f = open('logs.txt', 'a')
                f.write("Step {}: (MAX_FPS = {}), win rate = {}".format(step_counter, fps + 1, wins))# / n_persons) + '\n')
                f.close()
                populate(population)
                for i in range(n_persons):
                        population[i] = {**generate(person = True), **dict.fromkeys(["brain"], population[i]["brain"])}
                user = generate(mode = "user")
                educatable = {**generate(mode = "user"), **dict.fromkeys(["brain"], educatable["brain"])}

mainloop()
