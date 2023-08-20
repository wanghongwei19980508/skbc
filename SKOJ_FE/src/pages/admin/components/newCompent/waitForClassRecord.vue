
<template>
  <div class="baseInfo">
    <vTable ref="tableRef" :height="'calc(100vh -  ' + (400 + 47 * tableLength) + 'px)'" :tableColumn="tableColumn"
      :selectionShow="false" :tableData="tableData" :tableTotal="tableTotal" :tableScope="tableScope"
      @tableChange="tableChange">
    </vTable>
    <el-dialog :visible.sync="changeCourseVisible" title="选择调入的课次">
      <el-table ref="multipleTable" :data="changeCourseList" tooltip-effect="dark"
        @selection-change="handleSelectionChange" style="height:400px;overflow-y: auto;">
        <el-table-column type="selection" width="55">
        </el-table-column>
        <el-table-column label="班级名称">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="授课课程">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="上课时间">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="上课教室">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="上课老师">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="人数">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="容量">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
      </el-table>
      <div slot="footer">
        <el-button @click="changeCourse">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import api from "@admin/api";
import vTable from "@admin/components/vTable.vue"
import { waitForClassRecordTableColumn } from './config.js'
import { mapGetters } from 'vuex'

export default {
  name: "waitForClassRecord",
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
      chooseCourseData: [], // 选择调课数据
      changeCourseList: [], // 调课列表
      tableColumn: waitForClassRecordTableColumn,  // 表格页头
      changeCourseVisible: false, // 调课 dialog
      multipleSelection: [], // 调课选择
      tableScope: [{
        text: '调课',
        type: 'text',
        handle: (scope) => {}
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
      this.tableData = this.changeCourseList = [
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
    // 确认调课
    changeCourse() {
      this.changeCourseVisible = false
      console.log('确认调课');
    },
    // 调课内容选择
    handleSelectionChange(val) {
      if (val.length > 1) {
        this.$refs.multipleTable.clearSelection()
        this.$refs.multipleTable.toggleRowSelection(val.pop())
      } else {
        this.multipleSelection = val
      }
    },
    // 配置回调函数
    configProperty() {
      this.tableScope[0].handle = (scope) => {
        this.chooseCourseData = scope.row
        this.changeCourseVisible = true
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