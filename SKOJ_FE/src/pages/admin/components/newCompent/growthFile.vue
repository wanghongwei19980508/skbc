
<template>
  <div class="baseInfo">
    <el-card shadow="hover" v-for="(item, key) in  growthFileData " :key="'growthFilePlan' + key" class="growthFilePlan">
      <el-tag>{{ item.type }}</el-tag><span class="teacher">{{ item.teacher.name }}</span> <el-button
        @click="viewComments(item)" type="warning" size="mini" style="float: right;">查看评论</el-button>
      <div class="time">{{ item.time }}</div>
      <div class="rate">
        <span class="">综合评分</span><el-rate disabled score-template="{value}" v-model="item.comprehensiveScore"></el-rate>
      </div>
      <div class="rate">
        <span class="">课堂表现</span><el-rate disabled score-template="{value}"
          v-model="item.classroomPerformance"></el-rate>
      </div>
      <div class="rate">
        <span class="">作业情况</span><el-rate disabled score-template="{value}" v-model="item.operationCondition"></el-rate>
      </div>
      <div class="rate">
        <span class="">课后点评</span>{{ item.content }}
      </div>
    </el-card>
    <el-dialog :visible.sync="dialogVisible" :title="'评价详情'">
      <div class="studentContent">
        <div class="userBox">
          <el-avatar :size="40" :src="viewCommentsData.teacher.avatar" @error="errorHandler">
            <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png" />
          </el-avatar>
          <div class="name">{{ viewCommentsData.teacher.name }}</div>
        </div>
        <div class="date-info">
          <span class="date">
            <span class="icon iconfont" style="margin-right: 5px; color: rgb(255, 133, 52);"></span>
            {{ viewCommentsData.class.time }}
          </span>
          <span class="title">
            <span class="icon iconfont" style="margin-right: 5px; color: rgb(255, 133, 52);"></span>
            {{ viewCommentsData.class.title }}
          </span>
          <span class="name">{{ viewCommentsData.class.teacher }}</span>
        </div>
      </div>
      <el-divider></el-divider>
      <div class="viewCommentsContent">
        <div class="rate">
          <span class="">综合评分</span><el-rate disabled score-template="{value}"
            v-model="viewCommentsData.comprehensiveScore"></el-rate>
        </div>
        <div class="rate">
          <span class="">课堂表现</span><el-rate disabled score-template="{value}"
            v-model="viewCommentsData.classroomPerformance"></el-rate>
        </div>
        <div class="rate">
          <span class="">作业情况</span><el-rate disabled score-template="{value}"
            v-model="viewCommentsData.operationCondition"></el-rate>
        </div>
      </div>
      <el-divider></el-divider>
      <div class="contentBox">
        <span class="">课后点评</span>{{ viewCommentsData.content }}
      </div>
    </el-dialog>
  </div>
</template>
<script>
import api from "@admin/api";

export default {
  name: "growthFile",
  components: {
  },
  data() {
    return {
      growthFileData: [],
      dialogVisible: false,
      viewCommentsData: {
        teacher: { name: '', avatar: '' },
        class: { time: '', title: '', teacher: '' },
        content: ''
      }
    };
  },
  mounted() {
  },
  methods: {
    // 获取数据
    getTableData() {
      this.growthFileData = [
        { type: '课后评价', teacher: { name: '老师' }, class: { time: '2023-04-29 19:00 - 20:45', title: '【书克】C4-俊仁老师(六19:00)', teacher: '俊仁老师' }, time: '时间', comprehensiveScore: 3, classroomPerformance: 4, operationCondition: 5, content: '评价' },
        { type: '课后评价', teacher: { name: '老师' }, class: { time: '2023-04-29 19:00 - 20:45', title: '【书克】C4-俊仁老师(六19:00)', teacher: '俊仁老师' }, time: '时间', comprehensiveScore: 3, classroomPerformance: 4, operationCondition: 5, content: '评价' },
        { type: '课后评价', teacher: { name: '老师' }, class: { time: '2023-04-29 19:00 - 20:45', title: '【书克】C4-俊仁老师(六19:00)', teacher: '俊仁老师' }, time: '时间', comprehensiveScore: 3, classroomPerformance: 4, operationCondition: 5, content: '评价' },
      ]
    },
    viewComments(row) {
      this.viewCommentsData = row
      this.dialogVisible = true
    },
    // 图片加载失败
    errorHandler() {
      return true
    },
  },
  watch: {
  },
  computed: {
  }
};
</script>
                
<style lang="less" scoped>
.baseInfo {
  padding: 10px 10px 0;

  .growthFilePlan {
    // background-color: #ececec;
    margin: 20px 10px;

    .teacher {
      margin: 0 10px;
    }

    .time {
      font-size: 12px;
      color: #b3b3b3;
      margin: 0 10px 20px;
    }

    .rate {
      display: flex;
      height: 30px;
      align-items: flex-start;

      span {
        margin: 0 20px;
      }
    }
  }

  .studentContent {
    .userBox {
      display: flex;
      align-items: center;
      padding: 0px 20px 10px;

      .name {
        margin-left: 10px;
        font-size: 15px;
        color: #333;
      }
    }

    .date-info {
      padding: 10px 20px;
    }
  }

  .viewCommentsContent {
    .rate {
      display: flex;
      height: 40px;
      align-items: flex-start;

      span {
        margin: 0 20px;
      }
    }
  }

  .contentBox {
    min-height: 180px;
  }
}
</style>