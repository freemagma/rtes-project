<template>
  <div>
    <table>
      <tr v-for="(row, r) of grid" :key="r">
        <td v-for="(cell, c) of row" :key="(r, c)">
          <Cell
            :letter="grid[r][c]"
            :currentClue="currentClue"
            :relevantClues="clue_grid[r][c]"
            :focused="focus.r == r && focus.c == c"
            @keydown:input="keydown($event)"
            @click:input="clickEvent(r, c)"
            :ref="(el) => setCellRef(el, r, c)"
          />
        </td>
      </tr>
    </table>
    <div class="clue">
      <h3>{{ currentClueText }}</h3>
    </div>
  </div>
</template>

<script>
import Cell from "@/components/Cell.vue";

export default {
  name: "Crossword",
  components: { Cell },
  data() {
    return {
      grid: null,
      width: 0,
      height: 0,
      clues: [],
      clue_grid: null,
      focus: { r: 0, c: 0 },
      direction: "across",
      cellRefs: {},
    };
  },
  computed: {
    currentClue() {
      if (this.clue_grid === null)
        return { num: undefined, direction: this.direction };
      return {
        num: this.clue_grid[this.focus.r][this.focus.c][this.direction],
        direction: this.direction,
      };
    },
    currentClueText() {
      if (this.clue_grid === null) return "";
      let letter = this.direction.charAt(0).toUpperCase();
      let clue = this.clues[this.currentClue.num][this.direction];
      return `${this.currentClue.num}${letter}: ${clue}`;
    },
  },
  methods: {
    crosswordInit(data) {
      this.grid = data.grid;
      this.width = data.width;
      this.height = data.height;
      this.clues = data.clues;
      this.clue_grid = data.clue_grid;
      this.direction = "across";
      this.updateFocus(this.clues[1].start_r, this.clues[1].start_c);
    },
    keydown(event) {
      let keycode = event.keyCode;
      if (
        (65 <= keycode && keycode <= 90) ||
        (97 <= keycode && keycode <= 122)
      ) {
        // input was a letter
        this.grid[this.focus.r][this.focus.c] = event.key.toUpperCase();
        this.cycleFocus();
      } else if (keycode == 8) {
        // BACKSPACE removes current letter if present
        // otherwise, it moves the focus one backwards then removes
        if (this.grid[this.focus.r][this.focus.c] == "")
          this.cycleFocus({ backwards: true });
        this.grid[this.focus.r][this.focus.c] = "";
      } else if (keycode == 46) {
        // DEL removes the current letter
        this.grid[this.focus.r][this.focus.c] = "";
      } else if (keycode == 32) {
        // SPACE swaps directions
        this.direction = this.opposite(this.direction);
      } else if (keycode == 9) {
        // TAB moves forward or backward to a new clue
        // based on whether shift is pressed
        this.cycleFocus({ backwards: event.shiftKey, force_cycle_clue: true });
      } else if (37 <= keycode && keycode <= 40) {
        // ARROW keys switch direction and move among row/col
        if ((keycode % 2 ? "across" : "down") != this.direction) {
          this.direction = this.opposite(this.direction);
        } else {
          const delta = keycode <= 38 ? -1 : 1;
          let new_r = this.focus.r;
          let new_c = this.focus.c;
          do {
            new_r += delta * (this.direction == "down");
            new_c += delta * (this.direction == "across");
            if (this.whiteCell(new_r, new_c)) {
              this.updateFocus(new_r, new_c);
              break;
            }
          } while (this.inBounds(new_r, new_c));
        }
      }
    },
    cycleFocus({
      backwards = false,
      cycle_clue = true,
      cycle_in_word = true,
      force_cycle_clue = false,
    } = {}) {
      const delta = backwards ? -1 : 1;
      let new_clue = this.currentClue.num;
      let new_dir = this.direction;
      let new_r = this.focus.r;
      let new_c = this.focus.c;

      const incrementCell = (delta) => {
        new_r += delta * (new_dir == "down");
        new_c += delta * (new_dir == "across");
      };
      const advanceCell = (delta) => {
        while (this.whiteCell(new_r, new_c) && !this.freeCell(new_r, new_c)) {
          incrementCell(delta);
        }
      };
      const resetInWord = () => {
        new_r = this.clues[new_clue].start_r;
        new_c = this.clues[new_clue].start_c;
      };
      const incrementClue = (delta) => {
        new_clue += delta;
        if (new_clue == 0 || new_clue == this.clues.length) {
          new_clue += -1 * delta * (this.clues.length - 1);
          new_dir = this.opposite(new_dir);
        }
        resetInWord();
      };
      const advanceClue = (delta) => {
        let start_dir = new_dir;
        let start_clue = new_clue;
        advanceCell(1);
        while (!this.freeCell(new_r, new_c)) {
          incrementClue(delta);
          if (new_dir == start_dir && new_clue == start_clue) {
            return;
          }
          advanceCell(1);
        }
      };

      if (force_cycle_clue) {
        incrementClue(delta);
        advanceClue(delta);
      } else {
        advanceCell(delta);
        if (cycle_in_word && !this.whiteCell(new_r, new_c)) {
          resetInWord();
          advanceCell(1);
        }
        if (cycle_clue && !this.whiteCell(new_r, new_c)) {
          advanceClue(delta);
        }
      }

      if (force_cycle_clue || this.freeCell(new_r, new_c)) {
        this.direction = new_dir;
        this.updateFocus(new_r, new_c);
      }
    },
    updateFocus(r, c) {
      this.focus.r = r;
      this.focus.c = c;
      let cellRefKey = this.cellRefKey(r, c);
      if (cellRefKey in this.cellRefs) {
        this.cellRefs[cellRefKey].focusInput();
      }
    },
    clickEvent(r, c) {
      if (this.focus.r == r && this.focus.c == c) {
        this.direction = this.opposite(this.direction);
      } else {
        this.focus.r = r;
        this.focus.c = c;
      }
    },
    cellRefKey(r, c) {
      return `${r}:${c}`;
    },
    setCellRef(el, r, c) {
      this.cellRefs[this.cellRefKey(r, c)] = el;
    },
    inBounds(r, c) {
      return !(r < 0 || r >= this.height || c < 0 || c >= this.width);
    },
    whiteCell(r, c) {
      return this.inBounds(r, c) && this.grid[r][c] != "#";
    },
    freeCell(r, c) {
      return this.inBounds(r, c) && this.grid[r][c] == "";
    },
    opposite(direction) {
      return direction == "across" ? "down" : "across";
    },
  },
};
</script>

<style>
table {
  background-color: black;
  border: 1px solid black;
  font-size: 20px;
}
.clue {
  padding: 30px;
}
</style>
