<template>
  <div class="home">
    <CrosswordUpload />
    <CrosswordList />
  </div>
</template>

<script>
import CrosswordUpload from "@/components/CrosswordUpload.vue";
import CrosswordList from "@/components/CrosswordList.vue";

export default {
  name: "Home",
  components: {
    CrosswordUpload,
    CrosswordList,
  },
};
</script>
