<template>
  <div class="announcement view">
    <Panel>
      <template v-slot:title>
        <el-page-header @back="goBack" :content="$t('m.General_Announcement')" style="margin-top: 5px">
        </el-page-header>
      </template>
      <div class="list">
        <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="announcementList"
          style="width: 100%">
          <el-table-column width="100" prop="id" :label="$t('m.ID')"> </el-table-column>
          <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
          <el-table-column prop="create_time" :label="$t('m.Create_Time')">
            <template slot-scope="scope">
              {{ scope.row.create_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column prop="last_update_time" :label="$t('m.Last_Update_Time')">
            <template slot-scope="scope">
              {{ scope.row.last_update_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column prop="created_by.username" :label="$t('m.Author')">
          </el-table-column>
          <el-table-column width="100" prop="visible" :label="$t('m.Visible')">
            <template slot-scope="scope">
              <el-switch v-model="scope.row.visible" active-text="" inactive-text=""
                @change="handleVisibleSwitch(scope.row)">
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column width="100" prop="top" :label="$t('m.Top')">
            <template slot-scope="scope">
              <el-switch v-model="scope.row.top" active-text="" inactive-text="" @change="handleTopSwitch(scope.row)">
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column fixed="right" :label="$t('m.Option')" width="200">
            <div slot-scope="scope">
              <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="openAnnouncementDialog(scope.row.id)"></icon-btn>
              <icon-btn :name="$t('m.Delete')" icon="trash" @click.native="deleteAnnouncement(scope.row.id)"></icon-btn>
              <icon-btn v-if="showCopyAddress" :name="$t('m.Copy_Address')" icon="copy" @click.native="copyAddress(scope.row.id)"></icon-btn>
            </div>
          </el-table-column>
        </el-table>
        <div class="panel-options">
          <el-button type="primary" size="small" @click="openAnnouncementDialog(null)" icon="el-icon-plus">{{
            $t('m.Create') }}</el-button>
          <el-pagination v-if="!contestID && !courseID" class="page" layout="prev, pager, next"
            @current-change="currentChange" :page-size="pageSize" :total="total">
          </el-pagination>
        </div>
      </div>
    </Panel>
    <!--对话框-->
    <el-dialog :title="announcementDialogTitle" :visible.sync="showEditAnnouncementDialog" @open="onOpenEditDialog"
      :close-on-click-modal="false">
      <el-form label-position="top">
        <el-form-item :label="$t('m.Announcement_Title')" required>
          <el-input v-model="announcement.title" :placeholder="$t('m.Announcement_Title')" class="title-input">
          </el-input>
        </el-form-item>
        <el-form-item :label="$t('m.Announcement_Content')" required>
          <Simditor v-model="announcement.content"></Simditor>
        </el-form-item>
        <div class="visible-box">
          <span>{{ $t("m.Announcement_visible") }}</span>
          <el-switch v-model="announcement.visible" active-text="" inactive-text="">
          </el-switch>
        </div>
        <div class="top-box">
          <span>{{ $t("m.Announcement_top") }}</span>
          <el-switch v-model="announcement.top" active-text="" inactive-text="">
          </el-switch>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="showEditAnnouncementDialog = false"></cancel>
        <save type="primary" @click.native="submitAnnouncement"></save>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Simditor from "../../components/Simditor.vue";
import api from "../../api.js";

export default {
  name: "Announcement",
  components: {
    Simditor,
  },
  data() {
    return {
      contestID: "",
      courseID: "",
      // 显示编辑公告对话框
      showEditAnnouncementDialog: false,
      // 公告列表
      announcementList: [],
      // 一页显示的公告数
      pageSize: 15,
      // 总公告数
      total: 0,
      // 当前公告id
      currentAnnouncementId: null,

      mode: "create",
      // 公告 (new | edit) model
      announcement: {
        title: "",
        visible: true,
        content: "",
        top: false,
      },
      // 对话框标题
      announcementDialogTitle: "Edit Announcement",
      // 是否显示loading
      loading: true,
      // 当前页码
      currentPage: 0,
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    init() {
      this.contestID = this.$route.params.contestId;
      this.courseID = this.$route.params.courseId;
      if (this.contestID) {
        this.getContestAnnouncementList();
      } else if (this.courseID) {
        this.getCourseAnnouncementList();
      } else {
        this.getAnnouncementList(1);
      }
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getAnnouncementList(page);
    },
    getAnnouncementList(page) {
      this.loading = true;
      api.getAnnouncementList((page - 1) * this.pageSize, this.pageSize).then(
        (res) => {
          this.loading = false;
          this.total = res.data.data.total;
          this.announcementList = res.data.data.results;
        },
        (res) => {
          this.loading = false;
        }
      );
    },
    getContestAnnouncementList() {
      this.loading = true;
      api
        .getContestAnnouncementList(this.contestID)
        .then((res) => {
          this.loading = false;
          this.announcementList = res.data.data;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    getCourseAnnouncementList() {
      this.loading = true;
      api
        .getCourseAnnouncementList(this.courseID)
        .then((res) => {
          this.loading = false;
          this.announcementList = res.data.data;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    // 打开编辑对话框的回调
    onOpenEditDialog() {
      // todo 优化
      // 暂时解决 文本编辑器显示异常bug
      setTimeout(() => {
        if (document.createEvent) {
          let event = document.createEvent("HTMLEvents");
          event.initEvent("resize", true, true);
          window.dispatchEvent(event);
        } else if (document.createEventObject) {
          window.fireEvent("onresize");
        }
      }, 0);
    },
    // 提交编辑
    // 默认传入MouseEvent
    submitAnnouncement(data = undefined) {
      let funcName = "";
      if (!data.title) {
        data = {
          id: this.currentAnnouncementId,
          title: this.announcement.title,
          content: this.announcement.content,
          visible: this.announcement.visible,
          top: this.announcement.top,
        };
      }
      if (this.contestID) {
        data.contest_id = this.contestID;
        funcName =
          this.mode === "edit"
            ? "updateContestAnnouncement"
            : "createContestAnnouncement";
      } else if (this.courseID) {
        data.course_id = this.courseID;
        funcName =
          this.mode === "edit"
            ? "updateCourseAnnouncement"
            : "createCourseAnnouncement";
      } else {
        funcName =
          this.mode === "edit" ? "updateAnnouncement" : "createAnnouncement";
      }
      api[funcName](data)
        .then((res) => {
          this.showEditAnnouncementDialog = false;
          this.init();
        })
        .catch();
    },
    // 删除公告
    deleteAnnouncement(announcementId) {
      this.$confirm(
        "Are you sure you want to delete this announcement?",
        "Warning",
        {
          confirmButtonText: "Delete",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          // then 为确定
          this.loading = true;
          let funcName = this.contestID
            ? "deleteContestAnnouncement"
            : this.courseID
              ? "deleteCourseAnnouncement"
              : "deleteAnnouncement";
          api[funcName](announcementId).then((res) => {
            this.loading = true;
            this.init();
          });
        })
        .catch(() => {
          // catch 为取消
          this.loading = false;
        });
    },
    openAnnouncementDialog(id) {
      this.showEditAnnouncementDialog = true;
      if (id !== null) {
        this.currentAnnouncementId = id;
        this.announcementDialogTitle = "Edit Announcement";
        this.announcementList.find((item) => {
          if (item.id === this.currentAnnouncementId) {
            this.announcement.title = item.title;
            this.announcement.visible = item.visible;
            this.announcement.content = item.content;
            this.announcement.top = item.top;
            this.mode = "edit";
          }
        });
      } else {
        this.announcementDialogTitle = "Create Announcement";
        this.announcement.title = "";
        this.announcement.visible = true;
        this.announcement.content = "";
        this.announcement.top = false;
        this.mode = "create";
      }
    },
    handleVisibleSwitch(row) {
      this.mode = "edit";
      this.submitAnnouncement({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible,
        top: row.top,
      });
    },
    handleTopSwitch(row) {
      this.mode = "edit";
      this.submitAnnouncement({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible,
        top: row.top,
      });
    },
    copyAddress(id) {
      this.$copyText(`/AnnouncementDetails/${id}`)
    }
  },
  watch: {
    $route() {
      this.init();
    },
  },
  computed:{
    showCopyAddress(){
      return this.$route.name === 'announcement'
    }
  }
};
</script>

<style lang="less" scoped>
.title-input {
  margin-bottom: 20px;
}

.visible-box {
  margin-top: 10px;
  width: 205px;
  float: left;
}

.top-box {
  margin-top: 10px;
  width: 205px;
  float: left;
}
</style>
