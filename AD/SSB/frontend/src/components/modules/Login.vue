<template>
    <div>
        <div class="sidenav">
            <div class="login-main-text">
                <h2>{{app_name}}<br> Login Page</h2>
                <p>{{login_page_description}}</p>
            </div>
        </div>
        <div class="main">
            <div class="btn-group switcher" role="group">
                <button type="button" @click="changeModule('institute')" class="btn btn-default"
                        v-bind:class="{'switcher_active': computeModule[1] === 0}">Institute
                </button>
                <button type="button" @click="changeModule('special_login')" class="btn btn-default"
                        v-bind:class="{'switcher_active': computeModule[1] === 1}">Special
                </button>
            </div>
          <component v-bind:is="computeModule[0]"></component>
            <a style="margin-top: 10px" href="#" v-on:click="changeModule('special_signup')" v-if="computeModule[1] !== 2">Sign
                UP</a>

        </div>
    </div>
</template>

<script>

    import InstituteLogin from "@/components/modules/login-src/InstituteLogin";
    import SpecialLogin from "@/components/modules/login-src/SpecialLogin";
    import SignUpSpecial from "@/components/modules/sign-up-src/SignUpSpecial";

    export default {
        name: "Login",
        components: {SignUpSpecial, SpecialLogin, InstituteLogin},
        data() {
            return {
                choice: 0,
                app_name: "SSB",
                login_page_description: "Make world better!"
            }
        },
      methods: {
          changeModule: function (moduleName){
            if (moduleName === "institute"){
              this.$store.commit('change_login_module', InstituteLogin)
              return;
            }
            if (moduleName === 'special_login'){
              this.$store.commit('change_login_module', SpecialLogin)
              return;
            }
            if (moduleName === 'special_signup')
              this.$store.commit('change_login_module', SignUpSpecial)
          }
      },
        computed: {
          computeModule: function (){
            return this.$store.state.current_login_module;
          }
        }
    }


</script>
<style scoped>
    .switcher_active {
        background-color: darkseagreen;
    }

    .switcher {
        margin-top: 40%;
        margin-bottom: 5%;
    }

    @media screen and (max-width: 450px) {
        .switcher {
            margin-top: 10%;
        }

    }

    @media (max-width: 768px) {
        .switcher {
            margin-top: 5%;
        }
    }

    body {
        font-family: "Lato", sans-serif;
    }


    .sidenav {
        height: 100%;
        background-color: #000;
        overflow: hidden;
        padding-top: 20px;
    }


    .main {
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;
        margin-top: -12%;
        padding: 0 10px;
        overflow: hidden;
    }

    @media (max-width: 768px) {
        .sidenav {
            padding-top: -10%;
            margin-top: -10%;
        }

        .main {
            margin-top: 0 !important;
        }

    }


    @media screen and (min-width: 768px) {
        .main {
            margin-left: 40%;
        }

        .sidenav {
            width: 40%;
            position: fixed;
            z-index: 1;
            top: 0;
            left: 0;
        }

    }


    .login-main-text {
        margin-top: 20%;
        padding: 60px;
        color: #fff;
    }

    .login-main-text h2 {
        font-weight: 300;
    }

    a {
        text-decoration: none;
    }


</style>