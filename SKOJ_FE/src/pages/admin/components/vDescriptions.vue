<template>
  <div class="demo-pagination-block">
    <el-descriptions class="margin-top" :title="title" :column="column" :size="size">
      <!-- :border="true" direction="vertical"  -->
      <!-- <template slot="extra">
        <el-button type="primary" size="small">操作</el-button>
      </template> -->
      <el-descriptions-item v-for="(item, index) in formList" :label="item.label" :key="index"
        label-class-name="my-label">
        <span v-if="item.filter">
          {{ item.filter && item.filter(searchData[item.prop]) }}
        </span>
        <span v-else>{{ searchData[item.prop] }}</span>
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>
<script>
export default {
  name: "vDescriptions",
  components: {
  },
  data() {
    return {
      formData: {}
    };
  },
  props: {
    title: {
      type: String,
      default: ""
    },
    size: {
      type: String,
      default: "medium"
    },
    searchForm: {
      type: Array,
      default: () => []
    },
    searchData: {
      type: Object,
      default: () => { }
    },
    column: {
      type: Number,
      default: 3
    }
  },
  mounted() {
  },
  computed: {
    formList() {
      let list = this.searchForm
      return list.flat()
    }
  },
  watch: {
  }
};
</script>
<style lang="less">
.my-label {
  // background: #b5e7d4 !important;
}
</style>