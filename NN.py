from tflearn import *
import tensorflow as tf
from Constants import *
import numpy as np

def neural_network_model(input_size):

    graph = tf.Graph()
    tf.reset_default_graph()
    with graph.as_default():
                   config.init_training_mode()
    input_l = input_data(shape=[input_size, 1], name='input')

    hidden_l1 = fully_connected(input_l, hl1, activation='relu')
    hidden_l2 = fully_connected(hidden_l1, hl2, activation='relu')

    out_l = fully_connected(hidden_l2, out, activation='softmax')
    model = DNN(out_l)

    return [model, hidden_l1, hidden_l2, out_l]

def populate(population):
    populate_main(sorted(population, key = lambda x: x["score"]))

def pop_merge(new_population, population):
    #length = sum(len(new_population[0][j][k]) for j in range(len(new_population[0])) for k in range(len(new_population[0][j])))
    #prob_mutate = 1 - (1 - mutate_prob)**(1/length*100)
    for i in range(n_persons//2):
        for j in range(len(new_population[i])):
            for k in range(len(new_population[i][j])):
                for h in range(len(new_population[i][j][k])):
                    if mutate_prob >= np.random.randint(0, 10e8 + 1)/10e8:
                        new_population[i][j][k][h] += mutate_rate * np.random.randint(-10, 11)/10
            population[i]["brain"][0].set_weights(population[i]["brain"][j + 1].W, np.array(new_population[i][j]))
    for counter in range(n_persons//2):
        a = np.random.randint(0, n_persons//2)
        b = np.random.randint(0, n_persons//2)
        while a == b:
            if n_persons == 1:
                break
            b = np.random.randint(0, n_persons//2)
        parent_a = new_population[a][0] + new_population[a][1] + new_population[a][2]
        parent_b = new_population[b][0] + new_population[b][1] + new_population[b][2]
        c = np.random.randint(0, len(parent_a))
        parent_a[c:] = parent_b[c:]
        new_pop = [parent_a[0:input_l_s:1], parent_a[input_l_s:input_l_s+hl1:1], parent_a[input_l_s+hl1:input_l_s+hl1+hl2:1]]
        population[n_persons//2 + counter]["brain"][0].set_weights(population[n_persons//2 + counter]["brain"][1].W, np.array(new_pop[0]))
        population[n_persons//2 + counter]["brain"][0].set_weights(population[n_persons//2 + counter]["brain"][2].W, np.array(new_pop[1]))
        population[n_persons//2 + counter]["brain"][0].set_weights(population[n_persons//2 + counter]["brain"][3].W, np.array(new_pop[2]))

def populate_main(population):
    new_population = []
    population_buf = np.zeros(20)
    while len(new_population) < n_persons//2:
        for i in range(n_persons - 1, -1, -1):
            if not population_buf[i]:
                if 1/(n_persons - i) >= np.random.randint(0, n_persons_10 + 1)/n_persons_10:
                    if len(new_population) < n_persons//2:
                        new_population.append(population[i])
                        population_buf[i] = 1
    for i in range(len(population)):
        if not population_buf[i]:
            new_population.append(population[i])
    pop_merge([[x["brain"][0].get_weights(x["brain"][i].W).tolist() for i in range(1, len(new_population[0]["brain"]))] for x in new_population], new_population)
