import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LoginRegister from '../views/LoginRegister.vue'
import Dictionary from '../views/Dictionary.vue'
import Vocabulary from '../views/Vocabulary.vue'
import Folders from '../views/Folders.vue'
import Folder from '../views/Folder.vue'
import Game from '../views/Game.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/auth',
      name: 'Auth',
      component: LoginRegister
    },
    {
      path: '/dictionary',
      name: 'Dictionary',
      component: Dictionary
    },
    {
      path: '/vocabulary',
      name: 'Vocabulary',
      component: Vocabulary
    },
    {
      path: '/folders',
      name: 'Folders',
      component: Folders
    },
    {
      path: '/folder/:id',
      name: 'Folder',
      component: Folder,
      props: true
    },
    {
      path: '/game/:id',
      name: 'Game',
      component: Game,
      props: true
    }
  ]
})

export default router
