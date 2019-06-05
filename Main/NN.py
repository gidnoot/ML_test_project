import math
import ThoughtProcess, Player


class NN:
    generation = 1
    delay = 0
    pause = False
    def __init__(self, nr_of_players, inputs, neurons1, neurons2, neurons3, outputs, day, prev_gens):
        self.day = day
        self.nr_of_players = nr_of_players
        self.inputs = inputs
        self.neurons1 = neurons1
        self.neurons2 = neurons2
        self.neurons3 = neurons3
        self.outputs = outputs
        self.nn_players = []
        if (prev_gens):
            self.prev_gens = []
        self.prev_data = [{}]  # can be changed to more dict's
        self.revert_prev = 0
        self.fit_list = []
        self.create_thought_processes()
        self.fill_fit_list()
        for x in range(len(self.prev_data)):
            self.fill_prev_data(x, x)

    def create_thought_processes(self):
        for x in range(len(self.prev_gens)):
            self.nn_players.append(self.prev_gens[x])
            self.nn_players[x].player_nr = x
            self.nn_players[x].fitness = 0
        correction = len(self.nn_players)
        for x in range(self.nr_of_players - correction):
            self.nn_players.append(ThoughtProcess.ThoughtProcess(self, x + correction))

    def fill_fit_list(self):
        for x in range(self.nr_of_players):
            self.fit_list.append(self.nn_players[x])

    def fill_prev_data(self, prev_idx, fit_idx):
        fit = self.fit_list
        self.prev_data[prev_idx]['player'] = fit[fit_idx]
        self.prev_data[prev_idx]['fit'] = fit[fit_idx].fitness
        self.prev_data[prev_idx]['w'] = fit[fit_idx].w.copy()
        self.prev_data[prev_idx]['b'] = fit[fit_idx].b.copy()

    def get_act_pl_corr(self, act):
        # skip top players from previous days
        init = True
        corr = 0
        while (init or top_player):
            init = False
            top_player = False
            for x in range(len(self.prev_gens)):
                if (self.prev_gens[x].player_nr == act + corr):
                    corr += 1
                    top_player = True
        return corr

def get_direction(nr_inputs, nr_neurons1, nr_neurons2, nr_neurons3, nr_outputs, x_l, w_l, b_l):
    y_l = []
    a1_l = []
    a2_l = []
    a3_l = []
    for i in range(nr_neurons1):
        temp_append = 0
        for j in range(nr_inputs):
            temp_append += x_l[j] * w_l[j + i * nr_inputs]
        temp_append += b_l[i]
        a1_l.append(sigmoid(temp_append))
    for i in range(nr_neurons2):
        temp_append = 0
        for j in range(nr_neurons1):
            temp_append += a1_l[j] * w_l[j + i * nr_neurons1 + nr_inputs * nr_neurons1]
        temp_append += b_l[i + nr_neurons1]
        a2_l.append(sigmoid(temp_append))
    for i in range(nr_neurons3):
        temp_append = 0
        for j in range(nr_neurons2):
            temp_append += a2_l[j] * w_l[j + i * nr_neurons2 + nr_inputs * nr_neurons1 + nr_neurons1 * nr_neurons2]
        temp_append += b_l[i + nr_neurons1 + nr_neurons2]
        a3_l.append(sigmoid(temp_append))
    for i in range(nr_outputs):
        temp_append = 0
        for j in range(nr_neurons1):
            temp_append += a3_l[j] * w_l[j + i * nr_outputs + nr_inputs * nr_neurons1 + nr_neurons1 * nr_neurons2 +
                                         nr_neurons2 * nr_neurons3]
        temp_append += b_l[i + nr_neurons1 + nr_neurons2 + nr_neurons3]
        y_l.append(sigmoid(temp_append))
    if (y_l[0] == max(y_l[0], y_l[1], y_l[2], y_l[3])):
        return 'up'
    elif (y_l[1] == max(y_l[0], y_l[1], y_l[2], y_l[3])):
        return 'right'
    elif (y_l[2] == max(y_l[0], y_l[1], y_l[2], y_l[3])):
        return 'down'
    elif (y_l[3] == max(y_l[0], y_l[1], y_l[2], y_l[3])):
        return 'left'


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
