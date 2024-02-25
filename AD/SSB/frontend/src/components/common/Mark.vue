<template>
  <div class="mark" v-bind:class="defineMark">
    <span>{{mark}}</span>
  </div>
</template>

<script>
export default {
  name: "Mark",
  props: {
    mark: String
  },
  computed: {
    defineMark: function(){
      switch (this.mark){
        case "1":
          return 'worst';
        case "2":
          return 'bad';
        case "3":
          return 'passably';
        case "4":
          return 'good';
        case "5":
          return 'best';
        case "-":
          return 'worst';
        case "+":
          return 'best';
        default:
          return 'undefined';
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.mark {
  width: 30px;
  height: 30px;
  border-radius: 10px;
}

.mark span{
  width: inherit;
  height: inherit;
  font-size: 1.3em;
}

.worst{
  background-color: black;
  color: white;
}

.bad {
  background-color: darkred;
  color: whitesmoke;
}

.passably {
  background-color: darkorange;
  color: whitesmoke;
}

.good {
  background-color: dodgerblue;
  color: whitesmoke;
}

.best {
  background-color: green;
  color: whitesmoke;
}

.undefined {
  background-color: lightslategray;
  color: black;
}
</style>