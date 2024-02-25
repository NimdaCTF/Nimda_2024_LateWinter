import {createRouter, createWebHistory} from 'vue-router'
import { useUserStore } from "@/store/user";

import HomePage from "@/pages/HomePage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterPage
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage,
        meta: { requiresAuth: true },
    },
    { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
    routes,
    history: createWebHistory(import.meta.env.BASE_URL),
})

router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore();
  
    if (to.meta.requiresAuth) {  
      if (!userStore.isLoggedIn) return next('/login');
    }
  
    if (userStore.isLoggedIn && (to.path === '/login' || to.path === '/register')) {
      return next();
    }
  
    next();
  });

export default router