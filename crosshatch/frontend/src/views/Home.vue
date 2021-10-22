<template>
  <div class="home">
    <CrosswordList />
  </div>
</template>

<script>
import CrosswordList from "@/components/CrosswordList.vue";

export default {
  name: "Home",
  components: {
    CrosswordList,
  },
};
</script>
