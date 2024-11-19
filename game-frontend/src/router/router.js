import { createRouter, createWebHistory } from 'vue-router';
import Title from '@/views/title/title.vue';
import GameView from '@/views/game/game.vue';

const routes = [
  {
    path: '/',
    name: 'title',
    component: Title,
  },
  {
    path: '/game',
    name: 'game',
    component: GameView,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
