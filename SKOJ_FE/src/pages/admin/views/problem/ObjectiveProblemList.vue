<template>
  <div class="view">
    <Panel :title="this.$i18n.t('m.Objective_Problem_List')">
      <div slot="title" v-if="contestId">
        <el-page-header @back="goBack" :content="this.$i18n.t('m.Contest_Objective_Problem_List')"
          style="margin-top: 5px">
        </el-page-header>
      </div>
      <div slot="header">
        <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="objectiveProblemList"
        @row-dblclick="handleDblclick" style="width: 100%">
        <el-table-column width="100" prop="id" label="ID"> </el-table-column>
        <el-table-column width="150" :label="$t('m.Display_ID')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row._id }}</span>
            <el-input v-show="row.isEditing" v-model="row._id" @keyup.enter.native="handleInlineEdit(row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row.title }}</span>
            <el-input v-show="row.isEditing" v-model="row.title" @keyup.enter.native="handleInlineEdit(row)">
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
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEdit(scope.row.id)"></icon-btn>
            <icon-btn v-if="contestId" :name="$t('m.Make_Public')" icon="clone"
              @click.native="makeContestObjectiveProblemPublic(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_Problem')"
              @click.native="deleteObjectiveProblem(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreateObjectiveProblem" icon="el-icon-plus">{{ $t('m.Create') }}
        </el-button>
        <el-button v-if="contestId" type="primary" size="small" icon="el-icon-plus"
          @click="addProblemDialogVisible = true">Add From Public Problem
        </el-button>
        <el-pagination class="page" layout="prev, pager, next" @current-change="currentChange" :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
    <el-dialog title="Sure to update the Objective problem? " width="20%" :visible.sync="InlineEditDialogVisible"
      @close-on-click-modal="false">
      <div>
        <p>DisplayID: {{ currentRow._id }}</p>
        <p>Title: {{ currentRow.title }}</p>
      </div>
      <span slot="footer">
        <cancel @click.native="InlineEditDialogVisible = false;
        getObjectiveProblemList(currentPage);
                  "></cancel>
        <save @click.native=" updateObjectiveProblemList(currentRow) "></save>
      </span>
    </el-dialog>
    <el-dialog title="Add Contest Objective Problem" v-if=" contestId " width="80%" :visible.sync=" addProblemDialogVisible "
      @close-on-click-modal=" false ">
      <add-objective-problem-component :contestID=" contestId "
        @on-change=" getObjectiveProblemList "></add-objective-problem-component>
    </el-dialog>
  </div>
</template>
  
<script>
import api from "../../api.js";
import AddObjectiveProblemComponent from "./AddPublicObjectiveProblem.vue";
export default {
  name: "ObjectiveProblemList",
  components: {
    AddObjectiveProblemComponent,
  },
  data() {
    return {
      pageSize: 10,
      total: 0,
      objectiveProblemList: [],
      keyword: "",
      loading: false,
      currentPage: 1,
      routeName: "",
      contestId: "",
      // for make public use
      currentProblemID: "",
      currentRow: {},
      InlineEditDialogVisible: false,
      makePublicDialogVisible: false,
      addProblemDialogVisible: false,
    };
  },
  mounted() {
    this.routeName = this.$route.name;
    this.contestId = this.$route.params.contestId;
    this.contestTitle = this.$route.params.contestTitle;
    this.getObjectiveProblemList(this.currentPage);
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    handleDblclick(row) {
      row.isEditing = true;
    },
    goEdit(objectiveProblemId) {
      if (this.routeName === "objective-problem-list") {
        this.$router.push({
          name: "edit-objective-problem",
          params: { objectiveProblemId },
        });
      } else if (this.routeName === "contest-objective-problem-list") {
        this.$router.push({
          name: "edit-contest-objective-problem",
          params: {
            objectiveProblemId: objectiveProblemId,
            contestId: this.contestId,
          },
        });
      }
    },
    goCreateObjectiveProblem() {
      if (this.routeName === "objective-problem-list") {
        this.$router.push({ name: "create-objective-problem" });
      } else if (this.routeName === "contest-objective-problem-list") {
        this.$router.push({
          name: "create-contest-objective-problem",
          params: { contestId: this.contestId },
        });
      }
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getObjectiveProblemList(page);
    },
    getObjectiveProblemList(page = 1) {
      this.loading = true;
      let funcName =
        this.routeName === "objective-problem-list"
          ? "getObjectiveProblemList"
          : "getContestObjectiveProblemList";
      let params = {
        limit: this.pageSize,
        offset: (page - 1) * this.pageSize,
        keyword: this.keyword,
        contest_id: this.contestId,
      };
      api[funcName](params).then(
        (res) => {
          this.loading = false;
          this.total = res.data.data.total;
          for (let objectiveProblem of res.data.data.results) {
            objectiveProblem.isEditing = false;
          }
          this.objectiveProblemList = res.data.data.results;
        },
        (res) => {
          this.loading = false;
        }
      );
    },
    deleteObjectiveProblem(id) {
      this.$confirm(
        "Sure to delete this objective problem? The associated submissions will be deleted as well.",
        "Delete Objective Problem",
        {
          type: "warning",
        }
      ).then(
        () => {
          let funcName =
            this.routeName === "objective-problem-list"
              ? "deleteObjectiveProblem"
              : "deleteContestObjectiveProblem";
          api[funcName](id)
            .then(() => [this.getObjectiveProblemList(this.currentPage - 1)])
            .catch(() => { });
        },
        () => { }
      );
    },
    makeContestObjectiveProblemPublic(objectiveProblemID) {
      this.$prompt(
        "Please input display id for the public problem",
        "confirm"
      ).then(
        ({ value }) => {
          api
            .makeContestObjectiveProblemPublic({
              id: objectiveProblemID,
              display_id: value,
            })
            .catch();
        },
        () => { }
      );
    },
    updateObjectiveProblemList(row) {
      let data = Object.assign({}, row);
      let funcName = "";
      if (this.contestId) {
        data.contest_id = this.contestId;
        funcName = "editContestObjectiveProblem";
      } else {
        funcName = "editObjectiveProblem";
      }
      api[funcName](data)
        .then((res) => {
          this.InlineEditDialogVisible = false;
          this.getObjectiveProblemList(this.currentPage);
        })
        .catch(() => {
          this.InlineEditDialogVisible = false;
        });
    },
    handleInlineEdit(row) {
      this.currentRow = row;
      this.InlineEditDialogVisible = true;
    },
  },
  watch: {
    $route(newVal, oldVal) {
      this.contestId = newVal.params.contestId;
      this.routeName = newVal.name;
      this.getObjectiveProblemList(this.currentPage);
    },
    keyword() {
      this.currentChange();
    },
  },
};
</script>
  
<style scoped lang="less"></style>
  