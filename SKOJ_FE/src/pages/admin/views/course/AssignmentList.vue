<template>
  <div class="view">
    <panel>
      <div slot="title">
        <el-page-header @back="goBack" :content="$t('m.Assignment_List')" style="margin-top: 5px">
        </el-page-header>
      </div>
      <div slot="header">
        <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="assignmentList" style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-descriptions :column="2" border>
              <el-descriptions-item :label="$t('m.Start_Time')">
                {{ props.row.start_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item :label="$t('m.End_Time')">
                {{ props.row.end_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item :label="$t('m.Create_Time')">
                {{ props.row.create_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item :label="$t('m.Creator')">
                {{ props.row.created_by.username }}
              </el-descriptions-item>
            </el-descriptions>
          </template>
        </el-table-column>
        <el-table-column prop="id" width="80" label="ID"> </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
        <el-table-column :label="$t('m.Rule_Type')" width="130">
          <template slot-scope="scope">
            <el-tag type="gray">{{ scope.row.rule_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('m.Assignment_Type')" width="180">
          <template slot-scope="scope">
            <el-tag :type="
              scope.row.contest_type === 'Public' ? 'success' : 'primary'
            ">
              {{ scope.row.contest_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('m.Status')" width="130">
          <template slot-scope="scope">
            <el-tag :type="
              scope.row.status === '-1'
                ? 'danger'
                : scope.row.status === '0'
                  ? 'success'
                  : 'primary'
            ">
              {{ scope.row.status | assignmentStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column width="100" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text=""
              @change="handleVisibleSwitch(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" width="275" :label="$t('m.Operation')">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEdit(scope.row.id)"></icon-btn>
            <!-- <icon-btn :name="$t('m.Problem')" icon="list-ol"
              @click.native="goAssignmentProblemList(scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Objective_Problem')" icon="list-ol"
              @click.native="goAssignmentObjectiveProblemList(scope.row.id)"></icon-btn> -->
            <icon-btn :name="$t('m.Public_Topic')" icon="list-ol"
              @click.native="goAssignmentPublicTopicList(scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Announcement')" icon="info-circle"
              @click.native="goAssignmentAnnouncement(scope.row.id)"></icon-btn>
            <icon-btn icon="download" :name="$t('m.Download_Accepted_Submissions')"
              @click.native="openDownloadOptions(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreateAssignment" icon="el-icon-plus">{{ $t('m.Create') }}
        </el-button>
        <el-pagination class="page" layout="prev, pager, next" @current-change="currentChange" :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
    <el-dialog title="Download Assignment Submissions" width="30%" :visible.sync="downloadDialogVisible">
      <el-switch v-model="excludeAdmin" active-text="Exclude admin submissions"></el-switch>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="downloadSubmissions">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
  
<script>
import api from "../../api.js";
import utils from "@/utils/utils";
import { CONTEST_STATUS_REVERSE } from "@/utils/constants";

export default {
  name: "AssignmentList",
  data() {
    return {
      pageSize: 10,
      total: 0,
      assignmentList: [],
      keyword: "",
      loading: false,
      excludeAdmin: true,
      currentPage: 1,
      currentId: 1,
      downloadDialogVisible: false,
      lessonId: "",
    };
  },
  mounted() {
    this.lessonId = this.$route.params.lessonId;
    this.getAssignmentList(this.currentPage);
  },
  filters: {
    assignmentStatus(value) {
      return CONTEST_STATUS_REVERSE[value].name;
    },
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    goCreateAssignment() {
      this.$router.push({
        name: "create-assignment",
        path: "/assignment/create",
        params: {
          lessonId: this.lessonId,
        },
      });
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getAssignmentList(page);
    },
    getAssignmentList(page) {
      this.loading = true;
      api
        .getAssignmentList(
          this.lessonId,
          (page - 1) * this.pageSize,
          this.pageSize,
          this.keyword
        )
        .then(
          (res) => {
            this.loading = false;
            this.total = res.data.data.total;
            this.assignmentList = res.data.data.results;
          },
          (res) => {
            this.loading = false;
          }
        );
    },
    openDownloadOptions(assignmentId) {
      this.downloadDialogVisible = true;
      this.currentId = assignmentId;
    },
    downloadSubmissions() {
      let excludeAdmin = this.excludeAdmin ? "1" : "0";
      let url = `/admin/download_submissions?assignment_id=${this.currentId}&exclude_admin=${excludeAdmin}`;
      utils.downloadFile(url);
    },
    goEdit(assignmentId) {
      this.$router.push({ name: "edit-assignment", params: { assignmentId } });
    },
    goAssignmentAnnouncement(contestId) {
      this.$router.push({
        name: "contest-announcement",
        params: { contestId },
      });
    },
    // goAssignmentProblemList(contestId) {
    //   this.$router.push({
    //     name: "contest-problem-list",
    //     params: { contestId },
    //   });
    // },
    // goAssignmentObjectiveProblemList(contestId) {
    //   this.$router.push({
    //     name: "contest-objective-problem-list",
    //     params: { contestId },
    //   });
    // },
    goAssignmentPublicTopicList(contestId) {
      this.$router.push({
        name: "contest-public-topic-list",
        params: { contestId },
      });
    },
    handleVisibleSwitch(row) {
      api.editAssignment(row);
    },
  },
  watch: {
    keyword() {
      this.currentChange(1);
    },
  },
};
</script>
  