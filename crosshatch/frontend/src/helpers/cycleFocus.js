export default function cycleFocus(
  crossword,
  {
    backwards = false,
    cycle_clue = true,
    cycle_in_word = true,
    force_cycle_clue = false,
    skip_unfree = true,
  } = {}
) {
  const delta = backwards ? -1 : 1;
  var new_clue, new_dir, new_r, new_c;

  const resetPosition = () => {
    new_clue = crossword.currentClue.num;
    new_dir = crossword.direction;
    new_r = crossword.focus.r;
    new_c = crossword.focus.c;
  };
  const incrementCell = (delta) => {
    new_r += delta * (new_dir == "down");
    new_c += delta * (new_dir == "across");
  };
  const resetInWord = (delta) => {
    new_r = crossword.clues[new_clue].start_r;
    new_c = crossword.clues[new_clue].start_c;
    if (delta == -1) {
      while (crossword.whiteCell(new_r, new_c)) {
        incrementCell(1);
      }
      incrementCell(-1);
    }
  };
  const incrementClue = (delta) => {
    do {
      new_clue += delta;
      if (new_clue == 0 || new_clue == crossword.clues.length) {
        new_clue += -1 * delta * (crossword.clues.length - 1);
        new_dir = crossword.opposite(new_dir);
      }
    } while (!(new_dir in crossword.clues[new_clue]));
    resetInWord(delta);
  };
  const smartIncrementCell = (delta) => {
    incrementCell(delta);
    if (!crossword.whiteCell(new_r, new_c)) {
      incrementClue(delta);
    }
  };
  const advance = (increment, arg) => {
    const start_r = new_r;
    const start_c = new_c;
    const start_dir = new_dir;
    while (
      crossword.whiteCell(new_r, new_c) &&
      skip_unfree &&
      !crossword.freeCell(new_r, new_c)
    ) {
      increment(arg);
      if (new_r == start_r && new_c == start_c && new_dir == start_dir) {
        return;
      }
    }
  };

  resetPosition();
  if (force_cycle_clue) {
    incrementClue(delta);
    advance(smartIncrementCell, delta);
    resetInWord(1);
  } else {
    incrementCell(delta);
    advance(incrementCell, delta);
    if (cycle_in_word && !crossword.whiteCell(new_r, new_c)) {
      resetInWord(delta);
      advance(incrementCell, delta);
    }
    if (cycle_clue && !crossword.whiteCell(new_r, new_c)) {
      resetPosition();
      smartIncrementCell(delta);
      advance(smartIncrementCell, delta);
    }
  }

  if (
    crossword.whiteCell(new_r, new_c) &&
    (force_cycle_clue || !skip_unfree || crossword.freeCell(new_r, new_c))
  ) {
    crossword.direction = new_dir;
    crossword.setFocus(new_r, new_c);
  }
}
