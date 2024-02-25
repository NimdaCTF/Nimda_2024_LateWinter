<template>
<div class="flex flex-wrap align-items-center justify-content-center h-full">
    <div class="surface-card p-4 shadow-2 border-round-3xl w-full lg:w-3 m-auto">
        <div class="text-center mb-5">
            <img src="/images/logos/moda-logo.svg" alt="Logo" height="250" class="mb-3 svg" />
            <div class="text-900 text-3xl font-medium mb-3">Добро пожаловать!</div>
            <span class="text-600 font-medium line-height-3">Не зарегистрированы?</span>
            <RouterLink to="/register" class="font-medium no-underline ml-2 text-pink-500 cursor-pointer">Создайте аккаунт!</RouterLink>
        </div>
    
        <form @submit.prevent="onSubmit">
            <label for="email" class="block text-900 font-medium mb-2">Почта</label>
            <InputText :class="{ 'p-invalid': emailErrorMessage }" v-model="emailValue" id="email" type="text" class="w-full border-round-xl" />
            <small class="p-error text-xs">
                {{ emailErrorMessage || '&nbsp;'}}
            </small>

            <label for="password" class="block text-900 font-medium mb-2 mt-2">Пароль</label>
            <Password :class="{ 'p-invalid': passwordErrorMessage}" :feedback="false" toggleMask v-model="passwordValue" id="password" type="password" class="w-full"/>
            <small class="p-error  text-xs">
                {{ passwordErrorMessage || '&nbsp;' }}
            </small>
    
            <Button type="submit" label="Войти" :loading="loading" icon="pi pi-user" class="w-full border-round-xl"></Button>
        </form>
    </div>
    <Toast/>
</div>
</template>

<script setup>
import Button from "primevue/button";
import Password from 'primevue/password';
import InputText from "primevue/inputtext";
import Toast from "primevue/toast";

import * as Yup from 'yup';

import { RouterLink } from 'vue-router'
import { ref } from "vue";

import { useUserStore } from "@/store/user";
import { useToast } from 'primevue/usetoast';
import { useField, useForm } from 'vee-validate';

const userStore = useUserStore()
const toast = useToast();

const schema = Yup.object().shape({
    email: Yup.string().required('Введите почту').email('Введите корректный email'),
    password: Yup.string().required('Введите пароль').min(6, 'Минимальная длина пароля 6 символов')
});

const showSuccessToast = () => {
    return toast.add({ severity: 'success', summary: 'Успешный вход!', life: 6000 });
};
const showFailToast = (detail) => {
    return toast.add({ severity: 'fail', summary: 'Ошибка при входе!', detail: detail, life: 3000 });
};

const { handleSubmit, resetForm } = useForm();
const { value: emailValue, errorMessage: emailErrorMessage } = useField('email', schema.fields.email);
const { value: passwordValue, errorMessage: passwordErrorMessage } = useField('password', schema.fields.password);

const loading = ref(false);

const onSubmit = handleSubmit(async (values) => {
    const { email, password } = values;
    let status;
    loading.value = true;
    try {
        await schema.validate({ email, password }, { abortEarly: false });
        status = await userStore.signIn(email, password)
        resetForm();
    } catch (error) {
        console.error(error)
        resetForm();
    }
    finally {
        status ? showSuccessToast() : showFailToast(userStore.errorDetail)
        loading.value = false;
    }
})
</script>


<style lang="scss" scoped>

</style>