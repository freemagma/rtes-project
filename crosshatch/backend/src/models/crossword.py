class Crossword:
    def __init__(self, id, name, filename):
        self.id = id
        self.name = name
        self.filename = filename

    def asdict(self):
        return {"name": self.name, "filename": self.filename}
