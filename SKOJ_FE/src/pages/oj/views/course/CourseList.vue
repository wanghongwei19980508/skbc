<template>
  <Row>
    <Col>
    <panel class="container">
      <div slot="title">{{ $t("m.Courses") }}</div>
      <div slot="extra">
        <ul class="filter">
          <li>
            <Input v-model="query.keyword" @on-enter="getCourseList" @on-click="getCourseList" placeholder="keyword"
              icon="ios-search-strong" />
          </li>
          <li>
            <Button type="info" @click="onReset">
              <Icon type="refresh"></Icon>
              {{ $t("m.Reset") }}
            </Button>
          </li>
        </ul>
      </div>
      <el-tabs v-model="tabsValue" type="card" :before-leave="handleBeforeLeave" @tab-click="getCourseList()">
        <el-tab-pane :key="item.name" v-for="item in tabs" :label="item.title" :name="item.name">
          <Row :gutter="16" v-loading="loading">
            <el-result icon="info" :title="query.keyword == '' ? item.tips : '未找到相关课程'"
              v-if="tabCourses[item.name].length == 0">
              <template slot="extra">
                <el-button type="primary" size="medium" icon="el-icon-refresh" @click="getCourseList()">刷新</el-button>
              </template>
            </el-result>
            <Col span="8" v-for="(course, c_index) in tabCourses[item.name]" :key="c_index" class="course_card">
            <Card>
              <el-carousel :interval="6000" :height="bannerHeight + 'px'" type="card">
                <el-carousel-item v-for="(pic, p_index) in course.pics" :key="p_index">
                  <el-image :src="pic" :fit="fill" :preview-src-list="course.pics" class="inheritheight"></el-image>
                </el-carousel-item>
                <el-carousel-item>
                  <el-image :src="qcode" class="inheritheight"> </el-image>
                </el-carousel-item>
              </el-carousel>
              <div style="text-align: center">
                <el-button type="text" @click="goCourse(course.id)">
                  <h3>{{ course.title }}</h3>
                </el-button>
              </div>
            </Card>
            </Col>
          </Row>
        </el-tab-pane>
        <el-tab-pane name="manageTab">
          <span slot="label"><i class="el-icon-setting"></i>管理标签页</span>
          <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
          <div style="margin: 15px 0"></div>
          <el-checkbox-group v-model="checkedTabs" @change="handleCheckedTabsChange">
            <el-checkbox v-for="tab in totalTabs" :label="tab.title" :key="tab.title">{{ tab.title }}</el-checkbox>
          </el-checkbox-group>
          <div style="margin: 30px 0"></div>
        </el-tab-pane>
      </el-tabs>
    </panel>
    <Pagination :total="total" :page-size.sync="query.limit" @on-change="pushRouter" @on-page-size-change="pushRouter"
      :current.sync="query.page" :show-sizer="true"></Pagination>
    </Col>
  </Row>
</template>
    
<script>
import Pagination from "@oj/components/Pagination";
import api from "../../api.js";
import { COURSE_ROLE_V } from "@/utils/constants";

