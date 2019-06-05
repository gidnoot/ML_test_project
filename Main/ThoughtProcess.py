import random
import NN, InfoScreen


class ThoughtProcess:
    def __init__(self, nn, player_nr):
        self.player_nr = player_nr
        self.nn: NN.NN = nn
        self.swapping_back = False
        self.w = []
        self.b = []
        self.fitness = 0
        self.reset_nn_data()

    def reset_nn_data(self):
        self.w = []
        for _ in range(self.nn.inputs * self.nn.neurons1 + self.nn.neurons1 * self.nn.neurons2
                       + self.nn.neurons2 * self.nn.neurons3 + self.nn.neurons2 * self.nn.outputs):
            self.w.append(random.randint(-4, 4))
        self.b = []
        for _ in range(self.nn.neurons1 + self.nn.neurons2 + self.nn.neurons3 + self.nn.outputs):
            self.b.append(random.randint(-4, 4))

    def update_fit_list(self):
        fit = self.nn.fit_list
        wrong_list = True
        while (wrong_list):
            wrong_list = False
            for x in range(len(fit)):
                if (x != 0 and fit[x].fitness > prev_fit):
                    fit[x - 1], fit[x] = fit[x], fit[x - 1]
                    wrong_list = True
                prev_fit = fit[x].fitness


def mutate_neurons(nn: NN):
    fit = nn.fit_list
    prev = nn.prev_data
    # revert previous mutation if fitness got worse
    for x in range(len(prev)):
        if (prev[x]['player'].fitness < prev[x]['fit'] and nn.revert_prev >= 10):
            prev[x]['player'].w = prev[x]['w'].copy()
            prev[x]['player'].b = prev[x]['b'].copy()
            prev[x]['player'].swapping_back = True
            nn.revert_prev = 0
        else:
            # determine if there's a better player to save in prev_data and to mutate
            for y in range(len(fit)):
                if (fit[y].fitness >= prev[x]['fit']):
                    # just to be sure that we're not switching to another top player
                    top_player = False
                    for z in range(len(prev)):
                        if (fit[y].player_nr == prev[z]['player'].player_nr):
                            top_player = True
                            break
                    for z in range(len(nn.prev_gens)):
                        if (fit[y].player_nr == nn.prev_gens[z].player_nr):
                            top_player = True
                            break
                    if (not top_player):
                        nn.fill_prev_data(x, y)
                        break
                else:
                    break

    # mutate neurons if not reverted
    revert = False
    for x in range(len(prev)):
        if (prev[x]['player'].swapping_back):
            prev[x]['player'].swapping_back = False
            revert = True
    if (not revert):
        nn.revert_prev += 1
        swap_nn_data(fit, prev, nn.prev_gens)
        if (nn.revert_prev > 6):
            change_neurons(prev[x]['player'], 6, 2)

    # reset the three worst players (expect when they're mutated top players)
    for x in range(len(nn.nn_players) - len(nn.prev_gens)):
        top_player = False
        for y in range(len(prev)):
            if (fit[-x - 1].player_nr == prev[y]['player'].player_nr):
                top_player = True
                break
        for y in range(len(nn.prev_gens)):
            if (fit[-x - 1].player_nr == nn.prev_gens[y].player_nr):
                top_player = True
                break
        if (not top_player):
            fit[-x - 1].reset_nn_data()


def swap_nn_data(fit, prev, prev_gens):
    init = True
    while (init or fit[partner].player_nr == prev[0]['player'].player_nr):
        partner = random.randint(1, len(fit) - 1)
        init = False
    top_player = False
    for y in range(len(prev_gens)):
        if (fit[partner].player_nr == prev_gens[y].player_nr):
            top_player = True
            break
    if (not top_player):
        neurons = 20
        bias = 4
    else:
        neurons = random.randint(5, len(prev[0]['player'].w) - 1)
        bias = random.randint(2, 15)
    w = random.randint(0, len(prev[0]['player'].w) - neurons - 1)
    b = random.randint(0, len(prev[0]['player'].b) - bias - 1)
    for x in range(neurons):
        prev[0]['player'].w[w + x] = fit[partner].w[w + x]
    for x in range(bias):
        prev[0]['player'].b[b + x] = fit[partner].b[b + x]


def change_neurons(player, w, b):
    for x in range(w):
        random_w = random.randint(0, len(player.w) - 1)
        plus = random.random() < 0.5
        if (plus and player.w[random_w] < 4):
            player.w[random_w] += 1
        elif (player.w[random_w] > -4):
            player.w[random_w] -= 1
    for x in range(b):
        random_b = random.randint(0, len(player.b) - 1)
        plus = random.random() < 0.5
        if (plus and player.b[random_b] < 4):
            player.b[random_b] += 1
        elif (player.b[random_b] > -4):
            player.b[random_b] -= 1
