<template>
    <div v-if="isLoggedIn">
        <Menubar :model="items" class="border-round-3xl">
            <template #item="{ item, props, hasSubmenu, root }">
                <RouterLink class="no-underline" :to="item.route">
                    <a v-ripple class="flex align-items-center" v-bind="props.action">
                        <span :class="item.icon" />
                        <span class="ml-2">{{ item.label }}</span>
                        <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                        <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
                        <i v-if="hasSubmenu" :class="['pi pi-angle-down text-primary', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
                    </a>
                </RouterLink>
            </template>
            <template #end>
                <div class="flex align-items-center gap-4 p-1">
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText class="border-round-xl" placeholder="Поиск по приложению" />
                    </span>
                    <RouterLink to="/profile">
                        <Button size="small" outlined rounded class="border-2">
                            <Avatar size="large" :image="userStore.avatarURL" class="pointer-events-none select-none" shape="circle" />
                        </Button>
                    </RouterLink>
                    <Button :onClick="logout" rounded text icon="pi pi-sign-out"/>
                </div>
            </template>
        </Menubar>
    </div>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import Badge from 'primevue/badge';
import InputText from 'primevue/inputtext';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button'

import { RouterLink } from 'vue-router'
import { onMounted, ref, computed } from "vue";
import { useUserStore } from "@/store/user";

const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)

const logout = async () => {
    await userStore.signOut()
}

const items = ref([
    {
        label: 'Главная',
        icon: 'pi pi-home',
        route: '/',
        disabled: false 
    },
    {
        label: 'Коллекции',
        icon: 'pi pi-th-large',
        route: '/',
        disabled: true
    },
    {
        label: 'Сообщения',
        icon: 'pi pi-comments',
        badge: 3,
        route: '/',
        disabled: true
    },
    {
        label: 'Настройки',
        icon: 'pi pi-cog',
        route: '/profile',
        disabled: false
    }
]);
</script>