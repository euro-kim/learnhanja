// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import SearchPage from '../components/SearchPage.vue'
import InfoPage from '../components/InfoPage.vue'

const routes = [
  { path: '/', name: 'SearchPage', component: SearchPage },
  { path: '/info', name: 'InfoPage', component: InfoPage },
  { path: '/:pathMatch(.*)*', redirect: '/' }  // Redirect to SearchPage for any unknown paths
];

const router = createRouter({
  history: createWebHistory(),  // Use HTML5 History mode
  routes
});

export default router;

