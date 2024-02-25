<template>
  <div class="task-view">
    <h1>{{task.title}}</h1>
    <div class="input-file">
      <div class="form-group">
        <input id="file" @change="uploadFile" class="input-file" name="file" type="file">
        <label class="btn btn-tertiary js-labelFile" for="file">
          <span class="js-fileName">Загрузить ответ</span>
        </label>
      </div>
      <a v-if="task.filename" @click="loadFile">Просмотреть загруженный ответ</a>
    </div>
  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "TaskView",
  data() {
    return {
      task: {}
    }
  },
  methods: {
    getTasks: async function () {
      await axios({
        url: this.$store.state.api_host + '?method=getTaskById&id=' + this.$store.state.taskId,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        if (response.data.status) {
          this.task = response.data;
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    },
    uploadFile: async function(event){
      const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });

      let file = await toBase64(event.target.files[0]);
      file = file.split(',')[1];

      await axios({
        url: this.$store.state.api_host,
        withCredentials: true,
        method: 'POST',
        data: {
          method: 'uploadFile',
          taskId: this.task.id,
          file: file,
          filename: event.target.files[0].name
        }
      }).then((response) => {
        if (response.data.status) {
          this.$toast.success('Sent!');
          this.getTasks();
        } else {
          this.$toast.error(response.data.error);
        }
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
    },
    loadFile: function (){
      window.open("http://localhost:8099/index.php?method=loadFile&id=" + this.task.id, '_blank');
    }
  },
  deactivated() {
    this.task = {};
  },
  async activated() {
    await this.getTasks();
    console.log(this.task)
  }
}
</script>

<style lang="scss" scoped>
$default: #fff;
$background: #171717;

.task-view {
  background-color: $background;
  color: $default;
  height: 100%;
  width: 100%;
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
}

.input-file .btn-tertiary {
  color: white;
  padding: 0;
  line-height: 40px;
  width: 300px;
  margin: auto;
  display: block;
  border: 2px solid white;
}

.input-file .btn-tertiary:hover, .input-file .btn-tertiary:focus {
  color: greenyellow;
  border-color: darkslategray;
}

.input-file .input-file {
  width: .1px;
  height: .1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1
}

.input-file .input-file + .js-labelFile {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 10px;
  cursor: pointer
}

.input-file .input-file + .js-labelFile .icon:before {
  content: "\f093"
}

.input-file .input-file + .js-labelFile.has-file .icon:before {
  content: "\f00c";
  color: white
}
</style>