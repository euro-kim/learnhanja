import { createRouter, createWebHistory } from 'vue-router';
import SearchPage from '../views/SearchPage.vue'; // Import the App component (which includes SearchBar and SearchResult)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: SearchPage // Render the App component at the root path
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/' // Redirect any unknown paths to the root
  }
];

const router = createRouter({
  history: createWebHistory(), // Use HTML5 History mode
  routes
});

export default router;