const tabOptions = [
  {
    title: "我加入的班级",
    name: "join",
    tips: "您还没有加入任何班级",
  },
  {
    title: "我教授的班级",
    name: "teach",
    tips: "您还没有教授任何班级",
  },
  {
    title: "我管理的班级",
    name: "manage",
    tips: "您还没有管理任何班级",
  },
];
export default {
  name: "CourseList",
  components: {
    Pagination,
  },
  data() {
    return {
      limit: 20,
      total: 0,
      query: {
        keyword: "",
        page: 1,
        limit: 10,
      },
      tabsValue: "join",
      checkAll: false,
      checkedTabs: ["我加入的班级", "我教授的班级", "我管理的班级"],
      tabs: [
        {
          title: "我加入的班级",
          name: "join",
          tips: "您还没有加入任何班级",
        },
        {
          title: "我教授的班级",
          name: "teach",
          tips: "您还没有教授任何班级",
        },
        {
          title: "我管理的班级",
          name: "manage",
          tips: "您还没有管理任何班级",
        },
      ],
      tabCourses: {
        join: [],
        teach: [],
        manage: [],
      },
      loading: true,
      totalTabs: tabOptions,
      isIndeterminate: true,
      screenWidth: 0,
      bannerHeight: 0,
      qcode: "/public/upload/qcode.jpg",
    };
  },
  mounted() {
    this.init();
    // 轮播图自适应高度处理 ref: https://blog.csdn.net/ZHANGYANG_1109/article/details/121103486
    this.screenWidth = window.innerWidth;
    this.bannerHeight = (200 / 1550) * this.screenWidth;
    if (sessionStorage.getItem("courseCheckedTabs") !== null) {
      this.checkedTabs = sessionStorage.getItem("courseCheckedTabs").split(',')[0] != '' ? sessionStorage.getItem("courseCheckedTabs").split(',') : []
      let checkedCount = this.checkedTabs.length;
      this.checkAll = checkedCount === tabOptions.length;
      this.tabs = tabOptions.filter((tab) => {
        return this.checkedTabs.indexOf(tab.title) > -1;
      });
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < tabOptions.length;
      this.tabsValue = this.tabs.length === 0 ? "manageTab" : this.tabs[0].name
    }
    window.onresize = () => {
      this.screenWidth = window.innerWidth;
      this.bannerHeight = (200 / 1550) * this.screenWidth;
    };
  },
  methods: {
    init() {
      this.routeName = this.$route.name;
      let query = this.$route.query;
      this.query.keyword = query.keyword || "";
      this.query.page = parseInt(query.page) || 1;
      if (this.query.page < 1) {
        this.query.page = 1;
      }
      this.query.limit = parseInt(query.limit) || 10;
      this.getCourseList();
    },
    handleBeforeLeave(activeName, oldActiveName) {
      // this.courses.pop();
      return true;
    },
    handleCheckAllChange(val) {
      this.checkedTabs = val
        ? ["我加入的班级", "我教授的班级", "我管理的班级"]
        : [];
      this.tabs = val ? tabOptions : [];
      this.isIndeterminate = false;
      this.tabsValue = "manageTab";
      sessionStorage.setItem("courseCheckedTabs", this.checkedTabs)
    },
    handleCheckedTabsChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === tabOptions.length;
      this.tabs = tabOptions.filter((tab) => {
        return value.indexOf(tab.title) > -1;
      });
      this.isIndeterminate = checkedCount > 0 && checkedCount < tabOptions.length;
      this.tabsValue = "manageTab";
      sessionStorage.setItem("courseCheckedTabs", this.checkedTabs)
    },
    goCourse(id) {
      this.$router.push({
        name: "course-details",
        params: { courseID: id },
      });
    },
    getCourseList() {
      setTimeout(()=>{
        let offset = (this.query.page - 1) * this.query.limit;
        if (this.tabsValue != 'manageTab') {
          this.loading = true
          api.getCoursesAsRole(
            offset,
            this.limit,
            this.query,
            COURSE_ROLE_V[this.tabsValue]
          ).then((res) => {
            this.tabCourses[this.tabsValue] = res.data.data.results;
            this.loading = false
          }).catch((res) => {
            this.loading = false
          });
        }
      },100)
    },
    pushRouter() {
      this.$router.push({
        name: "course-list",
        query: utils.filterEmptyValue(this.query),
      });
    },
    onReset() {
      this.$router.push({ name: "course-list" });
    },
  },
};
</script>
    
<style lang="less" scoped>
.container {
  margin-bottom: 2%;
  padding-left: 1%;
  padding-right: 1%;
}

.course_card {
  margin-bottom: 1%;
}

.inheritheight {
  width: 100%;
  height: inherit;
}
</style>
    