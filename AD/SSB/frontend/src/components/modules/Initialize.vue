<template>
  <div class="init-page">
    <center>
      <h1>Hey. Where are you from?</h1>
      <div class="component">
        <div class="col-md-6 col-sm-12">
          <div class="institute-login-form">
            <form @submit.prevent="init">
              <div class="form-group">
                <model-select ref="inst_select" v-model="institute"
                              :options="inst_options"
                              placeholder="Institute"
                              required
                />
              </div>
              <div class="form-group" v-on:focus="get_groups">
                <model-select ref="group_select" v-model="group"
                              :options="group_options"
                              placeholder="Group"
                              required/>
              </div>
              <div class="form-group">
                <input ref="snp_tbx"
                       v-model="snp"
                       class="form-control"
                       placeholder="Surname Name Patronymic"
                       required
                       type="text"/>
              </div>
              <button class="btn btn-black" type="submit">Let me in!</button>
            </form>
          </div>
        </div>
      </div>
    </center>
  </div>
</template>

<script>
import {ModelSelect} from 'vue-search-select'
import axios from 'axios';
import 'vue-search-select/dist/VueSearchSelect.css'

export default {
  name: "Initialize",
  components: {
    ModelSelect
  },
  data() {
    return {
      institute: null,
      group: null,
      snp: null,
      inst_options: [],
      group_options: []
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
        init: async function () {
          await axios({
            url: this.$store.state.api_host,
            withCredentials: true,
            method: 'POST',
            data: {
              method: 'initUser',
              snp: this.snp,
              group_id: this.group
            }
          }).then((response) => {
            if (response.data.status) {
              this.$store.dispatch("getUser").then(() => {
                this.$router.push('/');
              });
            } else {
              this.$toast.error(response.data.error);
            }
          }).catch((err) => {
            this.$toast.error(err.toString());
          })
        }
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

<style lang="scss" scoped>
.init-page {
  position: absolute;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
}

.component {
  width: 100%;
  margin-top: 50px;
}

.btn-black {
  background-color: #000 !important;
  color: #fff !important;
  width: 50%;
}
</style>