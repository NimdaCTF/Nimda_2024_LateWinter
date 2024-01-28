<template>
    <div class="flex flex-wrap align-items-center justify-content-center h-full">
        <div class="surface-card p-4 shadow-2 border-round-3xl w-full lg:w-3 m-auto">
            <div class="text-center mb-5">
                <div class="text-900 text-3xl font-medium mb-3">Регистрация</div>
                <span class="text-600 font-medium line-height-3">Уже зарегистрированы?</span>
                <RouterLink to="/login" class="font-medium no-underline ml-2 text-pink-500 cursor-pointer">Войти</RouterLink>
            </div>
        
            <form @submit.prevent="onSubmit">
                <label for="name" class="block text-900 font-medium mb-2">Имя</label>
                <InputText :class="{ 'p-invalid': nameErrorMessage}" v-model="usernameValue" id="name" type="text" class="w-full border-round-xl" />
                <small class="p-error text-xs">
                    {{ nameErrorMessage || '&nbsp;'}}
                </small>

                <label for="email" class="block text-900 font-medium mb-2 mt-2">Почта</label>
                <InputText :class="{ 'p-invalid': emailErrorMessage}" v-model="emailValue" id="email" type="text" class="w-full border-round-xl" />
                <small class="p-error text-xs">
                    {{ emailErrorMessage || '&nbsp;'}}
                </small>
        
                <label for="password" class="block text-900 font-medium mb-2 mt-2">Пароль</label>
                <Password :class="{ 'p-invalid': passwordErrorMessage}" :feedback="false" v-model="passwordValue" id="password" type="password" class="w-full border-round-xl"/>
                <small class="p-error  text-xs">
                    {{ passwordErrorMessage || '&nbsp;' }}
                </small>

                <label for="passwordConfirm" class="block text-900 font-medium mb-2 mt-2">Подтвердите пароль</label>
                <Password :class="{ 'p-invalid': passwordConfirmErrorMessage}" :feedback="false" v-model="passwordConfirmValue" id="passwordConfirm" type="password" class="w-full"/>
                <small class="p-error  text-xs">
                    {{ passwordConfirmErrorMessage || '&nbsp;' }}
                </small>
        
                <Button type="submit" :loading="loading" label="Зарегистрироваться" icon="pi pi-user" class="w-full border-round-xl"></Button>
            </form>
        </div>
    </div>
</template>

<script setup>
import Button from "primevue/button";
import Password from 'primevue/password';
import InputText from "primevue/inputtext";

import * as Yup from 'yup';

import { RouterLink } from 'vue-router'

import { ref } from "vue";
import { useField, useForm } from 'vee-validate';

const schema = Yup.object().shape({
    name: Yup.string()
        .required('Необходимо ввести имя'),
    email: Yup.string()
        .required('Необходимо ввести почту').email('Введите корректный email'),
    password: Yup.string()
        .required('Необходимо ввести пароль')
        .min(6, 'Пароль должен состоять минимум из 6 символов'),
    passwordConfirm: Yup.string()
        .required('Необходимо ввести пароль')
        .min(6, 'Пароль должен состоять минимум из 6 символов')
        .oneOf([Yup.ref('password')], 'Пароли не совпадают'),
});

const { handleSubmit, resetForm } = useForm({ validationSchema: schema });
const { value: usernameValue, errorMessage: nameErrorMessage } = useField('name');
const { value: emailValue, errorMessage: emailErrorMessage } = useField('email');
const { value: passwordValue, errorMessage: passwordErrorMessage } = useField('password');
const { value: passwordConfirmValue, errorMessage: passwordConfirmErrorMessage } = useField('passwordConfirm');

const loading = ref(false);

const onSubmit = handleSubmit(async (values) => {
    const { username, email, password, passwordConfirm } = values;
    loading.value = true;
    try {
        await schema.validate({ username, email, password, passwordConfirm }, { abortEarly: false });
        console.log({data: {
            ...values
        }})
        resetForm();
    } catch (error) {
        console.error(error)
        resetForm();
    }
    finally {
        loading.value = false;
    }
});

</script>

<style lang="scss" scoped>

</style>