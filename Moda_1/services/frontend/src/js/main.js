import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { fakeBackend } from '@/helpers';

import App from '@/App.vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice';
import router from "@/router/router"

import '@/scss/style.scss'

fakeBackend();

const store = createPinia();
const app = createApp(App);
app
    .use(router)
    .use(PrimeVue)
    .use(store)
    .use(ToastService)
    .mount('#app')
