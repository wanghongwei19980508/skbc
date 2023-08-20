
<template>
  <div class="baseInfo">
    <vTable ref="tableRef" :height="'calc(100vh -  ' + (200 + 47 * tableLength) + 'px)'" :tableColumn="tableColumn" :selectionShow="false"
      :tableData="tableData" :tableTotal="tableTotal" :tableScope="tableScope" :headerForm=headerForm
      @tableChange="tableChange">
    </vTable>
  </div>
</template>
<script>
import api from "@admin/api";
import vTable from "@admin/components/vTable.vue"
import { classRecordTableColumn, classRecordHeaderForm } from './config.js'
import { mapGetters } from 'vuex'

export default {
  name: "classRecord",
  components: {
    vTable,
  },
  data() {
    return {
      tableTotal: { // 页码
        total: null,
        currentPage: 1,
        pageSize: 10
      },
      tableData: [], // 数据
      tableColumn: classRecordTableColumn,  // 表格页头
      headerForm: classRecordHeaderForm, // 表格搜索栏
      tableScope: [{
        text: '点名详情',
        type: 'text',
        handle: (scope) => {
        }
      }],
    };
  },
  mounted() {
    this.configProperty() // 配置回调函数
  },
  methods: {
    // 页码切换
    tableChange(obj) {
      this.tableTotal = obj
      if (!obj.noChange) this.getTableData()
      this.$store.commit('tableLength', this.$refs['tableRef'].headerFormList.length)
    },
    // 获取数据
    getTableData() {
      this.tableData = [
        { name: '11', date: '2022-11-06T15:03:31.000Z', tableState: 'warning', source: 1 },
        { name: '12', date: '2022-11-06T15:03:31.000Z', grade: 1 },
        { name: '13', date: '2022-11-06T15:03:31.000Z' },
        { name: '14', date: '2022-11-06T15:03:31.000Z', tableState: 'primary' },
        { name: '15', date: '2022-11-06T15:03:31.000Z' },
        { name: '16', date: '2022-11-06T15:03:31.000Z' },
        { name: '17', date: '2022-11-06T15:03:31.000Z' },
        { name: '18', date: '2022-11-06T15:03:31.000Z' },
        { name: '19', date: '2022-11-06T15:03:31.000Z' }]
      this.tableTotal.total = 11
    },
    // 返回上一页
    goBack() {
      this.$router.go(-1);
    },
    // 配置回调函数
    configProperty() {
      this.headerForm[3][0].handle = (item) => {
        this.$router.push({
          name: "studentDetail",
        });
      }
    }
  },
  watch: {
  },
  computed: {
    ...mapGetters(['tableLength']),
  }
};
</script>
              
<style lang="less" scoped>
.baseInfo {
  padding: 10px 10px 0;
}
</style>