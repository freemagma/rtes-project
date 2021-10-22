<template>
  <table>
    <tr v-for="(row, r) of grid" :key="r">
      <td v-for="(cell, c) of row" :key="(r, c)">
        <Cell
          :letter="grid[r][c]"
          :currentClue="currentClue"
          :relevantClues="clue_grid[r][c]"
          :focused="focus.r == r && focus.c == c"
          @update:letter="updateLetter(r, c, $event)"
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
    updateLetter(r, c, letter) {
      this.grid[r][c] = letter;

      let new_r = this.direction == "across" ? r : r + 1;
      let new_c = this.direction == "across" ? c + 1 : c;
      if (!this.freeSquare(new_r, new_c)) {
        let clue_num = this.currentClue.num;
        do {
          clue_num++;
          if (clue_num == this.clues.length) {
            clue_num = 1;
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
