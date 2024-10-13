import { createRouter, createWebHistory } from 'vue-router';
import SearchPage from '../components/pages/SearchPage.vue'; 
import StudyPage from '../components/pages/StudyPage.vue'; 
import StudyEomunhoe from '@/components/StudyEomunhoe.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: SearchPage,
  },
  {
    path: '/Study',
    name: 'Study',
    component: StudyPage,
    children: [
      {
        path: 'eomunhoe', 
        name: 'StudyEomunhoe',
        component: StudyEomunhoe
      },
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/main' // Redirect any unknown paths to the root
  }
];

const router = createRouter({
  history: createWebHistory(), // Use HTML5 History mode
  routes
});

export default router;
