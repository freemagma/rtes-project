import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://3.84.20.143:5001/";

const app = createApp(App);
app.use(router);
app.mount("#app");
