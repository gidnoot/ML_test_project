import NN
from matplotlib import pyplot as plt

class Plot:
    plotting = False
    def __init__(self, nn):
        self.nn: NN = nn
        self.fitness = []
        self.day = []

    def create_plot(self):
        Plot.plotting = False
        x_lst = []
        self.day = [1, 1, 1, 2, 3, 4, 5, 6, 7]
        self.fitness = [3, 3, 3, 4, 5, 6, 7, 8, 9]
        day = 1
        multiple_days = 0
        x = 0
        while (x < len(self.day)):
            if (self.day[x] == day):
                x += 1
                multiple_days += 1
            else:
                width = 1 / multiple_days
                for y in range(multiple_days):
                    if (y == 0):
                        x_lst.append(day)
                    else:
                        x_lst.append(x_lst[-1] + width)
                day += 1
                multiple_days = 0
                plt.plot(x_lst, self.fitness[:len(x_lst)])
        plt.show()


        x_lst = [0]
        width = 1 / (len(self.fitness) / self.nn.day)

        for _ in range(len(self.fitness) - 1):
            x_lst.append(x_lst[-1] + width)
        plt.plot(x_lst, self.fitness)
        plt.show()


def create_all_plots(plot_lst):
    Plot.plotting = False

    print(plot_lst[0].day)
    print(plot_lst[0].fitness)
    for x in range(len(plot_lst)):
        x_lst = []
        day = 1
        multiple_days = 0
        y = 0
        while (y < len(plot_lst[x].day)):
            if (plot_lst[x].day[y] == day):
                y += 1
                multiple_days += 1
            else:
                if (multiple_days != 0):
                    width = 1 / multiple_days
                else:
                    width = 1
                for z in range(multiple_days):
                    if (z == 0):
                        x_lst.append(day)
                    else:
                        x_lst.append(x_lst[-1] + width)
                day += 1
                multiple_days = 0
                plt.plot(x_lst, plot_lst[x].fitness[:len(x_lst)])
    plt.show()


