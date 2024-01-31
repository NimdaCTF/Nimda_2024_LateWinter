import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from "@/store/user";

import axios from 'axios';

import App from '@/App.vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice';
import router from "@/router/router"

import '@/scss/style.scss'

const pinia = createPinia();
const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:3000/';

app
    .use(pinia)
    .use(PrimeVue)
    .use(ToastService)
    .use(router)
    .mount('#app')


const userStore = useUserStore();
userStore.checkAuth();