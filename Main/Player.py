import Field
from tkinter import *


class Player(Field.Field):
    def __init__(self, column_pos, row_pos, field: Field):
        self.field: Field = field
        self.polygon = None
        self.dir = 'right'
        self.turns = 0
        self.column_pos = column_pos
        self.row_pos = row_pos
        self.prev_column_pos = column_pos
        self.prev_row_pos = row_pos
        self.good_direction = True
        self.moves = 0
        self.coords = []
        self.get_player_coords()
        self.block_inputs = [0, 0, 0, 0, 0, 0]

    def get_player_coords(self):
        offset = 5
        x1 = (self.column_pos) * self.field.block_width + offset
        x2 = (self.column_pos) * self.field.block_width + self.field.block_width
        x3 = x1
        y1 = (self.row_pos) * self.field.block_height + offset
        y2 = (self.row_pos) * self.field.block_height + (self.field.block_height / 2) + (offset / 2)
        y3 = (self.row_pos) * self.field.block_height + self.field.block_height
        self.coords = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3}

    def get_block_inputs(self):
        self.block_inputs[0] = self.field.field_dict[self.column_pos][self.row_pos - 1]['block']
        self.block_inputs[1] = self.field.field_dict[self.column_pos + 1][self.row_pos]['block']
        self.block_inputs[2] = self.field.field_dict[self.column_pos][self.row_pos + 1]['block']
        self.block_inputs[3] = self.field.field_dict[self.column_pos - 1][self.row_pos]['block']
        if (self.dir == 'right'):
            self.block_inputs[4] = 1
            self.block_inputs[5] = 1
        elif (self.dir == 'left'):
            self.block_inputs[4] = -1
            self.block_inputs[5] = -1
        elif (self.dir == 'up'):
            self.block_inputs[4] = 1
            self.block_inputs[5] = -1
        elif (self.dir == 'down'):
            self.block_inputs[4] = -1
            self.block_inputs[5] = 1

    def new_player(self, canvas: Canvas):
        self.polygon = canvas.create_polygon(self.coords['x1'], self.coords['y1'], self.coords['x2'],
                                             self.coords['y2'], self.coords['x3'], self.coords['y3'],
                                             fill='Blue')

    def move_player(self, direction, canvas: Canvas):
        if direction == 'right':
            if (self.dir == 'up' or self.dir == 'down'):
                self.turns += 1
            canvas.move(self.polygon, self.field.block_width, 0)
            if (self.prev_column_pos == self.column_pos + 1):
                self.good_direction = not self.good_direction
            self.prev_column_pos = self.column_pos
            self.column_pos += 1
            self.dir = 'right'
        if direction == 'up':
            if (self.dir == 'right'):
                self.turns += 1
            canvas.move(self.polygon, 0, -self.field.block_height)
            if (self.prev_row_pos == self.row_pos - 1):
                self.good_direction = not self.good_direction
            self.prev_row_pos = self.row_pos
            self.row_pos -= 1
            self.dir = 'up'
        if direction == 'down':
            if (self.dir == 'right'):
                self.turns += 1
            canvas.move(self.polygon, 0, self.field.block_height)
            if (self.prev_row_pos == self.row_pos + 1):
                self.good_direction = not self.good_direction
            self.prev_row_pos = self.row_pos
            self.row_pos += 1
            self.dir = 'down'
        if direction == 'left':
            canvas.move(self.polygon, -self.field.block_width, 0)
            if (self.prev_column_pos == self.column_pos - 1):
                self.good_direction = not self.good_direction
            self.prev_column_pos = self.column_pos
            self.column_pos -= 1
            self.dir = 'left'



