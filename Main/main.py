from tkinter import *
import time, copy
import Field, Path, Player, ThoughtProcess, NN, InfoScreen, Plot

root = Tk()

canvas = Canvas(root, width=root.winfo_screenwidth() - 200, height=root.winfo_screenheight(), bg='White')
info_frame = Frame(root, width=200, height=root.winfo_screenheight(), bg='Grey')
canvas.pack(side='left')
info_frame.pack(side='right')
field = Field.Field(50, 50, canvas.winfo_screenwidth() - 200, canvas.winfo_screenheight() - 200)

nr_of_players = 3
inputs = 6
neurons1 = 7
neurons2 = 8
neurons3 = 7
outputs = 4
day = 1


def game():
    active = 0
    FRAME_TIME = 1 / 60
    while (True):
        # configuration
        info_screen.update_player_info()
        if (active == nn.prev_data[0]['player'].player_nr):
            canvas.itemconfigure(players[active].polygon, fill='red')
        else:
            canvas.itemconfigure(players[active].polygon, fill='blue')

        # moving player
        players[active].get_block_inputs()
        players[active].move_player(NN.get_direction(inputs, neurons1, neurons2, neurons3, outputs, \
                                                     players[active].block_inputs, nn.nn_players[active].w, \
                                                     nn.nn_players[active].b), canvas)
        players[active].moves += 1

        # fitness + 1 or mutate and go to the next player ('cause player collided)
        if (field.field_dict[players[active].column_pos][players[active].row_pos]['block'] \
                or not players[active].good_direction):
            if (active + nn.get_act_pl_corr(active + 1) >= len(nn.nn_players) - 1):
                ThoughtProcess.mutate_neurons(nn)
                for x in range(len(nn.nn_players)):
                    nn.nn_players[x].fitness = 0
                    canvas.delete(players[x].polygon)
                active = 0
                players.clear()
                for _ in range(1 + nn.get_act_pl_corr(active)):
                    players.append(Player.Player(path.start_column_pos, path.start_row_pos, field))
                active += nn.get_act_pl_corr(active)
                players[active].new_player(canvas)
                NN.NN.generation += 1
            else:
                active += 1
                for _ in range(1 + nn.get_act_pl_corr(active)):
                    players.append(Player.Player(path.start_column_pos, path.start_row_pos, field))
                active += nn.get_act_pl_corr(active)
                players[active].new_player(canvas)
        else:
            nn.nn_players[active].fitness += 1
        nn.nn_players[active].update_fit_list()
        if (active == nn.prev_data[0]['player'].player_nr):
            player_plots[active].fitness.append(nn.nn_players[active].fitness)
            player_plots[active].day.append(nn.day)
        if (Plot.Plot.plotting):
            Plot.create_all_plots(player_plots)

        # save training, reset settings and generate new path when target achieved
        top_player = False
        for x in range(len(nn.prev_gens)):
            if (active == nn.prev_gens[x].player_nr):
                top_player = True
                break
        if (not top_player and players[active].turns >= 2 and nn.day < 3 or
                players[active].column_pos == field.columns - 5):
            nn.prev_gens.append(copy.deepcopy(nn.fit_list[0]))
            nn.day += 1
            for lst in players:
                canvas.delete(lst.polygon)
            for lst in path.blocks:
                canvas.delete(lst)
            nn.__init__(nr_of_players, inputs, neurons1, neurons2, neurons3, outputs, nn.day, False)
            field.__init__(50, 50, canvas.winfo_screenwidth() - 200, canvas.winfo_screenheight() - 200)
            path.__init__(field, canvas)
            active = 0
            players.clear()
            for _ in range(1 + nn.get_act_pl_corr(active)):
                players.append(Player.Player(path.start_column_pos, path.start_row_pos, field))
            active += nn.get_act_pl_corr(active)
            players[active].new_player(canvas)
            NN.NN.generation = 1

        time.sleep(FRAME_TIME + NN.NN.delay)
        while (NN.NN.pause):
            root.update()
        root.update()


def keystrokes():
    root.bind("1", change_speed)
    root.bind("2", change_speed)
    root.bind("3", change_speed)
    root.bind("4", change_speed)
    root.bind("5", change_speed)
    root.bind("<p>", key_plot)


def change_speed(event):
    if (int(event.keysym) != 5):
        NN.NN.delay = (int(event.keysym) - 1) * 0.2
    else:
        NN.NN.pause = not NN.NN.pause


def key_plot(event):
    Plot.Plot.plotting = True


if __name__ == '__main__':
    # creating block path
    path = Path.Path(field, canvas)

    # adding player to path
    players = []
    players.append(Player.Player(path.start_column_pos, path.start_row_pos, field))
    players[0].new_player(canvas)

    nn = NN.NN(nr_of_players, inputs, neurons1, neurons2, neurons3, outputs, day, True)
    info_screen = InfoScreen.InfoScreen(nn, info_frame, canvas)
    player_plots = []
    for _ in nn.nn_players:
        player_plots.append(Plot.Plot(nn))
    keystrokes()

    game()
