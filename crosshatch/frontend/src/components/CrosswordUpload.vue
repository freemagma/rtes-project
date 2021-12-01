<template>
  <div class="row">
    <div class="col-4"></div>
    <div class="col-4">
      <form v-on:submit.prevent="onUpload">
        <div class="mb-3">
          <label for="crosswordTitleInput" class="form-label">Crossword Title</label>
          <input v-model="crosswordTitle" class="form-control" id="crosswordTitleInput" placeholder="Crossword Title">
        </div>
        <div class="mb-3">
          <label for="crosswordPuzFileInput" class="form-label">Crossword Puz File</label>
          <input class="form-control" type="file" id="crosswordPuzFileInput" v-on:change="onFileChange">
        </div>
        <div class="mb-3">
          <button class="btn btn-success" type="submit">Upload Crossword</button>
        </div>
      </form>
    </div>
    <div class="col-4"></div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CrosswordUpload",
  data() {
    return {
      crosswordTitle: null,
      crosswordPuzFile: null,
    };
  },
  methods: {
    onFileChange(event) {
      this.crosswordPuzFile = event.target.files[0]
    },
    onUpload() {
      if (this.crosswordTitle && this.crosswordPuzFile) {
        let formData = new FormData();
        console.log(this.crosswordPuzFile);
        formData.append('puzfile', this.crosswordPuzFile);
        axios.post('/crosswords/puzfile', formData, {
        }).then((response) => {
          console.log(response);
          let new_blank_crossword = {
            title: this.crosswordTitle,
            puzfilename: response.data
          };
          axios.post('/crosswords', new_blank_crossword, {
          }).then((response) => {
            console.log(response);
          });
        });
      } else {
        console.log("ERROR: No crossword title and/or puzfile for upload!")
      }
    }
  },
};
</script>

<style></style>
