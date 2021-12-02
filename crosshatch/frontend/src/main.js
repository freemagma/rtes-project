import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://54.205.97.70:5001/";

const app = createApp(App);
app.use(router);
app.mount("#app");
