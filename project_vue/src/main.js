import { createApp } from 'vue'; // Import createApp from 'vue'
import App from './App.vue'; // Import the root App component
import store from './store'; // Import the Vuex store (adjust path if needed)

// Create a new Vue application instance
const app = createApp(App);

// Use Vuex store in the app
app.use(store);

// Mount the app to the DOM
app.mount('#app');
