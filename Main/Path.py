from tkinter import *
import Field
import random

class Path:
    def __init__(self, field, canvas):
        self.blocks = []
        self.path_list = []
        self.create_path(field, canvas)
        self.start_column_pos = self.path_list[0]['x'] + 1
        self.start_row_pos = self.path_list[0]['y'] + 1

    def create_path(self, field: Field, canvas: Canvas):
        next_direction = 'right'
        row_pos = random.randint(0, field.rows - 3)
        column_pos = 0

        # add start position
        self.path_list.append([])
        direction = 'right_right'
        self.path_list[0] = {'x': column_pos, 'y': row_pos,
                        '1': True, '2': True,  '3': True,
                        '4': True, '5': False, '6': False,
                        '7': True, '8': True,  '9': True}
        column_pos += 3

        # add whole path
        x = 1
        finished = False
        while (not finished):
            self.path_list.append([])
            try_again = True
            while (try_again):
                try_again = False
                if (next_direction == 'right'):
                    multiple_choice = random.randint(1, 3)
                    if (multiple_choice == 1):
                        self.update_list(x, 'right_right', column_pos, row_pos, +3, 0)
                        column_pos += 3
                    elif (multiple_choice == 2 and row_pos >= 6):
                        self.update_list(x, 'right_up', column_pos, row_pos, 0, -3)
                        row_pos -= 3
                        next_direction = 'up'
                    elif (multiple_choice == 3 and row_pos <= field.rows - 6):
                        self.update_list(x, 'right_down', column_pos, row_pos, 0, +3)
                        row_pos += 3
                        next_direction = 'down'
                    else:
                        try_again = True
                elif (next_direction == 'up'):
                    multiple_choice = random.randint(1, 2)
                    if (multiple_choice == 1 and row_pos >= 6):
                        self.update_list(x, 'up_up', column_pos, row_pos, 0, -3)
                        row_pos -= 3
                    elif (multiple_choice == 2):
                        self.update_list(x, 'up_right', column_pos, row_pos, +3, 0)
                        column_pos += 3
                        next_direction = 'right'
                    else:
                        try_again = True
                elif (next_direction == 'down'):
                    multiple_choice = random.randint(1, 2)
                    if (multiple_choice == 1 and row_pos <= field.rows - 6):
                        self.update_list(x, 'down_down', column_pos, row_pos, 0, +3)
                        row_pos += 3
                    elif (multiple_choice == 2):
                        self.update_list(x, 'down_right', column_pos, row_pos, +3, 0)
                        column_pos += 3
                        next_direction = 'right'
                    else:
                        try_again = True
            x += 1
            finished = bool(column_pos > field.columns - 3)

        # create path on canvas
        for block in self.path_list:
            for block_nr in range(1, 10):
                if (block[f'{block_nr}']):
                    offset = 5
                    x1 = (block['x'] + ((block_nr + 2) % 3)) * field.block_width + offset
                    x2 = x1 + field.block_width - offset
                    y1 = (block['y'] + int((block_nr - 0.1) / 3)) * field.block_height + offset
                    y2 = y1 + field.block_height - offset
                    self.blocks.append(canvas.create_rectangle(x1, y1, x2, y2, fill='black'))
                    field.field_dict[(block['x'] + ((block_nr + 2) % 3))][(block['y'] +
                                                                           int((block_nr - 0.1) / 3))]['block'] = 1


    # adds a block of 9 smaller blocks to the list
    def update_list(self, x, dir, c_pos, r_pos, c_add, r_add):
        pl = self.path_list
        if (dir == 'right_right'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': True, '3': True,
                     '4': False, '5': False, '6': False,
                     '7': True, '8': True, '9': True}
        elif (dir == 'up_up' or dir == 'down_down'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': False, '3': True,
                     '4': True, '5': False, '6': True,
                     '7': True, '8': False, '9': True}
        elif (dir == 'right_up'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': False, '3': True,
                     '4': False, '5': False, '6': True,
                     '7': True, '8': True, '9': True}
        elif (dir == 'right_down'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': True, '3': True,
                     '4': False, '5': False, '6': True,
                     '7': True, '8': False, '9': True}
        elif (dir == 'down_right'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': False, '3': True,
                     '4': True, '5': False, '6': False,
                     '7': True, '8': True, '9': True}
        elif (dir == 'up_right'):
            pl[x] = {'x': c_pos, 'y': r_pos,
                     '1': True, '2': True, '3': True,
                     '4': True, '5': False, '6': False,
                     '7': True, '8': False, '9': True}
        c_pos += c_add
        r_pos += r_add
