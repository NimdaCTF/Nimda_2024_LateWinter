<template>
  <div class="s-page">
    <h1>{{ this.props.name }}</h1>
    <hr>
    <vue-table-dynamic style="color: #C2C3C4;" :params=params class="good-dark-table" ref="table"></vue-table-dynamic>
  </div>
</template>

<script>
export default {
  name: "SubjectPage",
  data(){
    return {
      props: {
        'subject_id': '',
        'name': ''
      },
      params: {
        data: [['#', 'SNP', 'Average']],
        header: 'row',
        border: false,
        columnWidth: [{column: 0, width: 60}],
        highlight: { column: [0,1,2] },
        highlightedColor: 'rgb(23, 23, 23)'
      }
    }
  },
  methods: {
    getProps: function (){
      this.props.name = this.$store.state.current_module_params.name;
      this.props.subject_id = this.$store.state.current_module_params.subject_id;
    }
  },
  mounted() {
    this.getProps();
  }
}
</script>

<style lang="scss" scoped>
.s-page{
  color: #C2C3C4 !important;
  background-color: #171717;
}
</style>