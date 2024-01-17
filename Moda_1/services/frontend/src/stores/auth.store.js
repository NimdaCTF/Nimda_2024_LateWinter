import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';
import router from '@/router/router';

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null
    }),
    actions: {
        async login(email, password) {
            try {
                const user = await fetchWrapper.post(`${baseUrl}/authenticate`, { email, password });   

                this.user = user;

                localStorage.setItem('user', JSON.stringify(user));
                
                router.push(this.returnUrl || '/');
            } catch (error) {
                console.error(error);                
            }
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/login');
        }
    }
});
