<template>
  <div class="col-md-6 col-sm-12">
    <div class="institute-login-form">
      <form @submit.prevent="auth">
        <div class="form-group">
          <model-select required ref="inst_select"
                        :options="inst_options"
                        v-model="institute"
                        placeholder="Institute"
          />
        </div>
        <div class="form-group" v-on:focus="get_groups">
          <model-select required ref="group_select"
                        :options="group_options"
                        v-model="group"
                        placeholder="Group"/>
        </div>
        <div class="form-group">
          <model-select required
                        ref="snp_select"
                        :options="snp_options"
                        v-model="snp"
                        placeholder="Surname Name Patronymic"/>
        </div>
        <div class="form-group">
          <input type="password" required class="form-control" placeholder="Password" v-model="password">
        </div>
        <button type="submit" class="btn btn-black">Submit</button>
      </form>
    </div>
  </div>


</template>

<script>
import {ModelSelect} from 'vue-search-select'
import axios from 'axios';
import 'vue-search-select/dist/VueSearchSelect.css'
import deleteAllCookies from "@/utils";

export default {
  name: "InstituteLogin",
  components: {
    ModelSelect
  },
  data() {
    return {
      institute: null,
      group: null,
      snp: null,
      password: '',
      inst_options: [],
      group_options: [],
      snp_options: []
    }
  },
  methods:
      {
        get_institutes: async function () {
          let _ = [];
          await axios.get(this.$store.state.api_host + '?method=getInstitutesList').then((response) => {
            response.data.values.forEach((item) => {
              _.push({
                "value": item.id,
                "text": item.name
              })
            })
            this.inst_options = _;
          })
        },
        get_groups: async function (institute_id) {
          let _ = [];
          await axios.get(this.$store.state.api_host + '?method=getGroupsByInstitute&institute_id=' + institute_id).then((response) => {

            response.data.values.forEach((item) => {
              _.push({
                "value": item.id,
                "text": item.name
              })
            })
            this.group_options = _;
          })
        },
        get_students: async function (group_id) {
          let _ = [];
          await axios.get(this.$store.state.api_host + '?method=getStudentsByGroup&group_id=' + group_id).then((response) => {
            response.data.values.forEach((item) => {
              _.push({
                "value": item.id,
                "text": `${item.surname} ${item.name} ${item.patronymic}`
              })
            })
            this.snp_options = _;
          })
        },
        auth: async function (with_check = true, verbose = true) {
          if (with_check && !await this.is_fields_correct())
            return;

          this.$store.dispatch('login', {
            'id': this.snp || '',
            'password': this.password || '',
            'auth_type': 'institute'
          }).then(() => {
            if (this.$store.getters.isLoggedIn) {
              this.$router.push('/');
            } else if (this.$store.state.error) {
              if (verbose)
                this.$toast.error(this.$store.state.error);
              deleteAllCookies();
            } else
              throw new Error('EVERYTHING IS BAD');
          }).catch(err => {
            console.warn(err);
            if (verbose)
              this.$toast.warning('Something went wrong. Try to reload the page.')
            deleteAllCookies();
          })
        },
        is_fields_correct: async function () {
          if (!this.institute || !this.group || !this.snp) {
            this.$toast.error('Fill all fields');
            return false;
          }
          return true;
        }

      },
  async beforeMount() {
    if (document.cookie.includes('PHPSESSID='))
      await this.auth(false, false);
  },
  async mounted() {
    await this.get_institutes();
  },
  watch: {
    institute: async function (value) {
      await this.get_groups(value);
    },
    group: async function (value) {
      await this.get_students(value);
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