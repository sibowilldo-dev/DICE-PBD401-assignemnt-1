import { createApp } from "vue";
import { createAuth0 } from "@auth0/auth0-vue";
import "./style.css";
import App from "./App.vue";

const app = createApp(App);
const auth0config = {
    domain: "dice-pbdev401.us.auth0.com",
    clientId: "x5g3TkIOLbkJkxRtiN57g7CdwGRo7X4H",
    authorizationParams: {
        redirect_uri: window.location.origin,
    },
};
app.use(createAuth0(auth0config));

app.mount("#app");
