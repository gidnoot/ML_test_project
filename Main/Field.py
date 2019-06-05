class Field():
    def __init__(self, block_width, block_height, screen_width, screen_height):
        self.block_width = block_width
        self.block_height = block_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.field_dict = []
        self.calculate_blocks(screen_width, screen_height)
        self.get_block_coords()

    def calculate_blocks(self, screen_width, screen_height):
        self.columns = int(screen_width / self.block_width)
        self.rows = int(screen_height / self.block_height)

    def get_block_coords(self):
        for x in range(self.columns):
            self.field_dict.append([])
            for y in range(self.rows):
                self.field_dict[x].append([])
                x1 = self.block_width * y
                x2 = x1 + self.block_width
                y1 = self.block_height * x
                y2 = y1 + self.block_height
                self.field_dict[x][y] = {'x1' : x1, 'y1' : y1, 'x2' : x2, 'y2' : y2, 'block' : 0}
