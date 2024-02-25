<template>
  <div class="change-password">
    <h3>Change password</h3>
    <input type="password" placeholder="Password" v-model="password">
    <input type="password" placeholder="Retype password" v-model="retype_password">
    <button class="btn btn-primary" v-on:click="changePassword">Apply</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChangePassword",
  data() {
    return {
      'password': '',
      'retype_password': ''
    }
  },
  methods:{
    changePassword: async function (){
      if (this.password !== this.retype_password) {
        this.$toast.error('Passwords do not match');
        return false;
      }

      if (this.password.length < 7 || this.password.length > 30){
        this.$toast.error('Invalid password length');
        return false;
      }

      await axios({
        url: this.$store.state.api_host,
        data: {'method': 'updatePassword', 'password': this.password},
        withCredentials: true,
        method: 'POST'
      }).then((response) => {
        if (response.data.status){
          this.$toast.success('Successfully changed');
          this.password = '';
          this.retype_password = '';
        }
        else{

          this.$toast.error(response.data.error);}
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    }
  }
}
</script>

<style lang="scss" scoped>

$block-width: 400px;

.change-password{
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  width: 400px;
  height: 200px;
  border-radius: 10px;
  border: black solid 1px;
  @media (max-width: 400px) {
    width: 200px;
  }
}

.change-password input {
  width: 300px;
  margin-left: $block-width/9;
  @media (max-width: 400px) {
    width: 200px;
    margin-left: 0;
  }
}

.change-password button{
  width: 200px;
  margin-left: $block-width/4;
  margin-top: 5px;
  @media (max-width: 400px) {
    width: 150px;
    margin-left: 0;
  }
}


</style>