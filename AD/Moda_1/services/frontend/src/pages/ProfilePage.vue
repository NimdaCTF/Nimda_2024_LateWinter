<template>
    <form @submit.prevent="onSubmit" >
        <div class="card">
            <Panel >
                <template #header>
                    <div class="flex w-full align-items-center flex-column gap-4">
                        <div class="flex flex-column gap-2 align-items-center">
                            <Avatar class="w-20rem h-20rem border-circle overflow-hidden pointer-events-none select-none" :image="userStore.avatarURL" size="xlarge" alt="Avatar"/>
                            <span class="text-lg font-bold">{{ userStore.user?.username }}</span>
                        </div>
                        <span class="flex flex-row gap-1">
                            <FileUpload
                                chooseLabel="Изменить аватар" 
                                mode="basic" 
                                name="file"
                                :url=uploadURL 
                                withCredentials='true' 
                                accept="image/*" 
                                :maxFileSize="1000000" 
                                @upload="onUpload($event)"
                                auto
                                @error="userStore.checkAuth()"
                                
                            />
                        </span>
                    </div>
                </template>
                <Fieldset class="w-full" legend="Настройки учётной записи">
                    <div class="flex flex-column gap-5">
                        <div class="flex flex-column gap-2">
                            <label for="username">Логин</label>
                            <InputText id="username" v-model="usernameValue" aria-describedby="username" />
                            <small class="p-error  text-xs">
                                {{ usernameErrorMessage || '&nbsp;' }}
                            </small>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="email">Электронная почта</label>
                            <InputText id="email" v-model="emailValue" aria-describedby="email" />
                            <small class="p-error  text-xs">
                                {{ emailErrorMessage || '&nbsp;' }}
                            </small>
                        </div>
                        <div class="flex flex-column gap-2">
                            <label for="password">Изменение пароля</label>
                            <Password :feedback="false" v-model="passwordValue" placeholder="Новый пароль" />
                            <small class="p-error  text-xs">
                                {{ passwordErrorMessage || '&nbsp;' }}
                            </small>
                        </div>
                        <div class="flex flex-column gap-2">
                            <Password :feedback="false" v-model="passwordConfirmValue" placeholder="Подтвердите новый пароль" />
                            <small class="p-error  text-xs">
                                {{ passwordConfirmErrorMessage || '&nbsp;' }}
                            </small>
                        </div>
                        
                    </div>
                </Fieldset>
                <template #footer>
                    <div class="flex gap-3 mt-1">
                        <Button label="Отменить" severity="secondary" @click="setInitialValues" :disabled="!isNotEdited" outlined class="w-full" />
                        <Button label="Сохранить" type="submit" :disabled="!isNotEdited" :loading="loading" class="w-full" />
                    </div>
                </template>
            </Panel>
        </div>
    </form>
    <Toast/> 
</template>

<script setup>
import Button from 'primevue/button'
import Fieldset from 'primevue/fieldset';
import FileUpload from 'primevue/fileupload';
import Avatar from 'primevue/avatar';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Panel from 'primevue/panel';
import Toast from "primevue/toast";

import axios from 'axios';
import { useUserStore } from "@/store/user";
import { useField, useForm } from 'vee-validate';
import { useToast } from 'primevue/usetoast';
import * as Yup from 'yup';
import { computed, ref } from 'vue'

const userStore = useUserStore()
const toast = useToast();

const initialUsernameValue = ref(userStore.user.username);
const initialEmailValue = ref(userStore.user.email);
const loading = ref(false)

const schema = Yup.object().shape({
    username: Yup.string()
        .required('Новый логин не может быть пустым'),
    email: Yup.string()
        .required('Новая почта не может быть пустой').email('Введите корректный email'),
    password: Yup.string()
        .min(6, 'Новый пароль должен состоять минимум из 6 символов'),
    passwordConfirm: Yup.string()
        .min(6, 'Новый пароль должен состоять минимум из 6 символов')
        .oneOf([Yup.ref('password')], 'Пароли не совпадают'),
});

const { handleSubmit, resetForm } = useForm({ 
    validationSchema: schema,
});
const { value: usernameValue, errorMessage: usernameErrorMessage } = useField('username');
const { value: emailValue, errorMessage: emailErrorMessage } = useField('email');
const { value: passwordValue, errorMessage: passwordErrorMessage } = useField('password');
const { value: passwordConfirmValue, errorMessage: passwordConfirmErrorMessage } = useField('passwordConfirm');

const setInitialValues = () => {
    usernameValue.value = initialUsernameValue.value
    emailValue.value = initialEmailValue.value
}

const updateInitialValues = () => {
    initialUsernameValue.value = userStore.user.username
    initialEmailValue.value = userStore.user.email
}

setInitialValues()

const isNotEdited = computed(() => usernameValue.value !== initialUsernameValue.value || emailValue.value !== initialEmailValue.value)

const baseURL = axios.defaults.baseURL;
const uploadURL = `${baseURL}user/image`

const onUpload = () => {
    userStore.getImage()
}

const showSuccessToast = () => {
    return toast.add({ severity: 'success', summary: 'Данные успешно обновлены!', life: 6000 });
};
const showFailToast = (detail) => {
    return toast.add({ severity: 'fail', summary: 'Ошибка при обновлении данных!', detail: detail, life: 3000 });
};

const onSubmit = handleSubmit(async (values) => {
    const { username, email, password, passwordConfirm } = values;
    let status;
    loading.value = true;
    try {
        await schema.validate({ username, email, password, passwordConfirm }, { abortEarly: false });
        status = await userStore.update(email, username, password)
        updateInitialValues()
    } catch (error) {
        console.error(error)
        setInitialValues()
    }
    finally {
        status ? showSuccessToast() : showFailToast(userStore.errorDetail)
        loading.value = false;
    }
});
</script>