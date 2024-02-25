<template>
  <div class="book">
    <div class="block-search">
      <input type="text" placeholder="Subject name or teacher name" v-model="search">
      <select v-model="semester_selected" @change="routine">
        <option v-for="(item, idx) in semesters" :key="idx" v-bind:value="item">{{item}} semester</option>
      </select>
    </div>
    <div class="s-blocks">
      <div v-for="(item, idx) in items" :key="idx">
        <SubjectBlock :name=item.name :teacher=item.teacher :mark=item.mark :id=item.id :type=item.pass_type></SubjectBlock>
      </div>
    </div>
  </div>
</template>

<script>
import SubjectBlock from "@/components/modules/book-src/SubjectBlock";
import axios from "axios";

export default {
  name: "Book",
  components: {SubjectBlock},
  data() {
    return {
      "true_items": [],
      "items": [],
      "semesters": [],
      "semester_selected": 0,
      "search": ""
    }
  },
  methods: {
    getMarks: async function (){
      let _ = null;
      await axios({url: this.$store.state.api_host + '?method=getStudentMarks', withCredentials: true, method: 'POST'}).then((response) => {
        _ = response.data.values;
      })

      return _
    },
    getSubjects: async function(){
      let _ = null;
      await axios({url: this.$store.state.api_host + '?method=getGroupSubjects', withCredentials: true, method: 'POST'}).then((response) => {
          _ = response.data.values;
      })

      return _;
    },
    getMarkBySubject: function(marks, subject_id){
      let _res = null;
      marks.forEach((item) => {
        if (item.subject_id === subject_id){
          _res = item.mark;
        }
      });

      return _res;
    },
    routine: async function(){
      this.true_items = [];
      let mark = await this.getMarks();
      let subjects = await this.getSubjects();

      subjects.forEach((item) => {
        if (!this.semesters.includes(item.semester))
          this.semesters.push(item.semester);
      });
      if (this.semester_selected === 0)
        this.semester_selected = this.semesters[0];
      if (this.semester_selected)
        subjects.forEach((item) => {
          if (item.semester === this.semester_selected)
            this.true_items.push({
              'name': item.name,
              'teacher': item.t_snp,
              'mark': this.getMarkBySubject(mark, item.id),
              'pass_type': item.pass_type
            });
        })

      this.items = this.true_items;
    }
  },
  async created() {
    await this.routine();
  },
  watch: {
    search: function (value) {
      this.items = [];
      if (value === ""){
        this.$nextTick(() => this.items = this.true_items);
        return;
      }
      this.true_items.forEach((item) => {
        if (item.name.toLowerCase().startsWith(value.trim().toLowerCase()) || item.teacher.toLowerCase().includes(value.trim().toLowerCase())){
          this.items.push(item);
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
//Colors
$default: #fff;
$background: #171717;

.book {
  width: 100%;
  height: 100%;
  background-color: $background;
  color: $default;
}

.s-blocks {
  display: flex;
  align-items: flex-start;
  flex-flow: row wrap;
  justify-content: center;
  background-color: inherit;
}


.block-search input {
  background: rgba(23, 23, 23, .6);
  border: none;
  border-bottom: 1px solid #fff;
  color: #fff;
  font-family: 'Caveat', sans-serif;
  font-size: 20px;
  letter-spacing: 1px;
  padding: 10px 0;
  outline: none;
  width: 100%;
}
.block-search select {
  background: rgba(23, 23, 23, .6);
  border: none;
  border-bottom: 1px solid #fff;
  color: #fff;
  font-family: 'Caveat', sans-serif;
  font-size: 20px;
  letter-spacing: 1px;
  padding: 10px 0;
  outline: none;
  width: 100%;
}
</style>