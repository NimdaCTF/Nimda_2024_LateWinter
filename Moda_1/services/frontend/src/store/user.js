import { defineStore } from "pinia";
import axios from 'axios';
import router from '@/router/router';
import { StatusCodes } from 'http-status-codes';
import { ref } from 'vue';

export const useUserStore = defineStore("user", {
    state: () => ({
        user: null,
        isLoggedIn: false,
        errorDetail: '',
        avatarURL: '',
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
            console.log(error)
            this.errorDetail = error.response?.data.detail || "Неизвестная ошибка"
            status.value = false;
          }
        
          return status.value;
        },
        async signIn(email, password) {
          const status = ref(false);
          const formData = new FormData();
          formData.set('username', email);
          formData.set('password', password);
          try {
            const response = await axios.post('auth/jwt/login', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            })

            if (response.status === StatusCodes.NO_CONTENT) {
              this.fetchUser()
              this.getImage()
              router.push('/')
              this.isLoggedIn = true;
              status.value = true;
            }
            else {
              status.value = false;
            }
          } catch (error) {
            console.log(error)
            this.errorDetail = error.response?.data.detail || "Неизвестная ошибка"
            status.value = false;
          }
          return status.value;
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
              this.getImage()
              router.push('/')
            } else {
              this.resetState()
              router.push('/')
            }
          } catch (error) {
            this.resetState()
            router.push('/')
            console.error()
          }
        },
        async getImage() {
          let data = '/images/avatar/default-avatar.png';
          try {
            const response = await axios.get('/user/image');
            if (response.status === StatusCodes.OK) {
              data = response.data
            }
          } catch (error) {
            checkAuth()
            console.error(error)
          }
          finally {
            this.avatarURL = data
          }
        },
        async update(email, username, password) {
          const status = ref(false);
          const data = {
            email: email,
            username: username,
            password: password
          };
        
          try {
            const response = await axios.put('/user/update', data);
            if (response.status === StatusCodes.OK) {
              this.user = response.data;
              status.value = true;
              this.fetchUser()
            } else {
              console.error('Failed to update user:', response.data);
              this.errorDetail = error.response?.data.detail || "Неизвестная ошибка"
              status.value = false;
            }
          } catch (error) {
            console.error('Error while updating user:', error);
            status.value = false;
          }
        
          return status.value;
        },
    }
})