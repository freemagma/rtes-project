<template>
  <div class="play">
    <Crossword ref="crossword" @crossword-edit="sendCrosswordEditEvent" />
  </div>
</template>

<script>
import Crossword from "@/components/Crossword.vue";
import io from "socket.io-client";

export default {
  name: "Play",
  components: {
    Crossword,
  },
  data() {
    return {
      socket: io("ws://localhost:5001", {
        query: { room: window.location.pathname },
      }),
    };
  },
  created() {
    this.socket.on("crosswordInit", (data) => {
      this.$refs.crossword.crosswordInit(data);
    });
    this.socket.on("crosswordUpdate", (data) => {
      this.$refs.crossword.setCellCharacter(data.row, data.column, data.character)
    });
  },
  methods: {
    sendCrosswordEditEvent(data) {
      this.socket.emit("crosswordEdit", data);
    },
  }
};
</script>

<style>
.play {
  margin: 30px;
  display: flex;
  justify-content: center;
}
</style>
