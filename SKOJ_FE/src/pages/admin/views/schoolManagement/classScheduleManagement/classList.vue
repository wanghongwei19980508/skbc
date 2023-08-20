<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Class_Schedule_Management')">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <formSubmit class="headerInput" labelWidth="100px" ref="headerSubmitForm" size="mini" :searchData="headerData"
          :searchForm="headerFormList" :successBtn="false" :cancelBtn="false">
          <template #headerButton="scope">
            <el-button type="primary" @click="search">搜索</el-button>
            <el-button @click="headerDataClear">重置</el-button>
            <el-button @click="expansion = !expansion" v-if="headerForm.length > 2">{{ expansion ? '收起' : '展开'
            }}</el-button>
          </template>
        </formSubmit>
        <el-tab-pane label="时间课表" name="timeSchedule">
        </el-tab-pane>
        <el-tab-pane label="老师课表" name="teacherSchedule">
        </el-tab-pane>
        <el-tab-pane label="班级课表" name="classSchedule">
        </el-tab-pane>
      </el-tabs>
      <transition name="fadeInUp" mode="out-in">
        <router-view ref="child"></router-view>
      </transition>
    </Panel>
    <el-dialog :visible.sync="changeCourseVisible" title="按天调课">
      <span>从</span>
      <el-date-picker v-model="changeCourseDate.oldValue" type="date" placeholder="选择日期"></el-date-picker>
      <span>调整到</span>
      <el-date-picker v-model="changeCourseDate.newValue" type="date" placeholder="选择日期"></el-date-picker>
      <div slot="footer">
        <el-button @click="changeCourse">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>
    
<script>
import formSubmit from "@admin/components/vFrom.vue"

const headerForm = [
  [
    {
      span: 8,
      type: "select",
      label: "所属课程",
      prop: "source",
      options: [],
      placeholder: "请选择所属课程",
    },
    {
      span: 8,
      type: "select",
      label: "上课班级",
      prop: "class",
      options: [],
      placeholder: "请选择上课班级",
    },
    {
      span: 8,
      type: "select",
      label: "老师",
      prop: "teacher",
      options: [],
      placeholder: "请选择老师",
    },
  ],
  [
    {
      span: 8,
      type: "input",
      label: "学员姓名",
      prop: "name",
      placeholder: "请输入学员姓名",
    },
    {
      span: 8,
      type: "select",
      label: "开课情况",
      prop: "courseOpeningSituation",
      options: [
        { label: '已取消', value: 1 },
        { label: '未取消', value: 2 }
      ],
      placeholder: "请选择开课情况",
    },
    {
      span: 8,
      type: "select",
      label: "班级类型",
      prop: "ClassType",
      options: [
        { label: '班课', value: 1 },
        { label: '一对一', value: 2 }
      ],
      placeholder: "请选择班级类型",
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "新建排课",
      handle: (data) => {
        console.log(data);
      }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "按天调课",
      handle: (data) => {
        console.log(data);
      }
    },
    {
      span: 14,
    }
  ]
]

export default {
  name: "classList",
  components: {
    formSubmit
  },
  data() {
    return {
      activeName: 'timeSchedule',
      headerData: {}, // 搜索数据
      expansion: false, // 展开收齐
      headerForm: headerForm, // 搜索框
      changeCourseVisible: false, //调课 dialog
      changeCourseDate: { // 调课数据
        oldValue: new Date(),
        newValue: new Date()
      }
    };
  },
  mounted() {
    this.$router.push({
      name: 'timeSchedule'
    })
    this.changeFormData() // 页面数据
    this.configProperty() // 配置回调函数
  },
  methods: {
    // 切换视图
    handleClick(tab, event) {
      this.$router.push({
        name: tab.name,
      })
      this.changeFormData()
    },
    // 页面数据
    changeFormData() {
      let Data = {}
      this.headerForm.forEach(item => {
        item.forEach(i => {
          if (i.prop) Data[i.prop] = undefined
        })
      })
      this.headerData = Data
    },
    // 配置回调函数
    configProperty() {
      this.headerForm[2][0].handle = (scope) => {
        this.$refs.child.handleDateSelect()
      }
      this.headerForm[2][1].handle = (scope) => {
        this.changeCourseVisible = true
        this.changeCourseDate = {
          oldValue: new Date(),
          newValue: new Date()
        }
      }
    },
    // 搜索
    search() {
      this.$store.commit('classScheduleHeaderData', JSON.parse(JSON.stringify(this.headerData)))
    },
    // 搜索重置
    headerDataClear() {
      for (let item in this.headerData) {
        this.headerData[item] = undefined
      }
    },
    // 确认调课
    changeCourse() {
      this.changeCourseVisible = false
      // 请求数据
    },
  },
  computed: {
    headerFormList() {
      let list = []
      if (this.expansion) {
        for (let i = 0; i < this.headerForm.length; i++) {
          let [...arr1] = this.headerForm[i];
          list.push(arr1);
        }
      } else {
        if (this.headerForm.length > 1) {
          let [...arr1] = this.headerForm[0];
          list.push(arr1);
          let [...arr2] = this.headerForm[this.headerForm.length - 1];
          list.push(arr2);
        } else {
          let [...arr1] = this.headerForm[0];
          list.push(arr1);
        }
      }
      list[list.length - 1].push({
        span: 6,
        type: "slot",
        prop: "headerButton",
      })
      return list
    }
  },
  watch: {
  },
};
</script>
  
<style lang="less" scoped>
.baseInfo {
  padding: 0 10px 0;
}
</style>