from collections import defaultdict
import itertools as it
import puz

"""
    A data representation of a currently open crossword.
    This is what will be persisted to the database.

    The crossword's key will be the room id it is associated with.
    The constructor takes a blank instance of the crossword, copies the data,
    and also the associated room_id.
"""
class Crossword:
    # I have no idea if this is good but im doing it
    @staticmethod
    def get_title_from_filename(filename):
        puzzle = puz.read(f"src/resources/{filename}.puz")
        title = f"{puzzle.title}  {puzzle.copyright}"
        print("TITLE: ", title)
        return title

    def __init__(self, filename, room_id):
        self.filename = filename
        self.room_id = room_id
        self.set_init_crossword_data()

    def set_init_crossword_data(self):
        # TODO: Make file part of a database instead
        puzzle = puz.read(f"src/resources/{self.filename}.puz")

        grid = [
                [
                    "#" if puzzle.fill[col + row * puzzle.width] == "." else ""
                for col in range(puzzle.width)
            ]
            for row in range(puzzle.height)
        ]

        numbering = puzzle.clue_numbering()
        clues = [
            {}
            for _ in range(
                max(clue["num"] for clue in [*numbering.down, *numbering.across]) + 1
            )
        ]
        clues[0] = None
        index_to_nums = defaultdict(lambda: {"down": None, "across": None})
        clue_grid = [
            [None if val == "#" else {"down": None, "across": None} for val in row]
            for row in grid
        ]

        for clue, direction in [
            *zip(numbering.down, it.repeat("down")),
            *zip(numbering.across, it.repeat("across")),
        ]:
            num, flat_index, clue = clue["num"], clue["cell"], clue["clue"]
            clues[num][direction] = clue

            start_r, start_c = flat_index // puzzle.width, flat_index % puzzle.width
            clues[num]["start_r"] = start_r
            clues[num]["start_c"] = start_c
            index_to_nums[(start_r, start_c)][direction] = num

        for r, row in enumerate(clue_grid):
            for c, clue_dict in enumerate(row):
                if clue_dict is None:
                    continue
                cur_r, cur_c = r + 1, c
                while clue_dict["down"] is None:
                    cur_r -= 1
                    clue_dict["down"] = index_to_nums[(cur_r, cur_c)]["down"]
                cur_r, cur_c = r, c + 1
                while clue_dict["across"] is None:
                    cur_c -= 1
                    clue_dict["across"] = index_to_nums[(cur_r, cur_c)]["across"]

        self.title = puzzle.title
        self.author = puzzle.author
        self.grid = grid
        self.width = puzzle.width
        self.height = puzzle.height
        self.clues = clues
        self.clue_grid = clue_grid


    def get_label_data(self):
        data = {
            "title": self.title,
            "author": self.author
        }
        return data

    def get_puzzle_data(self):
        data = {
            "grid": self.grid,
            "width": self.width,
            "height": self.height,
            "clues": self.clues,
            "clue_grid": self.clue_grid,
        }
        return data