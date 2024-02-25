import Router from 'vue-router'
import store from './store.js'
import Login from "@/components/modules/Login";
import WorkSpace from "./components/modules/WorkSpace";
import Initialize from "@/components/modules/Initialize";


let router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'app',
            component: WorkSpace,
            meta: {
                requiresAuth: true,
                title: "PX | Workspace"
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: {
                title: "PX | Authentication"
            }
        },
        {
            path: '/init',
            name: 'init',
            component: Initialize,
            meta: {
                title: "PX | Initialize"
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    if (to.matched.some(record => record.meta.requiresAuth))
        if (store.getters.isLoggedIn)
            next()
        else
            next('/login')
    else
        next()

})

export default router