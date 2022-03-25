class Option():

    def __init__(self, index, command, description):
        self.index = index
        self.command = command
        self.description = description

    def get_index(self):
        return self.index
