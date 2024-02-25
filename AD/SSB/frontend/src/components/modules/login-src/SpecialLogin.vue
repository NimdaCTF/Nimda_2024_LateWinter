<template>
  <div class="col-md-6 col-sm-12">
    <div class="special-login-form">
      <form @submit.prevent="auth">
        <div class="form-group">
          <input v-model="login" class="form-control" placeholder="Username" required type="text">
        </div>
        <div class="form-group">
          <input v-model="password" class="form-control" placeholder="Password" required type="password">
        </div>
        <button class="btn btn-black" type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import deleteAllCookies from "@/utils";

export default {
  name: "SpecialLogin",
  data() {
    return {
      login: '',
      password: ''
    }
  },
  methods: {
    auth: function () {
      this.$store.dispatch('login', {
        'username': this.login.trim(),
        'password': this.password,
        'auth_type': 'special'
      }).then(() => {
        if (this.$store.getters.isLoggedIn) {
          this.$store.dispatch("getUser").then(() => {
            if (!this.$store.state.user.group_id) {
              this.$router.push('/init');
            } else {
              this.$router.push('/');
            }
          })
        } else {
          this.$toast.error(this.$store.state.error);
          deleteAllCookies();
        }


      })
          .catch((err) => {
            this.$toast.warning('Something went wrong. Try to reload the page.')
            deleteAllCookies();
            console.log(err)
          })
    }
  }
}

</script>

<style scoped>
.btn-black {
  background-color: #000 !important;
  color: #fff !important;
  width: 50%;
}

</style>