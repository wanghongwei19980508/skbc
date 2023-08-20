
<template>
  <div class="baseInfo">
    <vTable ref="tableRef" :height="'calc(100vh -  ' + (320 + 47 * tableLength) + 'px)'" :tableColumn="tableColumn"
      :tableData="tableData" :tableTotal="tableTotal" :headerForm=headerForm :tableScope="tableScope"
      @tableChange="tableChange" @selectionChange="selectionChange">
    </vTable>
  </div>
</template>
              
<script>
import api from "@admin/api";
import vTable from "@admin/components/vTable.vue"
import { historyStudentTableColumn, historyStudentHeaderForm } from './../config.js'
import { mapGetters } from 'vuex'

export default {
  name: "historyStudent",
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
      multipleSelection: [], // 勾选数据
      tableColumn: historyStudentTableColumn,  // 表格页头
      // 表格操作
      headerForm: historyStudentHeaderForm, // 表格搜索栏
      tableScope: [{
        text: '修改',
        handle: (scope) => {
          this.$router.push({
            name: "addCustomer",
            params: { item: scope.row },
          });
        }
      }, {
        text: '试听',
        handle: (scope) => {

        }
      }, {
        text: '删除',
        handle: (scope) => {
          api.editAssignment(scope.row.id).then((res) => {
          }).catch(() => { });
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
        { name: '11', age: '2022-11-06T15:03:31.000Z', tableState: 'warning', source: 1 },
        { name: '12', age: '2022-11-06T15:03:31.000Z', grade: 1 },
        { name: '13', age: '2022-11-06T15:03:31.000Z' },
        { name: '14', age: '2022-11-06T15:03:31.000Z', tableState: 'primary' },
        { name: '15', age: '2022-11-06T15:03:31.000Z' },
        { name: '16', age: '2022-11-06T15:03:31.000Z' },
        { name: '17', age: '2022-11-06T15:03:31.000Z' },
        { name: '18', age: '2022-11-06T15:03:31.000Z' },
        { name: '19', age: '2022-11-06T15:03:31.000Z' }]
      this.tableTotal.total = 11
    },
    // 返回上一页
    goBack() {
      this.$router.go(-1);
    },
    // 选择列表
    selectionChange(val) {
      this.multipleSelection = val;
      console.log(this.multipleSelection);
    },
    // 配置回调函数
    configProperty() {
      this.tableColumn[0].handle = (item) => {
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