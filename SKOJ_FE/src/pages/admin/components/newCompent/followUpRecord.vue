<template>
  <div>
    <el-button @click="followUpPopoverdialogVisible = true" type="warning" size="mini">添加跟进记录</el-button>
    <div v-if="followUpPlanData.length">
      <p>跟进计划</p>
      <el-card shadow="hover" v-for="(item, key) in  followUpPlanData " :key="'followUpPlan' + key" class="followUpPlan">
        <div v-if="item.follow_up_person">
          {{ item.follow_up_person.username }} {{ item.follow_up_person.phone }}
          {{ new Date(item.plan_follow_up_time).Format("yyyy-MM-dd HH:mm:ss") }}
          <span class="stage"
            :style="new Date(item.plan_follow_up_time) > new Date() ? '' : 'color: red; border-color: red;'">
            {{ new Date(item.plan_follow_up_time) > new Date() ? '未完成' : '已逾期' }}
          </span>
          <el-button style="float: right;color: #ff7519;" @click="followUp(item)" type="text" size="medium">跟进</el-button>
        </div>
        <div>
          {{ item.follow_up_content }}
        </div>
      </el-card>
    </div>
    <p>跟进记录</p>
    <el-card shadow="hover" v-for="( item, key ) in  followUpData " :key="'followUp' + key" class="followUpCard">
      <div class="followUpBox">
        <div v-if="item.follow_up_person">
          {{ item.follow_up_person.username }} {{ item.follow_up_person.phone }}
          {{ new Date(item.plan_follow_up_time).Format("yyyy-MM-dd HH:mm:ss") }}
          <span class="stage">已完成</span>
          <span class="display">{{ `${item.follow_up_method} · ${item.follow_up_stage} ` }}</span>
        </div>
        <div v-if="item.trialClass" class="trialClassBox">
          <p>已约试听课：<span>{{ item.trialClass.name }}</span></p>
          <p>试听班级：<span>{{ item.trialClass.class }}</span></p>
          <p>授课老师：<span>{{ item.trialClass.teacher }}</span></p>
          <p>授课时间：<span>{{ item.trialClass.time }}</span></p>
        </div>
        <div v-else>
          {{ item.follow_up_content }}
        </div>
      </div>
    </el-card>
    <followUpPopover ref="followUpPopoverRef" :dialogVisible="followUpPopoverdialogVisible" :userData="userData"
      @closeFollowUpPopover="closeFollowUpPopover()">
    </followUpPopover>
  </div>
</template>
  
<script>
import api from "@admin/api"
import followUpPopover from "@admin/components/newCompent/followUpPopover.vue"

export default {
  name: 'followUpRecord',
  components: {
    followUpPopover
  },
  props: {
    userData: { // 用户信息
      type: Object,
      default: () => { }
    }
  },
  data() {
    return {
      followUpPopoverdialogVisible: false, // 新增跟进记录弹窗
      followUpPlanData: [], // 跟进计划
      followUpData: [] // 跟进记录
    }
  },
  mounted() {

  },
  methods: {
    // 获取数据
    getData() {
      api.getFollowUpRecordList({ student: this.userData.id }).then((res) => {
        let followUpData = [], followUpPlanData = []
        res.data.data.results.map((item) => {
          if (item.actual_follow_up_time) {
            followUpData.push(item)
          } else {
            followUpPlanData.push(item)
          }
        })
        this.followUpData = followUpData
        this.followUpPlanData = followUpPlanData
      })
    },
    // 修改跟进记录
    followUp(row) {
      this.$refs['followUpPopoverRef'].searchData = row
      this.$refs['followUpPopoverRef'].parentComponentControl = true
      this.followUpPopoverdialogVisible = true
      setTimeout(() => {
        this.$refs['followUpPopoverRef'].showTable = false
      }, 0);
    },
    // 关闭跟进记录
    closeFollowUpPopover() {
      this.followUpPopoverdialogVisible = false
      this.getData()
    },
  },
  watch: {
    userData: {
      deep: true,
      handler: function (newValue, oldValue) {
        if (newValue.id != oldValue.id) this.getData()
      }
    }
  }
}
</script>
<style scoped lang="less">
.followUpPlan {
  background-color: #ececec;
  margin: 20px 10px;

  div {
    line-height: 2.5;

    .stage {
      color: #7c7676;
      border: 1px solid #7c7676;
      margin: 10px;
      padding: 5px 10px;
    }
  }
}

.followUpCard {
  margin: 20px 10px;

  .followUpBox {
    line-height: 2.5;

    div {
      .stage {
        color: green;
        border: 1px solid green;
        margin: 10px;
        padding: 5px 10px;
      }

      .display {
        background-color: #d4f7d4;
        border-radius: 20px;
        padding: 5px 10px;
        color: green;
        margin: 10px;
      }
    }

    .trialClassBox {
      display: flex;
      flex-direction: column;

      p {
        height: 25px;
        margin: 0;
      }
    }
  }
}

/deep/ .el-card__body {
  padding: 10px 20px;
}
</style>