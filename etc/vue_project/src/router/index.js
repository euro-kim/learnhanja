// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import ManagePage from '../components/00_ManagePage.vue'
import MainPage from '../components/01_MainPage.vue'
import SurveyPage from '../components/02_SurveyPage.vue'
import MemoryPage from '../components/03_MemoryPage.vue'
import TestPage from '../components/04_TestPage.vue'

const routes = [
  { path: '/manage', name: 'ManagePage', component: ManagePage },
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/survey', name: 'SurveyPage', component: SurveyPage },
  { path: '/memory', name: 'MemoryPage', component: MemoryPage },
  { path: '/test', name: 'TestPage', component: TestPage },
  { path: '/:pathMatch(.*)*', redirect: '/survey' }  // Redirect to SurveyPage for any unknown paths
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

