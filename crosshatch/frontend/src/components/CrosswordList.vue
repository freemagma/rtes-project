<template>
  <div class="row">
    <div class="col-2"></div>
    <div class="col-8">
      <ul class="list-group">
        <li
          v-for="crossword in crosswords"
          :key="crossword.id"
          class="list-group-item"
        >
          <div @click="createRoom(crossword.puzfilename)">
            {{ crossword.title }}
          </div>
        </li>
      </ul>
    </div>
    <div class="col-2"></div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CrosswordList",
  data() {
    return {
      crosswords: [],
    };
  },
  mounted() {
    axios.get("/crosswords").then((response) => (this.crosswords = response.data));
  },
  methods: {
    createRoom(puzfilename) {
      axios.get("/play/create/" + puzfilename).then((response) => {
        window.location.href = response.data;
      });
    },
  },
};
</script>

<style></style>
