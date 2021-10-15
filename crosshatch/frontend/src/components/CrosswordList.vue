<template>
    <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
            <ul class="list-group">
                <li v-for="crossword in crosswords" :key="crossword.id" class="list-group-item">
                    <div @click="createRoom(crossword.id)">
                        {{ crossword.name }}
                    </div>
                </li>
            </ul>
        </div>
        <div class="col-2">
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "CrosswordList",
    data() {
        return {
            crosswords: []
        }
    },
    mounted () {
    axios
      .get('/puzzles')
      .then(response => (this.crosswords = response.data))
    },
    methods: {
        createRoom(puzzleId) {
            axios
              .get('/play/create/' + puzzleId)
              .then(response => {
                  window.location.href = response.data;
              })
        }
    }
}
</script>

<style>

</style>