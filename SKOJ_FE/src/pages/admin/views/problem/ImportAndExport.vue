<template>
  <div>
    <div style="padding-bottom: 10px"></div>
    <panel :title="$t('m.Export_Problems')">
      <div slot="header">
        <el-input
          v-model="keyword"
          prefix-icon="el-icon-search"
          placeholder="Keywords"
        >
        </el-input>
      </div>
      <el-table
        :data="problems"
        v-loading="loadingProblems"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="60"> </el-table-column>
        <el-table-column label="ID" width="100" prop="id"> </el-table-column>
        <el-table-column :label="$t('m.Display_ID')" width="200" prop="_id">
        </el-table-column>
        <el-table-column :label="$t('m.Title')" prop="title"> </el-table-column>
        <el-table-column :label="$t('m.Author')" prop="created_by.username">
        </el-table-column>
        <el-table-column prop="create_time" :label="$t('m.Create_Time')">
          <template slot-scope="scope">
            {{ scope.row.create_time | localtime }}
          </template>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button
          type="primary"
          size="small"
          v-show="selected_problems.length"
          @click="exportProblems"
          icon="el-icon-fa-arrow-down"
          >Export
        </el-button>
        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="getProblems"
          :page-size="limit"
          :total="total"
        >
        </el-pagination>
      </div>
    </panel>
    <panel :title="$t('m.Export_Objective_Problems')">
      <div slot="header">
        <el-input
          v-model="objectiveKeyword"
          prefix-icon="el-icon-search"
          placeholder="Keywords"
        >
        </el-input>
      </div>
      <el-table
        :data="objectiveProblems"
        v-loading="loadingObjectiveProblems"
        @selection-change="handleObjectiveSelectionChange"
      >
        <el-table-column type="selection" width="60"> </el-table-column>
        <el-table-column label="ID" width="100" prop="id"> </el-table-column>
        <el-table-column :label="$t('m.Display_ID')" width="200" prop="_id">
        </el-table-column>
        <el-table-column :label="$t('m.Title')" prop="title"> </el-table-column>
        <el-table-column :label="$t('m.Author')" prop="created_by.username">
        </el-table-column>
        <el-table-column prop="create_time" :label="$t('m.Create_Time')">
          <template slot-scope="scope">
            {{ scope.row.create_time | localtime }}
          </template>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button
          type="primary"
          size="small"
          v-show="selected_objective_problems.length"
          @click="exportObjectiveProblems"
          icon="el-icon-fa-arrow-down"
          >Export
        </el-button>
        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="getObjectiveProblems"
          :page-size="limit"
          :total="total"
        >
        </el-pagination>
      </div>
    </panel>
    <panel :title="$t('m.Import_QDUOJ_Problems')">
      <el-upload
        ref="QDU"
        action="/api/admin/import_problem"
        name="file"
        :file-list="fileList1"
        :show-file-list="true"
        :with-credentials="true"
        :limit="3"
        :on-change="onFile1Change"
        :auto-upload="false"
        :on-success="uploadSucceeded"
        :on-error="uploadFailed"
      >
        <el-button
          size="small"
          type="primary"
          icon="el-icon-fa-upload"
          slot="trigger"
          >{{$t('m.Choose_File')}}</el-button
        >
        <el-button
          style="margin-left: 10px"
          size="small"
          type="success"
          @click="submitUpload('QDU')"
          >{{$t('m.Upload')}}</el-button
        >
      </el-upload>
    </panel>

    <panel :title="$t('m.Import_FPS_Problems')">
      <el-upload
        ref="FPS"
        action="/api/admin/import_fps"
        name="file"
        :file-list="fileList2"
        :show-file-list="true"
        :with-credentials="true"
        :limit="3"
        :on-change="onFile2Change"
        :auto-upload="false"
        :on-success="uploadSucceeded"
        :on-error="uploadFailed"
      >
        <el-button
          size="small"
          type="primary"
          icon="el-icon-fa-upload"
          slot="trigger"
          >{{$t('m.Choose_File')}}</el-button
        >
        <el-button
          style="margin-left: 10px"
          size="small"
          type="success"
          @click="submitUpload('FPS')"
          >{{$t('m.Upload')}}</el-button
        >
      </el-upload>
    </panel>
  </div>
</template>
<script>
import api from "@admin/api";
import utils from "@/utils/utils";

export default {
  name: "import_and_export",
  data() {
    return {
      fileList1: [],
      fileList2: [],
      page: 1,
      objectivePage: 1,
      limit: 10,
      total: 0,
      loadingProblems: false,
      loadingObjectiveProblems: false,
      loadingImporting: false,
      keyword: "",
      objectiveKeyword: "",
      problems: [],
      objectiveProblems: [],
      selected_problems: [],
      selected_objective_problems: [],
    };
  },
  mounted() {
    this.getProblems();
    this.getObjectiveProblems();
  },
  methods: {
    handleSelectionChange(val) {
      this.selected_problems = val;
    },
    handleObjectiveSelectionChange(val) {
      this.selected_objective_problems = val;
    },
    getProblems(page = 1) {
      let params = {
        keyword: this.keyword,
        offset: (page - 1) * this.limit,
        limit: this.limit,
      };
      this.loadingProblems = true;
      api.getProblemList(params).then((res) => {
        this.problems = res.data.data.results;
        this.total = res.data.data.total;
        this.loadingProblems = false;
      });
    },
    getObjectiveProblems(objectivePage = 1) {
      let params = {
        keyword: this.objectiveKeyword,
        offset: (objectivePage - 1) * this.limit,
        limit: this.limit,
      };
      this.loadingObjectiveProblems = true;
      api.getObjectiveProblemList(params).then((res) => {
        this.objectiveProblems = res.data.data.results;
        this.total = res.data.data.total;
        this.loadingObjectiveProblems = false;
      });
    },
    exportObjectiveProblems() {
      let params = [];
      for (let p of this.selected_problems) {
        params.push("objective_problem_id=" + p.id);
      }
      let url = "/admin/export_objective_problem?" + params.join("&");
      utils.downloadFile(url);
    },
    exportProblems() {
      let params = [];
      for (let p of this.selected_problems) {
        params.push("problem_id=" + p.id);
      }
      let url = "/admin/export_problem?" + params.join("&");
      utils.downloadFile(url);
    },
    submitUpload(ref) {
      this.$refs[ref].submit();
    },
    onFile1Change(file, fileList) {
      this.fileList1 = fileList.slice(-1);
    },
    onFile2Change(file, fileList) {
      this.fileList2 = fileList.slice(-1);
    },
    uploadSucceeded(response) {
      if (response.error) {
        this.$error(response.data);
      } else {
        this.$success(
          "Successfully imported " + response.data.import_count + " problems"
        );
        this.getProblems();
      }
    },
    uploadFailed() {
      this.$error("Upload failed");
    },
  },
  watch: {
    keyword() {
      this.getProblems();
    },
    objectiveKeyword() {
      this.getObjectiveProblems();
    },
  },
};
</script>

<style scoped lang="less">
</style>
