import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios';

import App from '@/App.vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice';
import router from "@/router/router"

import '@/scss/style.scss'

const store = createPinia();
const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:3000/';

app
    .use(router)
    .use(PrimeVue)
    .use(store)
    .use(ToastService)
    .mount('#app')
