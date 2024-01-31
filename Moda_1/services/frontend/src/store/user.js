import { defineStore } from "pinia";
import axios from 'axios';
import router from '@/router/router';
import { StatusCodes } from 'http-status-codes';
import { ref } from 'vue';

export const useUserStore = defineStore("user", {
    state: () => ({
        user: null,
        isLoggedIn: false,
        errorDetail: ''
    }),
    actions: {
        async fetchUser() {
          axios.get('/user')
          .then((response) => {
            if (response.status === StatusCodes.OK) {
              this.user = response.data;
              this.isLoggedIn = true;
            }
            else signOut();
          })
        },
        async resetState() {
          this.user = null,
          this.isLoggedIn = false
        },
        async signUp(username, email, password) {
          const status = ref(false);
        
          try {
            const response = await axios.post('auth/register', {
              username: username,
              email: email,
              password: password
            });
        
            if (response.status === StatusCodes.CREATED) {
              await this.signIn(email, password);
              status.value = true;
            } else {
              status.value = false;
            }
          } catch (error) {
            this.errorDetail = error.response.data.detail
            status.value = false;
          }
        
          return status.value;
        },
        async signIn(email, password) {
          const formData = new FormData();
          formData.set('username', email);
          formData.set('password', password);
          axios.post('auth/jwt/login', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }).then((response) => {
            if (response.status === StatusCodes.NO_CONTENT) {
              this.fetchUser()
              this.isLoggedIn = true;
              router.push('/')
            }
          })
        },
        async signOut() {
          axios.post('auth/jwt/logout');
          this.resetState()
          router.push('/login')
        },
        async checkAuth() {
          try {
            const response = await axios.get('/user');
            if (response.status === StatusCodes.OK) {
              this.user = response.data;
              this.isLoggedIn = true;
              router.push('/')
            } else {
              this.resetState()
            }
          } catch (error) {
            this.resetState()
            console.error()
          }
        },
    }
})