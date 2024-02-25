<template>
  <div class="c-view">
    <div class="c-header">
      <h1>{{ this.subject.name }}</h1>
      <h5>Преподаватель: {{ this.teacher.snp }}</h5>
      <h5>Кафедра: Кафедра рофлографии</h5>
    </div>
    <div class="c-body">
      <ol class="rounded">
        <li v-for="(item, idx) in this.tasks" :key="idx" v-bind:value="item"><a href="#" @click="gotoTaskView(item.id)">Практическая работа {{idx + 1}}. Тема: {{item.title}}</a></li>
      </ol>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TaskView from "@/components/common/TaskView";

export default {
  name: "CourseView",
  data() {
    return {
      "teacher_d": {},
      "subject_d": {},
      "tasks_d": []
    }
  },
  computed: {
    courseId: function () {
      return this.$store.state.viewCourseId;
    },
    teacher: function () {
      return this.teacher_d;
    },
    subject: function () {
      return this.subject_d;
    },
    tasks: function () {
      return this.tasks_d;
    }
  },
  methods: {
    getTeachers: async function () {
      await axios({
        url: this.$store.state.api_host + '?method=getTeacherByCourseId&id=' + this.courseId,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        if (response.data.status) {
          this.teacher_d = response.data;
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    },
    getSubject: async function () {
      await axios({
        url: this.$store.state.api_host + '?method=getSubjectById&id=' + this.courseId,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        if (response.data.status) {
          this.subject_d = response.data;
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    },
    getTasks: async function () {
      await axios({
        url: this.$store.state.api_host + '?method=getTasksBySubject&id=' + this.courseId,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        if (response.data.status) {
          console.log(response.data)
          this.tasks_d = response.data.values;
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    },
    gotoTaskView: function (taskId) {
      this.$store.state.taskId = taskId;
      this.$store.commit("change_module", TaskView);
    }

  },
  deactivated() {
    this.teacher_d = {};
    this.subject_d = {};
    this.tasks_d = [];
  },
  async activated() {
    await this.getTeachers();
    await this.getSubject();
    await this.getTasks();
  }
}
</script>

<style lang="scss" scoped>
$background: #171717;
$default: #fff;

.c-view {
  display: flex;
  flex-flow: column nowrap;
  width: 100%;
  height: 100%;
  background-color: $background;
  color: $default;
}

.c-header {
  margin-top: 20px;
}

.rounded {
  margin: 0 auto;
  margin-top: 100px;
  counter-reset: li;
  list-style: none;
  font: 14px "Trebuchet MS", "Lucida Sans";
  padding: 0;
  width: 50%;
  text-shadow: 0 1px 0 rgba(255, 255, 255, .5);
}

.rounded a {
  position: relative;
  display: block;
  padding: .4em .4em .4em 2em;
  margin: .5em 0;
  background: #DAD2CA;
  color: #444;
  text-decoration: none;
  border-radius: .3em;
  transition: .3s ease-out;
}

.rounded a:hover {
  background: #E9E4E0;
}

.rounded a:hover:before {
  transform: rotate(360deg);
}

.rounded a:before {
  content: counter(li);
  counter-increment: li;
  position: absolute;
  left: -1.3em;
  top: 50%;
  margin-top: -1.3em;
  background: #8FD4C1;
  height: 2em;
  width: 2em;
  line-height: 2em;
  border: .3em solid white;
  text-align: center;
  font-weight: bold;
  border-radius: 2em;
  transition: all .3s ease-out;
}

</style>