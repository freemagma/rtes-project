class Crossword():
    def __init__(self, id, name, puz_filename):
        self.id = id
        self.name = name
        self.puz_filename = puz_filename

    def asdict(self):
        return {
            'name': self.name,
            'puz_filename': self.puz_filename
        }