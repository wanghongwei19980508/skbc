<template>
  <div class="view">
    <Panel :title="$t('m.' + title)">
      <div slot="title">
        <el-page-header @back="goBack" :content="$t('m.' + title)" style="margin-top: 5px">
        </el-page-header>
      </div>
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item :label="$t('m.CourseTitle')" required>
              <el-input v-model="course.title" :placeholder="$t('m.CourseTitle')"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.CourseDescription')" required>
              <Simditor v-model="course.description"></Simditor>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Course_Start_Time')" required>
              <el-date-picker v-model="course.start_time" type="datetime" :placeholder="$t('m.Course_Start_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Course_End_Time')" required>
              <el-date-picker v-model="course.end_time" type="datetime" :placeholder="$t('m.Course_End_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Course_Password')">
              <el-input v-model="course.password" :placeholder="$t('m.Course_Password')"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Tag')" :error="error.tags" required>
              <span class="tags">
                <el-tag v-for="tag in course.tags" :closable="true" :close-transition="false" :key="tag" type="success"
                  @close="closeTag(tag)">{{ tag }}</el-tag>
              </span>
              <el-autocomplete v-if="inputTagVisible" size="mini" class="input-new-tag" popper-class="course-tag-poper"
                v-model="tagInput" :trigger-on-focus="false" @keyup.enter.native="addTag" @select="addTag"
                :fetch-suggestions="querySearchTag" ref="inputTag">
              </el-autocomplete>
              <el-button class="button-new-tag" v-else size="small" @click="showTagInput">+ {{ $t("m.New_Tag")
              }}</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <save @click.native="saveCourse"></save>
    </Panel>
  </div>
</template>
  
<script>
import api from "../../api.js";
import Simditor from "../../components/Simditor.vue";

export default {
  name: "CreateCourse",
  components: {
    Simditor,
  },
  data() {
    return {
      title: "Create_Course",
      course: {
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        password: "",
        visible: true,
        is_template: false,
        tags: [],
      },
      students: [],
      lecturers: [],
      managers: [],
      inputTagVisible: false,
      tagInput: "",
      inputStudentVisible: false,
      studentInput: "",
      inputLectureVisible: false,
      lectureInput: "",
      inputManagerVisible: false,
      managerInput: "",
      error: {
        tags: "",
        student: {},
        lecture: {},
        manager: {},
      },
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    querySearchTag(queryString, cb) {
      api
        .getCourseTagList({ keyword: queryString })
        .then((res) => {
          let tagList = [];
          for (let tag of res.data.data) {
            tagList.push({ value: tag.name });
          }
          if (tagList.length === 0) tagList.push({ value: queryString });
          cb(tagList);
        })
        .catch(() => { });
    },
    showTagInput() {
      this.inputTagVisible = true;
      this.$nextTick((_) => {
        this.$refs.inputTag.focus();
      });
    },
    addTag() {
      let inputValue = this.tagInput;
      if (inputValue) {
        this.course.tags.push(inputValue);
      }
      this.inputTagVisible = false;
      this.tagInput = "";
    },
    closeTag(tag) {
      this.course.tags.splice(this.course.tags.indexOf(tag), 1);
    },
    saveCourse() {
      let funcName =
        this.$route.name === "edit-course" ? "editCourse" : "createCourse";
      api[funcName](this.course)
        .then((res) => {
          this.$router.push({
            name: "course-list",
            query: { refresh: "true" },
          });
        })
        .catch(() => { });
    },
  },
  mounted() {
    if (this.$route.name === "edit-course") {
      this.title = "Edit_Course";
      api
        .getCourse(this.$route.params.courseId)
        .then((res) => {
          let data = res.data.data;
          this.course = data;
        })
        .catch(() => { });
    }
  },
};
</script>
    
<style lang="less" scoped>
.input-new-tag {
  width: 78px;
}

.button-new-tag {
  height: 24px;
  line-height: 22px;
  padding-top: 0;
  padding-bottom: 0;
}

.tags {
  .el-tag {
    margin-right: 10px;
  }
}
</style>
  