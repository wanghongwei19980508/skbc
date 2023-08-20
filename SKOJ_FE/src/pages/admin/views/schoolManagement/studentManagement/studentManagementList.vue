<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Student_Management_List')">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="在读学员" name="studentInSchoolList">
          <studentInSchoolList v-if="activeName == 'studentInSchoolList'" ref="studentInSchoolList"></studentInSchoolList>
        </el-tab-pane>
        <el-tab-pane label="报读情况" name="applicationStatus">
          <applicationStatus v-if="activeName == 'applicationStatus'" ref="applicationStatus"></applicationStatus>
        </el-tab-pane>
        <el-tab-pane label="历史学员" name="historyStudent">
          <historyStudent v-if="activeName == 'historyStudent'" ref="historyStudent"></historyStudent>
        </el-tab-pane>
      </el-tabs>
    </Panel>
  </div>
</template>
  
<script>
import studentInSchoolList from './child/studentInSchoolList.vue'
import applicationStatus from './child/applicationStatus.vue'
import historyStudent from './child/historyStudent.vue'

export default {
  name: "studentManagementList",
  components: {
    studentInSchoolList,
    applicationStatus,
    historyStudent
  },
  data() {
    return {
      activeName: 'studentInSchoolList',
    };
  },
  mounted() {
    this.$refs['studentInSchoolList'].$refs['tableRef'].tableChange()
  },
  methods: {
    handleClick(tab, event) {
      setTimeout(() => {
        this.$refs[tab.name].$refs['tableRef'].tableChange()
      }, 10);
    }
  },
  watch: {
  },
};
</script>

<style lang="less" scoped>
.baseInfo {
  padding: 0 10px 0;
}
</style>