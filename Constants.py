blue = (0, 255, 0)
inf = int(10e8)
display = (600, 600)
world_size = 20
mutate_rate = 10e-3
mutate_const = 20
obstacle_prob = 0.3
n_persons = 0
LR = 10e-3
hl_n = 1
out = 4
game_time = 8*world_size
memory_c = 0
input_l_s = memory_c*6+6
hl = 25#memory_c*6+6
draw_user = True
draw_all = True
sight_length = world_size
user_play = True
education_play = True
mutate_prob = mutate_const/(input_l_s * hl + hl * hl * (hl_n - 1) + hl * out)
import numpy as np
user_view = []
for i in range(input_l_s):
    user_view.append(i)
np.random.shuffle(user_view)

