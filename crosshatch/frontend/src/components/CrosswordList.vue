<template>
    <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
            <ul class="list-group">
                <li v-for="crossword in crosswords" :key="crossword.id" class="list-group-item">
                    <a :href="'/play/create/' + crossword.id">
                        {{ crossword.name }}
                    </a>
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
    }
}
</script>

<style>

</style>