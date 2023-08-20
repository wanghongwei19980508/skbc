<template>
  <div class="lesson view">
    <Panel>
      <div slot="title">
        <el-page-header @back="goBack" :content="$t('m.Lesson')" style="margin-top: 5px">
        </el-page-header>
      </div>
      <template v-slot:header>
        <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </template>
      <div class="list">
        <el-table v-loading="loading" element-loading-text="loading..." ref="table" :data="lessonList"
          style="width: 100%">
          <el-table-column width="100" prop="id" label="ID"> </el-table-column>
          <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
          <el-table-column prop="start_time" :label="$t('m.Start_Time')">
            <template slot-scope="scope">
              {{ scope.row.start_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column prop="end_time" :label="$t('m.End_Time')">
            <template slot-scope="scope">
              {{ scope.row.end_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column width="100" prop="visible" :label="$t('m.Visible')">
            <template slot-scope="scope">
              <el-switch v-model="scope.row.visible" active-text="" inactive-text=""
                @change="handleVisibleSwitch(scope.row)">
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column width="200" prop="ordinal" :label="$t('m.ordinal')">
            <template slot-scope="scope">
              <el-input-number v-model="scope.row.ordinal" @change="handleOrdinal(scope.row)">
              </el-input-number>
            </template>
          </el-table-column>
          <el-table-column fixed="right" :label="$t('m.Option')" width="240">
            <div slot-scope="scope">
              <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="openLessonDialog(scope.row.id)"></icon-btn>
              <icon-btn :name="$t('m.Assignment')" icon="list-ol"
                @click.native="goLessonAssignmentList(scope.row.id)"></icon-btn>
              <icon-btn :name="$t('m.PPT')" icon="list-ol" @click.native="goAssignmentPPTList(scope.row.id)"></icon-btn>
              <icon-btn :name="$t('m.Delete')" icon="trash" @click.native="deleteLesson(scope.row.id)"></icon-btn>
            </div>
          </el-table-column>
        </el-table>
        <div class="panel-options">
          <el-button type="primary" size="small" @click="openLessonDialog(null)" icon="el-icon-plus">{{ $t('m.Create')
          }}</el-button>
          <el-pagination class="page" layout="prev, pager, next" @current-change="currentChange" :page-size="pageSize"
            :total="total">
          </el-pagination>
        </div>
      </div>
    </Panel>
    <!--对话框-->
    <el-dialog :title="$t('m.' + lessonDialogTitle)" :visible.sync="showEditLessonDialog" @open="onOpenEditDialog"
      :close-on-click-modal="false">
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item :label="$t('m.Lesson_Title')" required>
              <el-input v-model="lesson.title" :placeholder="$t('m.Lesson_Title')">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.Lesson_Content')" required>
              <Simditor v-model="lesson.content"></Simditor>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Lesson_Start_Time')" required>
              <el-date-picker v-model="lesson.start_time" type="datetime" :placeholder="$t('m.Lesson_Start_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Lesson_End_Time')" required>
              <el-date-picker v-model="lesson.end_time" type="datetime" :placeholder="$t('m.Lesson_End_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Lesson_visible')" required>
              <el-switch v-model="lesson.visible"> </el-switch></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Lesson_ordinal')" required>
              <el-input-number v-model="lesson.ordinal"> </el-input-number></el-form-item>
          </el-col>
          <el-col :offset="16">
            <cancel @click.native="showEditLessonDialog = false"></cancel>
            <save type="primary" @click.native="submitLesson"></save>
          </el-col>
        </el-row>
      </el-form>
    </el-dialog>
    <el-dialog :visible="pptlistDialogVisible" :title="$t('m.Add_ppt')" :fullscreen="pptlistFullscreen"
      :close-on-click-modal="false" @close="pptlistDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Add_ppt') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="pptlistFullscreen = !pptlistFullscreen"></el-button>
      </div>
      <el-transfer filterable filter-placeholder="请输入PPT名称" v-model="pptlistvalue" :data="pptlist"  :titles="['全部PPT', '课程PPT']"  :button-texts="['删除', '添加']">
      </el-transfer>
      <span slot="footer" class="dialog-footer">
        <el-button @click="pptlistDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="savePPT">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>
  
<script>
import Simditor from "../../components/Simditor.vue";
import api from "../../api.js";

export default {
  name: "Lesson",
  components: {
    Simditor,
  },
  data() {
    return {
      courseID: "",
      // 显示编辑课时对话框
      showEditLessonDialog: false,
      // 课时列表
      lessonList: [],
      // 一页显示的课时数
      pageSize: 15,
      // 总课时数
      total: 0,
      // 当前课时id
      currentLessonId: null,
      mode: "create",
      // 课时 (new | edit) model
      lesson: {
        title: "",
        visible: true,
        content: "",
        ordinal: 1,
        start_time: "",
        end_time: "",
      },
      keyword: "",
      // 对话框标题
      lessonDialogTitle: "Edit_Lesson",
      // 是否显示loading
      loading: true,
      // 当前页码
      currentPage: 0,
      lesson_id: '', // 当前课程id
      pptlistDialogVisible: false, // ppt dialog
      pptlistFullscreen: false, // ppt全屏
      pptlist: [], // 全部ppt列表
      pptlistvalue: [], // 课程ppt列表 
      originPptlistvalue: [], // 原始课程ppt列表 
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
      this.courseID = this.$route.params.courseId;
      this.getLessonList(1);
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getLessonList(page);
    },
    getLessonList(page) {
      this.loading = true;
      api
        .getCourseLessonList(
          this.courseID,
          (page - 1) * this.pageSize,
          this.pageSize,
          this.keyword
        )
        .then(
          (res) => {
            this.loading = false;
            this.total = res.data.data.total;
            this.lessonList = res.data.data.results;
          },
          (res) => {
            this.loading = false;
          }
        );
    },
    goLessonAssignmentList(lessonId) {
      this.$router.push({
        name: "lesson-assignment-list",
        params: { lessonId },
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
    submitLesson(data = undefined) {
      let funcName = "";
      if (!data.title) {
        data = {
          id: this.currentLessonId,
          title: this.lesson.title,
          content: this.lesson.content,
          visible: this.lesson.visible,
          start_time: this.lesson.start_time,
          end_time: this.lesson.end_time,
          ordinal: this.lesson.ordinal,
        };
      }

      data.course_id = this.courseID;
      funcName =
        this.mode === "edit" ? "updateCourseLesson" : "createCourseLesson";

      api[funcName](data)
        .then((res) => {
          this.showEditLessonDialog = false;
          this.init();
        })
        .catch();
    },
    // 删除课时
    deleteLesson(lessonId) {
      this.$confirm("Are you sure you want to delete this lesson?", "Warning", {
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          // then 为确定
          this.loading = true;
          let funcName = "deleteCourseLesson";

          api[funcName](lessonId).then((res) => {
            this.loading = true;
            this.init();
          });
        })
        .catch(() => {
          // catch 为取消
          this.loading = false;
        });
    },
    openLessonDialog(id) {
      this.showEditLessonDialog = true;
      if (id !== null) {
        this.currentLessonId = id;
        this.lessonDialogTitle = "Edit_Lesson";
        this.lessonList.find((item) => {
          if (item.id === this.currentLessonId) {
            this.lesson.title = item.title;
            this.lesson.visible = item.visible;
            this.lesson.content = item.content;
            this.lesson.ordinal = item.ordinal;
            this.lesson.start_time = item.start_time;
            this.lesson.end_time = item.end_time;
            this.mode = "edit";
          }
        });
      } else {
        this.lessonDialogTitle = "Create_Lesson";
        this.lesson.title = "";
        this.lesson.visible = true;
        this.lesson.content = "";
        this.lesson.ordinal = 1;
        this.lesson.start_time = "";
        this.lesson.end_time = "";
        this.mode = "create";
      }
    },
    handleVisibleSwitch(row) {
      this.mode = "edit";
      this.submitLesson({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible,
        ordinal: row.ordinal,
        start_time: row.start_time,
        end_time: row.end_time,
      });
    },
    handleOrdinal(row) {
      this.mode = "edit";
      this.submitLesson({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible,
        ordinal: row.ordinal,
        start_time: row.start_time,
        end_time: row.end_time,
      });
    },
    // 添加ppt列表
    async goAssignmentPPTList(id) {
      this.lesson_id = id
      await api.getPPTList({ offset: 0 }).then((res) => {
        this.pptlist = res.data.data.results.map(item => {
          return {
            label: item.name,
            key: item.id
          }
        })
      })
      await api.getLessonPPT({ lesson_id: this.lesson_id }).then((res) => {
        this.pptlistvalue = res.data.data.results.map(item => {
          return item.attachment.id
        })
        this.originPptlistvalue = JSON.parse(JSON.stringify(this.pptlistvalue))
      })
      this.pptlistDialogVisible = true
    },
    // 报错课程ppt
    savePPT() {
      for (let attachment of this.originPptlistvalue) {
        if (!this.pptlistvalue.includes(attachment)) {
          api.deleteLessonPPT({ lesson_id: this.lesson_id, attachment_id: attachment });
        }
      }
      for (let attachment of this.pptlistvalue) {
        if (!this.originPptlistvalue.includes(attachment)) {
          api.createLessonPPT({ lesson_id: this.lesson_id, attachment_id: attachment });
        }
      }
      this.pptlistDialogVisible = false;
    }
  },
  watch: {
    $route() {
      this.init();
    },
    keyword() {
      this.currentChange(1);
    },
  },
};
</script>
  