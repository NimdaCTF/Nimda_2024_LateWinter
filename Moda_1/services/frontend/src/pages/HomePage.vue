<template>
    <div class="wrapper">
        <Menubar :model="items" class="border-round-3xl">
            <template #item="{ item, props, hasSubmenu, root }">
                <a v-ripple class="flex align-items-center" v-bind="props.action">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                    <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                    <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
                    <i v-if="hasSubmenu" :class="['pi pi-angle-down text-primary', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
                </a>
            </template>
            <template #end>
                <div class="flex align-items-center gap-4 p-1">
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText class="border-round-xl" placeholder="Поиск по приложению" />
                    </span>
                    <RouterLink to="/login">
                        <Avatar size="large" image="/images/avatar/avatar.png" shape="circle" />
                    </RouterLink>
                </div>
            </template>
        </Menubar>
        <div class="cards border-round-3xl">
            <DataView :value="products" :layout="layout">
                <template #header>
                    <div class="flex justify-content-end">
                        <DataViewLayoutOptions v-model="layout" />
                    </div>
                </template>
    
                <template #list="slotProps">
                    <div class="grid grid-nogutter">
                        <div v-for="(item, index) in slotProps.items" :key="index" class="col-12">
                            <div class="flex flex-column xl:flex-row xl:align-items-start p-4 gap-4" :class="{ 'border-top-1 surface-border': index !== 0 }">
                                <img class="w-9 sm:w-16rem xl:w-10rem shadow-2 block xl:block mx-auto border-round" :src="`https://primefaces.org/cdn/primevue/images/product/${item.image}`" :alt="item.name" />
                                <div class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
                                    <div class="flex flex-column align-items-center sm:align-items-start gap-3">
                                        <div class="text-2xl font-bold text-900">{{ item.name }}</div>
                                        <Rating :modelValue="item.rating" readonly :cancel="false"></Rating>
                                        <div class="flex align-items-center gap-3">
                                            <span class="flex align-items-center gap-2">
                                                <i class="pi pi-tag"></i>
                                                <span class="font-semibold">{{ item.category }}</span>
                                            </span>
                                            <Tag :value="item.inventoryStatus" :severity="getSeverity(item)"></Tag>
                                        </div>
                                    </div>
                                    <div class="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
                                        <span class="text-2xl font-semibold">${{ item.price }}</span>
                                        <Button disabled icon="pi pi-shopping-cart" rounded :disabled="item.inventoryStatus === 'OUTOFSTOCK'"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
    
                <template #grid="slotProps">
                    <div class="grid grid-nogutter">
                        <div v-for="(item, index) in slotProps.items" :key="index" class="col-12 sm:col-6 lg:col-12 xl:col-4 p-2">
                            <div class="p-4 border-1 surface-border surface-card border-round">
                                <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                                    <div class="flex align-items-center gap-2">
                                        <i class="pi pi-tag"></i>
                                        <span class="font-semibold">{{ item.category }}</span>
                                    </div>
                                    <Tag :value="item.inventoryStatus" :severity="getSeverity(item)"></Tag>
                                </div>
                                <div class="flex flex-column align-items-center gap-3 py-5">
                                    <img class="w-9 shadow-2 border-round" :src="`https://primefaces.org/cdn/primevue/images/product/${item.image}`" :alt="item.name" />
                                    <div class="text-2xl font-bold">{{ item.name }}</div>
                                    <Rating :modelValue="item.rating" readonly :cancel="false"></Rating>
                                </div>
                                <div class="flex align-items-center justify-content-between">
                                    <span class="text-2xl font-semibold">${{ item.price }}</span>
                                    <Button disabled icon="pi pi-shopping-cart" rounded :disabled="item.inventoryStatus === 'OUTOFSTOCK'"></Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
        </div>
    </div>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import Badge from 'primevue/badge';
import InputText from 'primevue/inputtext';
import Avatar from 'primevue/avatar';
import DataView from 'primevue/dataview'
import Tag from 'primevue/tag'
import DataViewLayoutOptions from 'primevue/dataviewlayoutoptions'
import Rating from 'primevue/rating'
import Button from 'primevue/button'

import { ref, onMounted } from "vue";
import { ProductService } from '@/helpers/product-service';
import { RouterLink } from 'vue-router';

onMounted(() => {
    ProductService.getProducts().then((data) => (products.value = data.slice(0, 12)));
});

const items = ref([
    {
        label: 'Главная',
        icon: 'pi pi-home'
    },
    {
        label: 'Коллекции',
        icon: 'pi pi-th-large'
    },
    {
        label: 'Сообщения',
        icon: 'pi pi-comments',
        badge: 3
    },
    {
        label: 'Настройки',
        icon: 'pi pi-cog',
    }
]);

const products = ref();
const layout = ref('grid');

const getSeverity = (product) => {
    switch (product.inventoryStatus) {
        case 'INSTOCK':
            return 'success';

        case 'LOWSTOCK':
            return 'warning';

        case 'OUTOFSTOCK':
            return 'danger';

        default:
            return null;
    }
}
</script>

<style lang="scss" scoped>

</style>