<template>
  <div class="cell">
    <input
      :value="displayLetter"
      @keydown="keydown($event)"
      @click="$emit('click:input')"
      :disabled="isBlank"
      :class="classes"
      type="text"
      size="1"
      ref="input"
    />
  </div>
</template>

<script>
export default {
  name: "Cell",
  props: {
    letter: String,
    currentClue: Object,
    relevantClues: Object,
    focused: Boolean,
  },
  emits: ["update:letter", "click:input"],
  computed: {
    isBlank() {
      return this.letter == "#";
    },
    classes() {
      return {
        highlight:
          !this.focused &&
          this.relevantClues &&
          this.relevantClues[this.currentClue.direction] ==
            this.currentClue.num,
        focus: this.focused,
        blank: this.isBlank,
      };
    },
    displayLetter() {
      if (this.letter == "#") return "";
      return this.letter;
    },
  },
  methods: {
    keydown(event) {
      event.preventDefault();
      if (/^[a-zA-Z]$/.test(event.key)) {
        this.$emit("update:letter", event.key.toUpperCase());
      }
    },
    focusInput() {
      this.$refs.input.focus();
    },
  },
  mounted() {
    if (this.focused) this.focusInput();
  },
};
</script>

<style>
.blank {
  background-color: black;
  color: black;
}
.highlight {
  background-color: #88d5f7;
}
.focus {
  background-color: #e1ef99;
}
input {
  caret-color: transparent;
  text-align: center;
  border: none;
}
input:focus {
  outline: none;
}
</style>
