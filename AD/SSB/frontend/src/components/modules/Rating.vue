<template>
  <keep-alive>
    <div class="rating">
      <select v-model="rating_choice" :disabled=working class="form-control form-control-lg selector">
        <option value="1">Group rating</option>
        <option value="2">Global rating</option>
      </select>
      <vue-table-dynamic ref="table" :params=params class="good-dark-table"></vue-table-dynamic>

    </div>
  </keep-alive>
</template>

<script>
import axios from "axios";

export default {
  name: "Rating",
  data() {
    return {
      rating_choice: 1,
      params: {
        data: [],
        header: 'row',
        border: false,
        columnWidth: [{column: 0, width: 60}],
        highlight: {column: [0, 1, 2]},
        highlightedColor: 'rgb(23, 23, 23)',
        scrollbar: 'hidden'

      },
      working: true
    }
  },
  methods: {
    getRating: async function () {
      this.working = true;
      let choice = "";
      switch (parseInt(this.rating_choice)) {
        case 1:
          choice = "getGroupRating";
          break;
        case 2:
          choice = "getGlobalRating";
          break;
        default:
          return;
      }

      this.ratingClear();

      await axios({
        url: this.$store.state.api_host + '?method=' + choice,
        withCredentials: true,
        method: 'GET'
      }).then((response) => {
        let vals = response.data.values || [];

        vals.forEach((item, i) => {
          this.params.data.push([i + 1, item.snp || item.username, item.average.toFixed(2)]);
        });
      }).catch((err) => {
        this.$toast.error(err.toString());
      })
      this.working = false;
    },
    ratingClear: function () {
      this.params.data = [['#', 'SNP', 'Average']];
    }
  },
  async mounted() {
    await this.getRating();
  },
  watch: {
    rating_choice: function () {
      this.getRating();
    }
  }
}
</script>

<style lang="scss" scoped>
//Colors
$default: #fff;
$background: #171717;

.rating {
  width: 100%;
  height: 100%;
  background-color: $background;
  color: $default;
}

.good-dark-table {
  margin-top: 10px;
  color: #C2C3C4 !important;
  font-size: 1.1em !important;
  z-index: -1;
}

.selector {
  background-color: inherit;
  outline: none;
  border: 0;
}
</style>