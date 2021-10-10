<template>
  <div>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";
import io from "socket.io-client";

export default {
  name: "HelloWorld",
  data() {
    return {
      greeting: "undefined",
      userList: [],
      socket: io("ws://localhost:5000"),
    };
  },
  computed: {
    message() {
      return this.greeting + " [" + this.userList.join(", ") + "]";
    },
  },
  methods: {
    getGreeting() {
      axios
        .get("/")
        .then((res) => {
          this.greeting = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getGreeting();
    this.socket.on("updateUserList", (list) => {
      this.userList = list;
    });
  },
};
</script>
