<template>
  <div class="s-field">
    <img src="../../../assets/empty_avatar.png">
    <div>
      <a v-if="user.name && user.surname" @click="gotoUser">{{ user.name}}<br>{{ user.surname}}</a>
      <a v-else @click="gotoUser">{{ user.username }}</a>
      <hr color="white">
    </div>
  </div>
</template>

<script>
import User from "@/components/common/User";

export default {
  name: "StudentField",
  props: {
    editable: Boolean || false
  },
  data() {
    return {
      user: {
        'name': 'none',
        'surname': 'none'
      },
      userName: null,
      userSurName: null,
      userPatronymic: null,
      snpChanged: false
    }
  },
  created() {
    this.getUser();
  },
  methods: {
    getUser: function () {
      this.$store.dispatch('getUser').then(() => {
        this.user = this.$store.state.user;
        this.userName = this.user.name;
        this.userSurName = this.user.surname;
        this.userPatronymic = this.user.patronymic;
      });
    },
    isSnpChanged: function () {
      this.snpChanged = this.userName !== this.user.name && this.userSurName !== this.user.surname && this.userPatronymic !== this.user.patronymic;
    },
    gotoUser: function (){
      this.$store.commit("change_module", User);
    }

  },
  watch: {
    userName: function () {
      this.isSnpChanged();
    },
    userSurName: function () {
      this.isSnpChanged();
    },
    userPatronymic: function () {
      this.isSnpChanged();
    }
  }
}
</script>

<style scoped>
.s-field {
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
}

.s-field img {
  width: 100px;
  height: 100px;
}

.s-field a {
  margin-top: 0.5em;
}

.snp-mutable {
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
}

.snp-mutable input {
  background: inherit;
  outline: none;
  border-radius: 10px;
  color: whitesmoke;
  text-align: center;
  margin-top: 5px;
}

.snp-mutable button {
  margin-top: 10px;
}

</style>