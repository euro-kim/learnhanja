// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import dataPage from '../components/DataPage.vue'


const routes = [
  { path: '/', name: 'DataPage', component: dataPage },
];

const router = createRouter({
  history: createWebHistory(),  // Use HTML5 History mode
  routes
});

router.beforeEach((to, from) => {
  if (from.name === 'TestPage' && to.name === 'SurveyPage') {
    window.location.reload();
  }
});

export default router;

