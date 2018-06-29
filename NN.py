from tflearn import *
import tensorflow as tf
from Constants import *
import numpy as np

def neural_network_model(input_size):

    graph = tf.Graph()
    tf.reset_default_graph()
    with graph.as_default():
                   config.init_training_mode()
    hidden_l = []
    input_l = input_data(shape=[input_size, 1], name='input')
    hidden_l.append(fully_connected(input_l, hl, activation='sigmoid'))
    for i in range(hl_n - 1):
                    hidden_l.append(fully_connected(hidden_l[-1], hl, activation='sigmoid'))
    out_l = fully_connected(hidden_l[-1], out, activation='softmax')
    model = DNN(out_l)
    return [model, hidden_l, out_l]
def neural_network_model_educatable(input_size):

    graph = tf.Graph()
    tf.reset_default_graph()
    with graph.as_default():
                   config.init_training_mode()
    hidden_l = []
    input_l = input_data(shape=[input_size, 1], name='input')
    hidden_l.append(fully_connected(input_l, hl, activation='sigmoid'))
    for i in range(hl_n - 1 + 2):
                    hidden_l.append(fully_connected(hidden_l[-1], hl, activation='sigmoid'))
    out_l = fully_connected(hidden_l[-1], out, activation='softmax')
    network = regression(out_l, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = DNN(network)
    return [model, hidden_l, out_l]

def populate(population):
    populate_main(sorted(population, key = lambda x: x["score"], reverse = True))

def pop_merge(new_population):
    for i in range(n_persons):
    #Mutation
        for j in range(hl_n - 1):
            weights = new_population[i]["brain"][0].get_weights(new_population[i]["brain"][1][j].W)
            biases = new_population[i]["brain"][0].get_weights(new_population[i]["brain"][1][j].b)
            w_shape = np.shape(weights)
            b_shape = np.shape(biases)
            new_population[i]["brain"][0].set_weights(new_population[i]["brain"][1][j].W, weights + np.fromiter(((-1)**np.random.randint(0, 2) * mutate_rate*(np.random.random() < mutate_prob) for _ in range(w_shape[0] * w_shape[1])), dtype = 'float').reshape(w_shape))
            new_population[i]["brain"][0].set_weights(new_population[i]["brain"][1][j].b, biases + np.fromiter(((-1)**np.random.randint(0, 2) * mutate_rate*(np.random.random() < mutate_prob) for _ in range(b_shape[0])), dtype = 'float').reshape(b_shape))
        weights = new_population[i]["brain"][0].get_weights(new_population[i]["brain"][2].W)
        biases = new_population[i]["brain"][0].get_weights(new_population[i]["brain"][2].b)
        w_shape = np.shape(weights)
        b_shape = np.shape(biases)
        new_population[i]["brain"][0].set_weights(new_population[i]["brain"][2].W, weights + np.fromiter(((-1)**np.random.randint(0, 2) * mutate_rate*(np.random.random() < mutate_prob) for _ in range(w_shape[0] * w_shape[1])), dtype = 'float').reshape(w_shape))
        new_population[i]["brain"][0].set_weights(new_population[i]["brain"][2].b, biases + np.fromiter(((-1)**np.random.randint(0, 2) * mutate_rate*(np.random.random() < mutate_prob) for _ in range(b_shape[0])), dtype = 'float').reshape(b_shape))
    #Crossing over
    for counter in range(n_persons//2 - 1):
        a = np.random.randint(0, n_persons//4)
        b = np.random.randint(0, n_persons//4)
        while a == b:
            if n_persons == 1:
                break
            b = np.random.randint(0, n_persons//4)
        #Weights
        parent_a = [new_population[a]["brain"][0].get_weights(new_population[a]["brain"][1][j].W) for j in range(hl_n - 1)] + [new_population[a]["brain"][0].get_weights(new_population[a]["brain"][2].W)]
        parent_b = [new_population[b]["brain"][0].get_weights(new_population[b]["brain"][1][j].W) for j in range(hl_n - 1)] + [new_population[b]["brain"][0].get_weights(new_population[b]["brain"][2].W)]
        for j in range(len(parent_a)):
            c = np.random.randint(0, len(parent_a))
            parent_a[j][c:] = parent_b[j][c:]
        for j in range(hl_n - 1):
            new_population[i]["brain"][0].set_weights(new_population[i]["brain"][1][j].W, parent_a[j])
        new_population[i]["brain"][0].set_weights(new_population[i]["brain"][2].W, parent_a[-1])
        #biases
        parent_a = [new_population[a]["brain"][0].get_weights(new_population[a]["brain"][1][j].b) for j in range(hl_n - 1)] + [new_population[a]["brain"][0].get_weights(new_population[a]["brain"][2].b)]
        parent_b = [new_population[b]["brain"][0].get_weights(new_population[b]["brain"][1][j].b) for j in range(hl_n - 1)] + [new_population[b]["brain"][0].get_weights(new_population[b]["brain"][2].b)]
        for j in range(len(parent_a)):
            c = np.random.randint(0, len(parent_a))
            parent_a[j][c:] = parent_b[j][c:]
        for j in range(hl_n - 1):
            new_population[i]["brain"][0].set_weights(new_population[i]["brain"][1][j].b, parent_a[j])
        new_population[i]["brain"][0].set_weights(new_population[i]["brain"][2].b, parent_a[-1])

def populate_main(population):
    new_population = []
    population_buf = np.zeros(n_persons)
    while len(new_population) < n_persons//2:
        for i in range(0, n_persons):
            if not population_buf[i]:
                if 1/(i + 1) >= np.random.randint(0, inf + 1)/inf:
                    if len(new_population) < n_persons//2:
                        new_population.append(population[i])
                        population_buf[i] = 1
    for i in range(len(population)):
        if not population_buf[i]:
            new_population.append(population[i])
    pop_merge(new_population)
