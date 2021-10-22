<template>
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
        console.log(keycode);
        this.grid[this.focus.r][this.focus.c] = event.key.toUpperCase();
        this.cycleFocus(true, false);
      } else if (keycode == 8) {
        // BACKSPACE removes current letter if present
        // otherwise, it moves the focus one backwards then removes
        if (this.grid[this.focus.r][this.focus.c] == "")
          this.cycleFocus(false, false);
        this.grid[this.focus.r][this.focus.c] = "";
      } else if (keycode == 46) {
        // DEL removes the current letter
        this.grid[this.focus.r][this.focus.c] = "";
      } else if (keycode == 32) {
        // SPACE swaps directions
        this.swapDirections();
      } else if (keycode == 9) {
        // TAB moves forward or backward to a new clue
        // based on whether shift is pressed
        this.cycleFocus(!event.shiftKey, true);
      }
    },
    cycleFocus(forward, next_clue) {
      let delta = forward ? 1 : -1;
      let new_r =
        this.direction == "across" ? this.focus.r : this.focus.r + delta;
      let new_c =
        this.direction == "across" ? this.focus.c + delta : this.focus.c;
      if (next_clue || !this.freeSquare(new_r, new_c)) {
        let clue_num = this.currentClue.num;
        do {
          clue_num += delta;
          if (clue_num == this.clues.length) {
            clue_num = 1;
            this.swapDirections();
          } else if (clue_num == 0) {
            clue_num = this.clues.length - 1;
            this.swapDirections();
          }
        } while (!(this.direction in this.clues[clue_num]));
        new_r = this.clues[clue_num].start_r;
        new_c = this.clues[clue_num].start_c;
      }
      this.updateFocus(new_r, new_c);
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
      if (this.focus.r == r && this.focus.c == c) this.swapDirections();
      else {
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
    freeSquare(r, c) {
      if (r < 0 || r >= this.height || c < 0 || c >= this.width) return false;
      return this.grid[r][c] != "#";
    },
    swapDirections() {
      this.direction = this.direction == "across" ? "down" : "across";
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
</style>
