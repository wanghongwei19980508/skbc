<template>
  <div class="container">
    <div>
      <el-menu class="vertical_menu" :router="true" :default-active="route_name">
        <div class="logo">
          <el-carousel :interval="6000" :height="bannerHeight + 'px'" type="card">
            <el-carousel-item v-for="(pic, p_index) in course.pics" :key="p_index">
              <el-image :src="pic" :fit="fill" :preview-src-list="course.pics" class="inheritheight"></el-image>
            </el-carousel-item>
            <el-carousel-item>
              <el-image :src="qcode" class="inheritheight"> </el-image>
            </el-carousel-item>
          </el-carousel>
        </div>
        <el-menu-item index="details" :route="{ name: 'course-details', params: { courseID: courseID } }">
          <i class="el-icon-document"></i>
          <span>课程概要</span>
        </el-menu-item>
        <el-menu-item index="lessons" :route="{ name: 'lessons', params: { courseID: courseID } }">
          <i class="el-icon-date"></i>
          <span>课程目录</span>
        </el-menu-item>
        <el-menu-item index="members" :route="{ name: 'members', params: { courseID: courseID } }">
          <i class="el-icon-user"></i>
          <span>课程成员</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="content-app">
      <transition name="fadeInUp" mode="out-in">
        <router-view></router-view>
      </transition>
      <div v-if="route_name === 'details'">
        <Panel>
          <div slot="title">
            <h3>课程概要</h3>
          </div>
          <div v-html="course.description" style="font-size: large"></div>
          <el-divider></el-divider>
        </Panel>
      </div>
    </div>
  </div>
</template>
      
<script>
import Pagination from "@oj/components/Pagination";
import api from "../../api.js";
import time from "@/utils/time";
import { CONTEST_STATUS_REVERSE } from "@/utils/constants";
import Panel from "../../../admin/components/Panel.vue";

export default {
  name: "Course",
  components: {
    Pagination,
    Panel,
  },
  data() {
    return {
      total: 0,
      query: {
        keyword: "",
        page: 1,
        limit: 10,
      },
      courseID: "",
      tabsValue: "join",
      course: {},
      screenWidth: 0,
      bannerHeight: 0,
      qcode: "/public/upload/qcode.jpg",
      lessons: [],
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      route_name: "details", // 当前激活菜单的 index
    };
  },
  mounted() {
    this.courseID = this.$route.params.courseID;
    this.route_name = this.$route.name === 'course-details' ? 'details' : this.$route.name;
    this.init();
    // 轮播图自适应高度处理 ref: https://blog.csdn.net/ZHANGYANG_1109/article/details/121103486
    this.screenWidth = window.innerWidth;
    this.bannerHeight = (100 / 1550) * this.screenWidth;
    window.onresize = () => {
      this.screenWidth = window.innerWidth;
      this.bannerHeight = (100 / 1550) * this.screenWidth;
    };
  },
  watch: {
    $route(newVal) {
      this.route_name = newVal.name === 'course-details' ? 'details' : newVal.name;
      this.courseID = newVal.params.courseID;
    },
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    init() {
      this.getCourse();
      // this.getLessonList();
    },
    getCourse() {
      api.getCourse(this.courseID).then((res) => {
        this.course = res.data.data;
      });
    },
    getDuration(startTime, endTime) {
      return time.duration(startTime, endTime);
    },
  },
};
</script>
      
<style lang="less" scoped>
a {
  background-color: transparent;
}

a:active,
a:hover {
  outline-width: 0;
}

img {
  border-style: none;
}

.container {
  overflow: auto;
  font-weight: 400;
  height: 100%;
  -webkit-font-smoothing: antialiased;
  background-color: #edecec;
  overflow-y: scroll;
  min-width: 1000px;
}

* {
  box-sizing: border-box;
}

#header {
  text-align: right;
  padding-left: 210px;
  padding-right: 30px;
  line-height: 50px;
  height: 50px;
  background: #f9fafc;

  .screen-full {
    margin-right: 8px;
  }
}

.content-app {
  margin-top: 10px;
  padding-top: 0px;
  padding-right: 10px;
  padding-left: 210px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate(0, 30px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

.vertical_menu {
  overflow: auto;
  width: 205px;
  height: 100%;
  position: fixed !important;
  z-index: 100;
  top: 60px;
  bottom: 0;
  left: 0;

  .logo {
    margin: 20px 0;
    text-align: center;

    img {
      background-color: #fff;
      border-radius: 50%;
      border: 3px solid #fff;
      width: 75px;
      height: 75px;
    }
  }
}
</style>
      