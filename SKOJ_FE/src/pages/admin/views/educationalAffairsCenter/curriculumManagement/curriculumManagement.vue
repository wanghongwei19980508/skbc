
<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Curriculum_Management')">
      <vTable ref="tableRef" :height="'calc(100vh -  ' + (280 + 47 * tableLength) + 'px)'" :tableColumn="tableColumn"
        :tableData="tableData" :tableTotal="tableTotal" :headerForm=headerForm :tableScope="tableScope"
        @tableChange="tableChange" @selectionChange="selectionChange">
        <template slot-scope="row" slot="enabledState">
          <el-switch v-model="row.row['enabledState']" active-value="1" inactive-value="2"
            @change="enabledStateChange(row.row)">
          </el-switch>
        </template>
      </vTable>
    </Panel>
  </div>
</template>
                
<script>
import api from "@admin/api";
import vTable from "@admin/components/vTable.vue"
import { curriculumManagementTableColumn, curriculumManagementHeaderForm } from './config.js'
import { mapGetters } from 'vuex'

export default {
  name: "curriculumManagement",
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
      tableColumn: curriculumManagementTableColumn,  // 表格页头
      headerForm: curriculumManagementHeaderForm, // 表格搜索栏
      tableScope: [
        {
          text: '编辑',
          handle: (scope) => {
            this.$router.push({
              name: "courseDetails",
              params: scope.row
            });
          }
        },
        {
          text: '删除',
          handle: (scope) => {
            console.log(scope);
          }
        },
      ]
    };
  },
  mounted() {
    this.configProperty() // 配置回调函数
    this.getTableData() // 获取数据
  },
  methods: {
    // 页码切换
    tableChange(obj) {
      this.tableTotal = obj
      if (!obj.noChange) this.getTableData()
    },
    // 获取数据
    getTableData() {
      this.tableData = [
        { courseTitle: '11', date: '2022-11-06T15:03:31.000Z', tableState: 'warning', source: 1 },
        { courseTitle: '12', date: '2022-11-06T15:03:31.000Z', grade: 1 },
        { courseTitle: '13', date: '2022-11-06T15:03:31.000Z' },
        { courseTitle: '14', date: '2022-11-06T15:03:31.000Z', tableState: 'primary' },
        { courseTitle: '15', date: '2022-11-06T15:03:31.000Z' },
        { courseTitle: '16', date: '2022-11-06T15:03:31.000Z' },
        { courseTitle: '17', date: '2022-11-06T15:03:31.000Z' },
        { courseTitle: '18', date: '2022-11-06T15:03:31.000Z' },
        { courseTitle: '19', date: '2022-11-06T15:03:31.000Z' }]
      this.tableTotal.total = 11
    },
    // 选择列表
    selectionChange(val) {
      this.multipleSelection = val;
    },
    // 配置回调函数
    configProperty() {
      this.headerForm[1][0].handle = (item) => {
        this.$router.push({
          name: "courseDetails",
        });
      }
      this.headerForm[1][1].handle = (item) => {
        if (this.multipleSelection.length) {
          this.$msgbox({
            title: '确认删除',
            type: "error",
            message: `是否删除这${this.multipleSelection.length}条数据`,
            showCancelButton: true,
            closeOnClickModal: true,
          }).then(res => {
            console.log('删除');
          }).catch(res => { });
        } else {
          this.$error('请选择要删除的数据')
        }
      }
    },
    // 启用停用
    enabledStateChange(row) {
      console.log(row);
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