<template>
  <div>
    <el-drawer :title="title" :visible.sync="drawer" :direction="direction" :before-close="handleClose" :size="width"
      style="z-index: 4000;">
      <div class="basicInformation">
        <div class="basicInformationHeard">
          <h3 class="info-detail-title">{{ searchData.class }}</h3>
          <div class="buttonBox">
            <el-button size="mini" :type="'success'" @click="adjust(searchData)">编辑课次</el-button>
            <el-button size="mini" :type="'success'" @click="audition(searchData)">删除课次</el-button>
          </div>
        </div>
        <vDescriptions class="searchInput" ref="searchSubmitForm" size="default" :searchData="searchData"
          :searchForm="searchForm" :title="'课次信息'" :column="2">
        </vDescriptions>
        <div class="basicInformationHeard">
          <h3 class="info-detail-title">上课学员</h3>
          <p>共{{ courseDetailsDrawerData.length }}名学员</p>
        </div>
        <el-button size="mini" :type="'success'" @click="audition(searchData)">添加临时学员</el-button>
        <p></p>
        <vTable :height="'400px'" :tableColumn="courseDetailsDrawerColumn" :tableData="courseDetailsDrawerData"
          :tableScope="courseDetailsDrawerScope" :tableTotal="{}">
        </vTable>
      </div>
    </el-drawer>
  </div>
</template>
      
<script>
import vDescriptions from "@admin/components/vDescriptions.vue"
import vTable from "@admin/components/vTable.vue"
import { courseDetailsDrawerForm, courseDetailsDrawerColumn } from "./config.js"

export default {
  name: 'courseDetailsDrawer',
  components: {
    vDescriptions,
    vTable
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    direction: {
      type: String,
      default: 'rtl'
    },
    drawer: {
      type: Boolean,
      default: false
    },
    width: {
      type: String,
      default: '45%'
    },
    searchData: {
      type: Object,
      default: () => { }
    }
  },
  data() {
    return {
      searchForm: courseDetailsDrawerForm,
      courseDetailsDrawerColumn: courseDetailsDrawerColumn,
      courseDetailsDrawerData: [],
      courseDetailsDrawerScope: [{
        text: '调整',
        handle: (scope) => {
        }
      }, {
        text: '请假',
        handle: (scope) => {
        }
      }]
    }
  },
  mounted() {
    this.configProperty() // 配置回调函数
  },
  methods: {
    // 关闭抽屉
    handleClose() {
      this.$emit('fromCancel', { label: 'courseDetailsDrawer' })
    },
    // 配置回调函数
    configProperty() {
      this.courseDetailsDrawerColumn[0].handle = (item) => {
        this.$router.push({
          name: "studentDetail",
        });
      }
    },
    // 编辑课次
    adjust(item) {
      // this.$emit('fromCancel', { label: 'courseDetailsDrawer', blon: true })
      this.$emit('adjust', item)
    }
  },
  watch: {

  },
  computed: {

  }
}
</script>
<style lang="less" scoped>
.basicInformation {
  padding: 0 20px;

  .basicInformationHeard {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .info-detail-title {
      overflow: hidden;
      text-overflow: ellipsis;
      -webkit-line-clamp: 1;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      width: calc(100% - 180px);
    }
  }
}
</style>
<style lang="less"></style>
    
      