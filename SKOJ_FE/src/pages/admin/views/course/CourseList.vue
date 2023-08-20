<template>
  <div class="view">
    <Panel :title="$t('m.Course_List')">
      <div slot="header">
        <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="courseList" style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Start Time">
                {{ props.row.start_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item label="End Time">
                {{ props.row.end_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item label="Create Time">
                {{ props.row.create_time | localtime }}
              </el-descriptions-item>
              <el-descriptions-item label="Creator">
                {{ props.row.created_by.username }}
              </el-descriptions-item>
            </el-descriptions>
          </template>
        </el-table-column>
        <el-table-column prop="id" width="80" label="ID"> </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
        <el-table-column :label="$t('m.Tag')" width=" 130">
          <template slot-scope="scope">
            <span class="tags">
              <el-tag type="primary" v-for="tag in scope.row.tags" :key="tag">{{
                tag
              }}</el-tag></span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('m.Course_Type')" width="180">
          <template slot-scope="scope">
            <el-tag :type="scope.row.course_type === 'Public' ? 'success' : 'primary'">
              {{ scope.row.course_type }}
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
              {{ scope.row.status | courseStatus }}
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
        <el-table-column width="100" :label="$t('m.Template')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.template" active-text="" inactive-text=""
              @change="handleTemplatewitch(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" width="275" :label="$t('m.Operation')">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEdit(scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Member')" icon="user" @click.native="editMember(scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Lesson')" icon="list-ol" @click.native="goCourseLeeson(scope.row.id)"></icon-btn>
            <icon-btn :name="$t('m.Announcement')" icon="info-circle"
              @click.native="goCourseAnnouncement(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreateCourse" icon="el-icon-plus">{{ $t('m.Create') }}
        </el-button>
        <!-- <el-button
          type="primary"
          size="small"
          @click="goCreateCourse"
          icon="el-icon-plus"
          >Create From Template
        </el-button> -->
        <el-pagination class="page" layout="prev, pager, next" @current-change="currentChange" :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
    <el-dialog title="提示" :visible.sync="dialogVisible" :before-close="handleClose">
      <el-tabs v-model="tabActivate" @tab-click="handleClick">
        <el-tab-pane label="管理学生" name="student">
          <el-transfer filterable :filter-method="filterUser" filter-placeholder="请输入关键信息" v-model="studentList"
            :data="userList" :titles="[$t('m.Source'), $t('m.Target')]" :button-texts="[$t('m.Del'), $t('m.Add')]">
          </el-transfer>
        </el-tab-pane>
        <el-tab-pane label="管理讲师" name="lecture">
          <el-transfer filterable :filter-method="filterUser" filter-placeholder="请输入关键信息" v-model="lectureList"
            :data="userList" :titles="[$t('m.Source'), $t('m.Target')]" :button-texts="[$t('m.Del'), $t('m.Add')]">
          </el-transfer></el-tab-pane>
        <el-tab-pane label="管理学管" name="Manager">
          <el-transfer filterable :filter-method="filterUser" filter-placeholder="请输入关键信息" v-model="managerList"
            :data="userList" :titles="[$t('m.Source'), $t('m.Target')]" :button-texts="[$t('m.Del'), $t('m.Add')]">
          </el-transfer>
        </el-tab-pane>
      </el-tabs>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveMember">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>
  
<script>
import api from "../../api.js";
import { CONTEST_STATUS_REVERSE, COURSE_ROLE } from "@/utils/constants";

export default {
  name: "CourseList",
  data() {
    return {
      pageSize: 10,
      total: 0,
      courseList: [],
      keyword: "",
      tabActivate: "student",
      loading: false,
      excludeAdmin: true,
      currentPage: 1,
      dialogVisible: false,
      courseId: "",
      studentList: [],
      lectureList: [],
      managerList: [],
      originStudentList: [],
      originLectureList: [],
      originManagerList: [],
      userList: [],
      saveLoading: false,
    };
  },
  mounted() {
    this.getCourseList(this.currentPage);
  },
  filters: {
    courseStatus(value) {
      return CONTEST_STATUS_REVERSE[value].name;
    },
  },
  methods: {
    goCreateCourse() {
      this.$router.push({
        name: "create-course",
        path: "/course/create",
      });
    },
    filterUser(query, item) {
      if (item.user.real_name) {
        return (
          item.label.indexOf(query) > -1 ||
          item.user.real_name.indexOf(query) > -1
        );
      }
      return item.label.indexOf(query) > -1;
    },
    getStudents(courseId) {
      api.getCourseUsers(courseId, COURSE_ROLE.STUDENT).then((res) => {
        this.studentList = [];
        for (let user of res.data.data) {
          this.studentList.push(user.user.id);
        }
        this.originStudentList = this.studentList;
      });
    },
    getLectures(courseId) {
      api.getCourseUsers(courseId, COURSE_ROLE.LECTURE).then((res) => {
        this.lectureList = [];
        for (let user of res.data.data) {
          this.lectureList.push(user.user.id);
        }
        this.originLectureList = this.lectureList;
      });
    },
    getManagers(courseId) {
      api.getCourseUsers(courseId, COURSE_ROLE.MANAGER).then((res) => {
        this.managerList = [];
        for (let user of res.data.data) {
          this.managerList.push(user.user.id);
        }
        this.originManagerList = this.managerList;
      });
    },
    editMember(courseId) {
      api
        .getUserList(undefined, undefined, undefined)
        .then((res) => {
          this.userList = [];
          for (let user of res.data.data.results) {
            this.userList.push({
              label: user.phone
                ? user.username + "|" + user.phone
                : user.username,
              key: user.id,
              user: user,
            });
          }
          this.courseId = courseId;
          this.getStudents(courseId);
          this.getLectures(courseId);
          this.getManagers(courseId);
          this.dialogVisible = true;
        })
        .catch(() => { });
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => { });
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getCourseList(page);
    },
    getCourseList(page) {
      this.loading = true;
      api
        .getCourseList((page - 1) * this.pageSize, this.pageSize, this.keyword)
        .then(
          (res) => {
            this.loading = false;
            this.total = res.data.data.total;
            this.courseList = res.data.data.results;
          },
          (res) => {
            this.loading = false;
          }
        );
    },
    goEdit(courseId) {
      this.$router.push({ name: "edit-course", params: { courseId } });
    },
    goCourseAnnouncement(courseId) {
      this.$router.push({
        name: "course-announcement",
        params: { courseId },
      });
    },
    goCourseLeeson(courseId) {
      this.$router.push({
        name: "course-lesson",
        params: { courseId },
      });
    },
    handleVisibleSwitch(row) {
      api.editCourse(row);
    },
    handleTemplatewitch(row) {
      api.editCourse(row);
    },
    saveMember() {
      this.saveLoading = true;
      for (let student of this.originStudentList) {
        if (!this.studentList.includes(student)) {
          api.deleteCourseUser(this.courseId, student, COURSE_ROLE.STUDENT);
        }
      }
      for (let student of this.studentList) {
        if (!this.originStudentList.includes(student)) {
          api.addCourseUser(this.courseId, student, COURSE_ROLE.STUDENT);
        }
      }
      for (let lecture of this.originLectureList) {
        if (!this.lectureList.includes(lecture)) {
          api.deleteCourseUser(this.courseId, lecture, COURSE_ROLE.LECTURE);
        }
      }
      for (let lecture of this.lectureList) {
        if (!this.originLectureList.includes(lecture)) {
          api.addCourseUser(this.courseId, lecture, COURSE_ROLE.LECTURE);
        }
      }
      for (let manager of this.originManagerList) {
        if (!this.managerList.includes(manager)) {
          api.deleteCourseUser(this.courseId, manager, COURSE_ROLE.MANAGER);
        }
      }
      for (let manager of this.managerList) {
        if (!this.originManagerList.includes(manager)) {
          api.addCourseUser(this.courseId, manager, COURSE_ROLE.MANAGER);
        }
      }
      this.saveLoading = false;
      this.dialogVisible = false;
    },
    handleClick(){
      
    }
  },
  watch: {
    keyword() {
      this.currentChange(1);
    },
  },
};
</script>
    
<style lang="less" scoped>
.tags {
  .el-tag {
    margin-right: 10px;
  }
}
</style>