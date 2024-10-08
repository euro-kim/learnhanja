import { createApp } from 'vue'; // Import createApp from 'vue'
import App from './App.vue'; // Import the root App component
import router from './router'

// Create a new Vue application instance
const app = createApp(App);

//rounter
app.use(router)

// Mount the app to the DOM
app.mount('#app');