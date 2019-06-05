from tkinter import *
import NN

class InfoScreen():
    def __init__(self, nn, root: Tk, canvas: Canvas):
        self.nn: NN = nn
        self.root: Tk = root
        self.canvas: Canvas = canvas
        self.label_frames = {}
        self.labels = {}
        self.create_player_info()
        self.day = canvas.create_text(200, 50, font="Times 50 bold")

    def create_label_frame(self, frame):
        self.label_frames[frame] = LabelFrame(self.root, width=200, height=self.root.winfo_screenheight(), bg='Grey')
        self.label_frames[frame].pack(side='top')

    def create_label(self, label, frame):
        self.labels[label] = Label(self.label_frames[frame])
        self.labels[label].pack(side='top')

    def create_player_info(self):
        self.create_label_frame('gen')
        self.create_label('gen', 'gen')

        for x in range(len(self.nn.nn_players)):
            self.create_label_frame(f'player{x}')
            self.create_label(f'{x}name', f'player{x}')
            self.create_label(f'{x}fitness', f'player{x}')
            self.create_label(f'{x}swap_b', f'player{x}')

    def update_player_info(self):
        self.labels['gen'].configure(text=f'generation {self.nn.generation}')
        for x in range(len(self.nn.nn_players)):
            self.labels[f'{x}name'].configure(text=f'player {x}')
            self.labels[f'{x}fitness'].configure(text=f'fitness: {self.nn.nn_players[x].fitness}')
            self.labels[f'{x}swap_b'].configure(text=f'swap_b: {self.nn.nn_players[x].swapping_back}')
        self.canvas.itemconfigure(self.day, text=f'day {self.nn.day}')

    def update_info(self, label, text):
        self.labels[label].configure(text=text)

