<template>
  <div>
    <el-skeleton :loading="loading">
      <Panel>
        <div slot="title">
          <h3>{{ $t('m.Course_Member') }}</h3>
        </div>
        <el-row>
          <el-col :span="12">
            <h2>{{ $t('m.Lecturer') }}</h2>
            <el-result icon="info" :title="$t('m.Not_Set') + $t('m.Lecturer')"
              v-if="lecturerList.length == 0"></el-result>
            <div class="userBox" v-else>
              <div class="userList" v-for="(item, index) in lecturerList" :key="index" @click="toUserHome(item)">
                <Avatar :src="item.pic ? item.pic : 'https://i.loli.net/2017/08/21/599a521472424.jpg'" size="large" />
                <p>{{ item.real_name != null ? item.real_name : item.username }}</p>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <h2>{{ $t('m.Class_Teacher') }}</h2>
            <el-result icon="info" :title="$t('m.Not_Set') + $t('m.Class_Teacher')"
              v-if="managerList.length == 0"></el-result>
            <div class="userBox" v-else>
              <div class="userList" v-for="(item, index) in managerList" :key="index" @click="toUserHome(item)">
                <Avatar :src="item.pic ? item.pic : 'https://i.loli.net/2017/08/21/599a521472424.jpg'" size="large" />
                <p>{{ item.real_name != null ? item.real_name : item.username }}</p>
              </div>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <h2>{{ $t('m.Trainee') }}</h2>
            <el-result icon="info" :title="$t('m.Not_Set') + $t('m.Trainee')" v-if="studentList.length == 0"></el-result>
            <div class="userBox" v-else>
              <div class="userList" v-for="(item, index) in studentList" :key="index" @click="toUserHome(item)">
                <Avatar :src="item.pic ? item.pic : 'https://i.loli.net/2017/08/21/599a521472424.jpg'" size="large" />
                <p>{{ item.real_name != null ? item.real_name : item.username }}</p>
              </div>
            </div>
          </el-col>
        </el-row>
      </Panel>
    </el-skeleton>
  </div>
</template>
  
<script>
import api from "../../../api.js";
import Panel from "../../../../admin/components/Panel.vue";
export default {
  components: {
    Panel,
  },
  data() {
    return {
      courseID: "",
      loading: true,
      studentList: [], // 学员
      lecturerList: [], // 讲师
      managerList: [], // 班主任
    };
  },
  mounted() {
    this.courseID = this.$route.params.courseID;
    this.init();
  },
  methods: {
    init() {
      this.getMemberList();
      this.loading = false;
    },
    getMemberList() {
      api.getMemberList(this.courseID).then((res) => {
        let MemberList = res.data.data;
        let roleList = [[], [], []]
        MemberList.forEach((item) => {
          roleList[item.role].push(item.user)
        })
        this.studentList = roleList[0]
        this.lecturerList = roleList[1]
        this.managerList = roleList[2]
      });
    },
    toUserHome(row) {
      this.$router.push({
        name: "user-home",
        query: { username: row.username },
      });
    },
  },
};
</script>
  
<style lang="less" scoped>
.userBox {
  display: flex;
  flex-wrap: wrap;
  padding: 30px 10px;
  min-height: 120px;

  .userList {
    height: 120px;
    width: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .ivu-avatar-large {
      height: 50px;
      width: 50px;
      border-radius: 50%;
      cursor: pointer;
    }

    p {
      height: 40px;
      line-height: 40px;
      font-size: 18px;
      margin-top: 5px;
      overflow: hidden;
      width: 100%;
      text-align: center;
      white-space: nowrap;
      text-overflow: ellipsis;
      cursor: pointer;
    }
  }
}
</style>