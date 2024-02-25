<script setup>
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
</script>

<template>
  <div class="wrapper gap-3">
    <TheHeader/>
    <RouterView></RouterView>
  </div>
</template>

