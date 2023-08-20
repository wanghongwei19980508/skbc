<template>
  <div>
    <el-skeleton :loading="loading">
      <template>
        <AssignmentRow v-for="(lesson, index) in lessons" :key="index" :title="lesson.title" :content="lesson.content"
          :assignments="lesson.assignments" :pptList="lesson.pptList">
        </AssignmentRow>

        <Pagination :total="total" :pageSize="query.limit" @on-change="pushRouter" @on-page-size-change="pushRouter"
          :current="query.page" :showSizer="true"></Pagination>
      </template>
    </el-skeleton>
  </div>
</template>

<script>
import api from "../../../api.js";
import Pagination from "../../../components/Pagination.vue";
import Panel from "../../../../admin/components/Panel.vue";
import AssignmentRow from "../../../components/AssignmentRow.vue";
export default {
  name: "LessonList",
  components: {
    Pagination,
    Panel,
    AssignmentRow,
  },
  data() {
    return {
      total: 0,
      query: {
        keyword: "",
        page: 1,
        limit: 10,
        courseID: "",
      },
      lessons: [],
      loading: true,
      number: 0,
      pptList: [],
    };
  },
  mounted() {
    this.query.courseID = this.$route.params.courseID;
    this.init();
  },
  methods: {
    init() {
      this.getLessonList();
    },
    getLessonList() {
      let offset = (this.query.page - 1) * this.query.limit;
      api.getCourseLessons(offset, this.query.limit, this.query.courseID).then((res) => {
        this.total = res.data.data.total;
        this.lessons = res.data.data.results;
        this.getdata()
      });
    },
    async getdata() {
      for (let lesson of this.lessons) {
        lesson.pptList = []
        api.getContestPPTList({ lesson_id: lesson.id }).then((res) => {
          for (let ppt of res.data.data.results) {
            lesson.pptList.push(ppt.attachment);
          }
        })
        await api.getLessonAssignments(lesson.id).then((res) => {
          lesson.assignments = [];
          for (let ass of res.data.data) {
            let assignment = {
              id: ass.id,
              title: ass.title,
              start_time: ass.start_time,
              end_time: ass.end_time,
              problem: [],
              objectiveProblem: [],
            };
            api.getContestObjectiveProblemList(ass.id).then((res) => {
              for (let problem of res.data.data) {
                assignment.objectiveProblem.push(problem);
              }
            });
            api.getContestProblemList(ass.id).then((res) => {
              for (let problem of res.data.data) {
                assignment.problem.push(problem);
              }
            });
            lesson.assignments.push(assignment);
          }
          this.number += 1;
          if (this.number == this.lessons.length) {
            this.loading = false;
            this.number = 0;
          }
        });
      }
    },
    pushRouter(page) {
      this.$router.push({
        name: "members",
        query: {
          page: page,
          keyword: this.query.keyword,
          courseID: this.query.courseID,
        },
      });
    },
  },
};
</script>

<style></style>