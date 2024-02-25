<template>
  <div></div>
</template>

<script>

export default {
  name: "Logout",
  beforeCreate() {
    this.$store.dispatch('logout');
    this.$router.push('/login');
  }
}
</script>

<style scoped>

</style>