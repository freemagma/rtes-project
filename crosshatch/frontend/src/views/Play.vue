<template>
  <div class="play">
    <Crossword ref="crossword" />
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
      socket: io("ws://localhost:5000", {
        query: { room: window.location.pathname },
      }),
    };
  },
  created() {
    this.socket.on("crosswordInit", (data) => {
      this.$refs.crossword.crosswordInit(data);
    });
  },
};
</script>

<style>
.play {
  margin: 30px;
  display: flex;
  justify-content: center;
}
</style>
