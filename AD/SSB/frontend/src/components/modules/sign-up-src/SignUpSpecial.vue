<template>
  <div class="col-md-6 col-sm-12">
    <div class="special-login-form">
      <form @submit.prevent="signup">
        <div class="form-group">
          <input required type="text" class="form-control" placeholder="Username" v-model="login">
        </div>
        <div class="form-group">
          <input required type="password" class="form-control" placeholder="Password" v-model="password">
        </div>
        <div class="form-group">
          <input required type="password" class="form-control" placeholder="Retype password" v-model="password_retype">
        </div>
        <button type="submit" class="btn btn-black">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import deleteAllCookies from "@/utils";

export default {
  name: "SignUpSpecial",
  data() {
    return {
      login: '',
      password: '',
      password_retype: ''
    }
  },
  methods: {
    signup: function () {
      if (!this.check_fields())
        return;
      this.$store.dispatch('signup', {
        'username': this.login.trim(),
        'password': this.password,
        'signup_type': 'special'
      }).then(() => {
        if (this.$store.getters.isSignedUp) {
          this.$toast.success('Success');
          this.$router.push('/');
        } else if (this.$store.state.error) {
          this.$toast.error(this.$store.state.error);
          deleteAllCookies();
        } else
          throw new Error('EVERYTHING IS BAD');
      })
          .catch((err) => {
            this.$toast.warning('Something went wrong. Try to reload the page.')
            deleteAllCookies();
            console.log(err)
          })
    },
    check_fields: function () {
      if (this.password !== this.password_retype) {
        this.$toast.error('Passwords do not match');
        return false;
      }
      if (this.login.trim().length < 3 || this.login.trim().length > 30){
        this.$toast.error('Invalid username length');
        return false;
      }

      if (!this.login.trim().match('^[A-Za-zА-Яа-я-]{2,30}$')){
        this.$toast.error('Invalid username');
        return false;
      }

      if (this.password.length < 7 || this.password.length > 30){
        this.$toast.error('Invalid password length');
        return false;
      }

      return true;
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