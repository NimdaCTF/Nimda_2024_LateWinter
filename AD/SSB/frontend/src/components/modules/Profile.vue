<template>
  <div class="profile">
    <div class="upper-space">
      <StudentField class="student-field"></StudentField>
    </div>
    <div v-for="(item, idx) in items" :key="idx" class="middle-space">
      <Transition name="fade" mode="out-in" appear>
        <StudentCourse :title="item.name" dep="Кафедра рофлографии" :course-id="item.id"></StudentCourse>
      </Transition>
    </div>
  </div>
</template>

<script>
import StudentField from "./profile-src/StudentField";
import axios from "axios";
import StudentCourse from "@/components/modules/profile-src/StudentCourse";

export default {
  name: "Profile",
  components: {StudentCourse, StudentField},
  mounted() {
    this.getCurrentSubjects();
  },
  data() {
    return {
      "items": []
    }
  },
  methods: {
    getCurrentSubjects: async function () {
      await axios({
        url: this.$store.state.api_host + '?method=getCurrentSubjects&semester=' + 3,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        if (response.data.status) {
          this.items = response.data.values;
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })

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

.middle-space {
  width: 100%;
  padding-left: 50px;
  padding-right: 50px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}


</style>