<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Customer_List')">
      <vTable ref="tableRef" :height="'calc(100vh -  ' + (270 + 47 * tableLength) + 'px)'" :tableColumn="tableColumn"
        :tableData="tableData" :tableScope="tableScope" :tableTotal="tableTotal" :headerForm=headerForm
        @tableChange="tableChange" @selectionChange="selectionChange">
        <template slot-scope="row" slot="intention_level">
          <el-select v-model="row.row['intention_level']" :placeholder="'请选择'" :multiple="false"
            @change="intentionLevelChange(row)">
            <el-option v-for="(op, index) in intentionLevelList" :label="op.label" :value="op.value" :key="index"
              :disabled="op.disabled">{{
                op.label
              }}</el-option>
          </el-select>
        </template>
      </vTable>
    </Panel>
    <addCustomer ref="addCustomerDrawerRef" :searchData="addCustomerData" :drawer="addCustomerDrawer" :title="'新增客户'"
      @fromCancel="handleClose" />
    <followUpPopover :dialogVisible="followUpPopoverdialogVisible" :userData="userData"
      @closeFollowUpPopover="followUpPopoverdialogVisible = false" />
    <el-dialog :visible="batchImportVisible" :title="'批量导入'" :fullscreen="batchImportFullscreen"
      :close-on-click-modal="false" @close="batchImportVisible = false">
      <div slot="title">
        <h2>批量导入</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="batchImportFullscreen = !batchImportFullscreen"></el-button>
      </div>
      <div>
        <h4>1.下载导入模板，按要求填写信息</h4>
        <el-button size="small" type="primary" icon="el-icon-fa-upload" @click="downloadTemplate">下载学员信息导入模板</el-button>
        <h4>2.选择需要导入的Excel文件</h4>
        <el-upload class="upload-demo" action="/api/admin/upload_file" name="file" :data="batchImport"
          :on-success="uploadSuccess" :on-error="uploadError">
          <el-button size="small" type="primary">上传文件</el-button>
        </el-upload>
        <h4>3.选择数据重复时的操作方式</h4>
        <h5>注:数据重复判定规则：学员姓名和手机号与系统内已有的学员都相同，则为重复数据</h5>
        <el-radio-group v-model="batchImport.importMode">
          <el-radio :label="1">继续导入，并覆盖原信息</el-radio>
          <el-radio :label="2">终止导入，修改后重新上传</el-radio>
        </el-radio-group>
        <h4>4.添加备注</h4>
        <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="batchImport.remarks">
        </el-input>
        <h5>为导入的文件添加备注，便于在导入记录中查找</h5>
      </div>
    </el-dialog>
  </div>
</template>
    
<script>
import api from "@admin/api";
import vTable from "@admin/components/vTable.vue"
import addCustomer from "@admin/components/newCompent/addCustomer.vue"
import followUpPopover from "@admin/components/newCompent/followUpPopover.vue"
import { tableColumn, headerForm, intentionLevelList } from './config.js'
import { mapGetters } from 'vuex'

export default {
  name: "customerList",
  components: {
    vTable,
    addCustomer,
    followUpPopover
  },
  data() {
    return {
      followUpPopoverdialogVisible: false, // 新增跟进记录弹窗
      userData: {}, // 用户操作信息
      addCustomerDrawer: false, // 新增客户抽屉
      addCustomerData: {}, // 新增客户信息
      batchImportVisible: false, // 批量导入 dialog
      batchImportFullscreen: false, // 批量导入 全屏
      batchImport: { // 上传数据
        importMode: 1,
        remarks: ''
      },
      tableTotal: { // 页码
        total: null,
        currentPage: 1,
        pageSize: 10
      },
      tableData: [], // 数据
      multipleSelection: [], // 勾选数据
      tableColumn: tableColumn,  // 表格页头
      headerForm: headerForm, // 表格搜索栏
      tableScope: [{
        text: '跟进',
        handle: (scope) => {
          this.userData = scope.row
          this.followUpPopoverdialogVisible = true
        }
      }, {
        text: '试听',
        handle: (scope) => {
          this.$router.push({
            name: "timeSchedule",
            params: scope
          });
        }
      }, {
        text: '报名',
        handle: (scope) => {

        }
      }],
      intentionLevelList: intentionLevelList, // 意向级别
    };
  },
  mounted() {
    this.$refs['tableRef'].tableChange()
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
      api.getClueList(this.tableTotal).then((res) => {
        this.tableData = res.data.data.results
        this.tableTotal.total = res.data.data.total
      })
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
      tableColumn[0].handle = (scope) => {
        this.$router.push({
          name: "studentDetail",
          params: scope.row
        });
      }
      headerForm[2][0].handle = (scope) => {
        this.addCustomerDrawer = true
      }
      headerForm[2][1].handle = (scope) => {
        this.batchImportVisible = true
      }
      headerForm[2][2].handle = (scope) => {
        console.log(this.multipleSelection);
      }
    },
    // 关闭抽屉
    handleClose(row) {
      if (row.showPopover) {
        this.$confirm('确认关闭？').then(_ => {
          this.addCustomerDrawer = false
          this.$refs['addCustomerDrawerRef'].$refs['searchSubmitForm'].$refs['searchFormRef'].resetFields()
        }).catch(_ => { });
      } else {
        this.addCustomerDrawer = false
        this.$refs['addCustomerDrawerRef'].$refs['searchSubmitForm'].$refs['searchFormRef'].resetFields()
        this.$refs['tableRef'].tableChange()
      }
    },
    // 选择意向级别
    intentionLevelChange(row) {
      api.editClue(row.row).then((res) => { })
    },
    // 下载学员信息导入模板
    downloadTemplate() {
      console.log(111);
    },
    // 上传成功
    uploadSuccess(response) {
      if (response.error) {
        this.$error(response.data);
        return;
      }
    },
    // 上传失败
    uploadError() {
      this.$error(this.$i18n.t('m.Upload_Failed'));
    },
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
  padding: 10px 20px 0;
}
</style>