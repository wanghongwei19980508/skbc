<template>
  <div class="view">
    <Panel>
      <div slot="title">
        <el-page-header @back="goBack" :content="this.$i18n.t('m.Contest_Objective_Problem_List')"
          style="margin-top: 5px">
        </el-page-header>
      </div>
      <div slot="header">
        <el-input v-model="objectiveProblemKeyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="objectiveProblemLoading" element-loading-text="loading" ref="objectiveProblemTable"
        :data="objectiveProblemList" @row-dblclick="handleDblclick" style="width: 100%">
        <el-table-column width="100" prop="id" label="ID"> </el-table-column>
        <el-table-column width="150" :label="$t('m.Display_ID')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row._id }}</span>
            <el-input v-show="row.isEditing" v-model="row._id"
              @keyup.enter.native="handleInlineEdit('objectiveProblem', row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row.title }}</span>
            <el-input v-show="row.isEditing" v-model="row.title"
              @keyup.enter.native="handleInlineEdit('objectiveProblem', row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="created_by.username" :label="$t('m.Author')">
        </el-table-column>
        <el-table-column width="200" prop="create_time" :label="$t('m.Create_Time')">
          <template slot-scope="scope">
            {{ scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column width="100" prop="visible" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text=""
              @change="updateObjectiveProblemList(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('m.Operation')" width="250">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit"
              @click.native="goEdit('objectiveProblem', scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Make_Public')" icon="clone"
              @click.native="makeContestObjectiveProblemPublic(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_Problem')"
              @click.native="deleteObjectiveProblem(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreateObjectiveProblem" icon="el-icon-plus">{{
          $t('m.Create') }}
        </el-button>
        <el-button type="primary" size="small" icon="el-icon-plus" @click="addObjectiveProblemDialogVisible = true">{{
          $t('m.Add_From_Public_Problem') }}
        </el-button>
        <el-pagination class="page" layout="prev, pager, next" @current-change="objectiveProblemCurrentChange"
          :page-size="pageSize" :total="objectiveProblemTotal">
        </el-pagination>
      </div>
    </Panel>
    <Panel :title="this.$i18n.t('m.Problem_List')">
      <div slot="header">
        <el-input v-model="problemKeyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="problemLoading" element-loading-text="loading" ref="problemTable" :data="problemList"
        @row-dblclick="handleDblclick" style="width: 100%">
        <el-table-column width="100" prop="id" label="ID"> </el-table-column>
        <el-table-column width="150" :label="$t('m.Display_ID')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row._id }}</span>
            <el-input v-show="row.isEditing" v-model="row._id" @keyup.enter.native="handleInlineEdit('problem', row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row.title }}</span>
            <el-input v-show="row.isEditing" v-model="row.title" @keyup.enter.native="handleInlineEdit('problem', row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="created_by.username" :label="$t('m.Author')">
        </el-table-column>
        <el-table-column width="200" prop="create_time" :label="$t('m.Create_Time')">
          <template slot-scope="scope">
            {{ scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column width="100" prop="visible" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text="" @change="updateProblem(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('m.Operation')" width="250">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEdit('problem', scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Make_Public')" icon="clone" @click.native="makeProblemPublic(scope.row.id)"></icon-btn>
            <icon-btn icon="download" :name="$t('m.Download_Test_Case')"
              @click.native="downloadTestCase(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_Problem')" @click.native="deleteProblem(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreateProblem" icon="el-icon-plus">{{ $t('m.Create') }}
        </el-button>
        <el-button type="primary" size="small" icon="el-icon-plus" @click="addProblemDialogVisible = true">{{
          $t('m.Add_From_Public_Problem') }}
        </el-button>
        <el-pagination class="page" layout="prev, pager, next" @current-change="problemCurrentChange"
          :page-size="pageSize" :total="problemTotal">
        </el-pagination>
      </div>
    </Panel>
    <el-dialog :title="$t('m.Sure_To_Update_The_Public_Topic')" width="20%" :visible.sync="InlineEditDialogVisible"
      @close-on-click-modal="false">
      <div>
        <p>{{ $t('m.Display_ID') }}: {{ currentRow._id }}</p>
        <p>{{ $t('m.Title') }}: {{ currentRow.title }}</p>
      </div>
      <span slot="footer">
        <cancel
          @click.native="InlineEditDialogVisible = false; currentRow.routeName === 'objectiveProblem' ? getObjectiveProblemList(objectiveProblemCurrentPage) : getProblemList(problemCurrentPage);">
        </cancel>
        <save
          @click.native=" currentRow.routeName === 'objectiveProblem' ? updateObjectiveProblemList(currentRow) : updateProblem(currentRow) ">
        </save>
      </span>
    </el-dialog>
    <el-dialog :title=" $t('m.Add_Contest_Problem') " width="80%" :visible.sync=" addProblemDialogVisible "
      @close-on-click-modal=" false ">
      <add-problem-component :contestID=" contestId " @on-change=" getProblemList "></add-problem-component>
    </el-dialog>
    <el-dialog title="Add Contest Objective Problem" width="80%" :visible.sync=" addObjectiveProblemDialogVisible "
      @close-on-click-modal=" false ">
      <add-objective-problem-component :contestID=" contestId "
        @on-change=" getObjectiveProblemList "></add-objective-problem-component>
    </el-dialog>
  </div>
</template>
    
<script>
import api from "../../api.js";
import utils from "@/utils/utils";
import AddObjectiveProblemComponent from "./AddPublicObjectiveProblem.vue";
import AddProblemComponent from "./AddPublicProblem.vue";
export default {
  name: "PublicTopicList",
  components: {
    AddObjectiveProblemComponent,
    AddProblemComponent,
  },
  data() {
    return {
      pageSize: 10,
      objectiveProblemTotal: 0,
      problemTotal: 0,
      objectiveProblemList: [],
      problemList: [],
      objectiveProblemKeyword: "",
      problemKeyword: "",
      objectiveProblemLoading: false,
      problemLoading: false,
      objectiveProblemCurrentPage: 1,
      problemCurrentPage: 1,
      contestId: "",
      currentRow: {},
      InlineEditDialogVisible: false,
      addObjectiveProblemDialogVisible: false,
      addProblemDialogVisible: false,
    };
  },
  mounted() {
    this.contestId = this.$route.params.contestId;
    this.contestTitle = this.$route.params.contestTitle;
    this.getObjectiveProblemList(this.objectiveProblemCurrentPage);
    this.getProblemList(this.problemCurrentPage);
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    handleDblclick(row) {
      row.isEditing = true;
    },
    goEdit(routeName, id) {
      if (routeName === "objectiveProblem") {
        this.$router.push({
          name: "edit-contest-objective-problem",
          params: { objectiveProblemId: id, contestId: this.contestId },
        });
      } else if (routeName === "problem") {
        this.$router.push({
          name: "edit-contest-problem",
          params: { problemId: id, contestId: this.contestId },
        });
      }
    },
    goCreateObjectiveProblem() {
      this.$router.push({
        name: "create-contest-objective-problem",
        params: { contestId: this.contestId },
      });
    },
    goCreateProblem() {
      this.$router.push({
        name: "create-contest-problem",
        params: { contestId: this.contestId },
      });
    },
    // 切换页码回调
    objectiveProblemCurrentChange(page) {
      this.objectiveProblemCurrentPage = page;
      this.getObjectiveProblemList(page);
    },
    problemCurrentChange(page) {
      this.problemCurrentPage = page;
      this.getObjectiveProblemList(page);
    },
    getObjectiveProblemList(page = 1) {
      this.objectiveProblemLoading = true;
      let params = {
        limit: this.pageSize,
        offset: (page - 1) * this.pageSize,
        keyword: this.objectiveProblemKeyword,
        contest_id: this.contestId,
      };
      api["getContestObjectiveProblemList"](params).then((res) => {
        this.objectiveProblemLoading = false;
        this.objectiveProblemTotal = res.data.data.total;
        for (let objectiveProblem of res.data.data.results) {
          objectiveProblem.isEditing = false;
        }
        this.objectiveProblemList = res.data.data.results;
      }, (res) => {
        this.objectiveProblemLoading = false;
      });
    },
    getProblemList(page = 1) {
      this.problemLoading = true;
      let params = {
        limit: this.pageSize,
        offset: (page - 1) * this.pageSize,
        keyword: this.problemKeyword,
        contest_id: this.contestId,
      };
      api["getContestProblemList"](params).then((res) => {
        this.problemLoading = false;
        this.problemTotal = res.data.data.total;
        for (let problem of res.data.data.results) {
          problem.isEditing = false;
        }
        this.problemList = res.data.data.results;
      }, (res) => {
        this.problemLoading = false;
      });
    },
    deleteObjectiveProblem(id) {
      this.$confirm(this.$i18n.t('m.Sure_To_Delete_This_Problem') + '?' + this.$i18n.t('m.The_Associated_Submissions_Will_Be_Deleted_As_Well'), this.$i18n.t('m.Delete_Objective_Problem'), { type: "warning", }).then(() => {
        api['deleteContestObjectiveProblem'](id).then(() => [
          this.getObjectiveProblemList(this.objectiveProblemCurrentPage - 1)
        ]).catch()
      }, () => { });
    },
    deleteProblem(id) {
      this.$confirm(this.$i18n.t('m.Sure_To_Delete_This_Problem') + '?' + this.$i18n.t('m.The_Associated_Submissions_Will_Be_Deleted_As_Well'), this.$i18n.t('m.Delete_Problem'), { type: "warning", }).then(() => {
        api["deleteContestProblem"](id).then(() => [
          this.getProblemList(this.problemCurrentPage - 1)
        ]).catch(() => { });
      }, () => { });
    },
    makeContestObjectiveProblemPublic(objectiveProblemID) {
      this.$prompt(this.$i18n.t('m.Please_Input_Display_Id_For_The_Public_Objective_Problem'), this.$i18n.t('m.Confirm')).then(({ value }) => {
        api.makeContestObjectiveProblemPublic({ id: objectiveProblemID, display_id: value, }).catch()
      }, () => { });
    },
    makeProblemPublic(problemID) {
      this.$prompt(this.$i18n.t('m.Please_Input_Display_Id_For_The_Public_Problem'), this.$i18n.t('m.Confirm')).then(({ value }) => {
        api.makeContestProblemPublic({ id: problemID, display_id: value }).catch();
      }, () => { });
    },
    updateObjectiveProblemList(row) {
      let data = Object.assign({ contest_id: this.contestId }, row);
      api["editContestObjectiveProblem"](data).then((res) => {
        this.InlineEditDialogVisible = false;
        this.getObjectiveProblemList(this.objectiveProblemCurrentPage);
      }).catch(() => {
        this.InlineEditDialogVisible = false;
      });
    },
    updateProblem(row) {
      let data = Object.assign({ contest_id: this.contestId }, row);
      api['editContestProblem'](data).then((res) => {
        this.InlineEditDialogVisible = false;
        this.getProblemList(this.problemCurrentPage);
      }).catch(() => {
        this.InlineEditDialogVisible = false;
      });
    },
    handleInlineEdit(routeName, row) {
      this.currentRow = Object.assign({ routeName: routeName }, row)
      this.InlineEditDialogVisible = true;
    },
    downloadTestCase(problemID) {
      let url = "/admin/test_case?problem_id=" + problemID;
      utils.downloadFile(url);
    },
  },
  watch: {
    $route(newVal, oldVal) {
      this.contestId = newVal.params.contestId;
      this.getObjectiveProblemList(this.objectiveProblemCurrentPage);
      this.getProblemList(this.problemCurrentPage);
    },
    objectiveProblemKeyword() {
      this.objectiveProblemCurrentChange();
    },
    problemKeyword() {
      this.problemCurrentChange();
    },
  },
};
</script>
    
<style scoped lang="less"></style>
    