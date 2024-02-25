<template>
  <div class="profile">
    <div class="upper-space">
      <StudentField :editable="isUserSNPed" class="student-field"></StudentField>
    </div>
    <div class="items">
    <ChangePassword></ChangePassword>
    </div>
  </div>
</template>

<script>
import StudentField from "@/components/modules/profile-src/StudentField";
import ChangePassword from "@/components/modules/settings-src/ChangePassword";

export default {
  name: "Settings",
  components: {ChangePassword, StudentField},
  computed: {
    isUserSNPed: function (){
      return !this.$store.state.user.name || !this.$store.state.user.surname;
    }
  }
}
</script>

<style lang="scss" scoped>
//Colors
$default: #fff;
$background: #171717;

.profile {
  display: flex;
  flex-flow: column nowrap;
  width: 100%;
  height: 100%;
  background-color: $background;
  color: $default;
}

.upper-space {
  margin-top: 10px;
}

.items {
  display: flex;
  align-items: flex-start;
  flex-flow: row wrap;
  justify-content: center;
}

</style>