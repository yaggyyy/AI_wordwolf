class Player:

    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human

        self.role = None
        self.topic = None

        self.vote = None

        self.alive = True

        self.memory = []

    def __str__(self):
        return self.name