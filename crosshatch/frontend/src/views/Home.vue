<template>
  <div class="home">
    <HelloWorld />
    <CrosswordList />
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";
import CrosswordList from "@/components/CrosswordList.vue";

export default {
  name: "Home",
  components: {
    HelloWorld,
    CrosswordList,
  },
};
</script>
