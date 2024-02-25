import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Home from "./components/modules/Profile";
import InstituteLogin from "@/components/modules/login-src/InstituteLogin";
import SpecialLogin from "@/components/modules/login-src/SpecialLogin";
import SignUpSpecial from "@/components/modules/sign-up-src/SignUpSpecial";
import deleteAllCookies from "@/utils";

Vue.use(Vuex)
export default new Vuex.Store({
    state: {
        loginState: false,
        signUpState: false,
        error: "",
        user: {},
        current_module: Home,
        current_module_params: {},
        current_login_module: [InstituteLogin, 0],
        is_menu_opened: false,
        menu_content: null,
        api_host: 'http://localhost:8099/index.php',
        viewCourseId: NaN,
        taskId: NaN
    },
    mutations: {
        change_module(state, new_module) {
            state.current_module = new_module;
        },
        change_active_module(state, module_name) {
            state.menu_content.forEach(function (item, i, arr) {
                arr[i].is_active = item.title === module_name;
            })
        },
        change_login_module(state, new_module) {
            let num = 0;
            if (new_module === SpecialLogin)
                num = 1;
            else if (new_module === SignUpSpecial)
                num = 2;
            state.current_login_module = [new_module, num];
        },
        toggle_menu(state) {
            state.is_menu_opened = !state.is_menu_opened;
        },
        set_menu_items(state, items) {
            state.menu_content = items;
        },
        auth_state(state, status, user) {
            state.loginState = status
            state.user = user
        },
        logout(state) {
            state.loginState = false;
            state.signUpState = false;
            state.error = "";
            state.user = {};
            state.current_module = Home;
            state.current_login_module = [InstituteLogin, 0];
            state.is_menu_opened = false;
            state.menu_content = null;
            state.current_module_params = {};
        },
        signup_state(state, status) {
            state.signUpState = status
        },
        set_user(state, user) {
            state.user = user;
        }
    },
    getters: {
        isLoggedIn: state => state.loginState,
        isSignedUp: state => state.signUpState
    },
    actions: {
        login({commit}, user) {
            return new Promise((resolve) => {
                let requestData = {
                    'method': 'auth'
                }
                Object.assign(requestData, user);
                axios({url: this.state.api_host, data: requestData, method: 'POST', withCredentials: true})
                    .then(resp => {
                        const reply = resp.data;
                        if (reply.status) {
                            commit('auth_state', true, resp.data);

                            if (!document.cookie.includes('PHPSESSID') && reply.token)
                                document.cookie += 'PHPSESSID=' + reply.token + ';'
                            resolve(resp);
                        } else
                            throw new Error(reply.error);
                    })
                    .catch((err) => {
                        this.state.error = err.toString();
                        commit('auth_state', false, {})
                        resolve(err);
                    })
            })
        },
        logout({commit}) {
            deleteAllCookies();
            return new Promise((resolve) => {
                axios({url: this.state.api_host, data: {'method': 'logout'}, withCredentials: true, method: 'POST'})
                    .then(resp => {
                        commit('logout')
                        resolve(resp)
                    })
                    .catch((err) => {
                        resolve(err);
                    })
            })
        },
        signup({commit}, user) {
            return new Promise((resolve) => {
                let requestData = {
                    'method': 'signup'
                }
                Object.assign(requestData, user);
                axios({url: this.state.api_host, data: requestData, method: 'POST', withCredentials: true})
                    .then(resp => {
                        const reply = resp.data;
                        if (reply.status) {
                            commit('signup_state', true)
                            commit('change_login_module', SpecialLogin)
                            resolve(resp)
                        } else
                            throw new Error(reply.error);
                    })
                    .catch((err) => {
                        this.state.error = err.toString();
                        commit('signup_state', false)
                        resolve(err);
                    })
            })
        },
        getUser({commit}) {
            return new Promise((resolve) => {
                axios({url: this.state.api_host + '/?method=getUser', method: 'GET', withCredentials: true})
                    .then(resp => {
                        const reply = resp.data;
                        if (reply.status) {
                            commit('set_user', reply)
                            resolve(resp)
                        } else
                            throw new Error(reply.error);
                    })
                    .catch((err) => {
                        this.state.error = err.toString();
                        resolve(err);
                    })
            })
        }

    }
})