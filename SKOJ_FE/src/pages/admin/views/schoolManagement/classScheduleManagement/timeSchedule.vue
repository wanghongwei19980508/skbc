<template>
  <div>
    <FullCalendar ref="myCalendar" :options="calendarOptions" />
    <div id="actionBar" class="actionBar"
      :style="'left:' + actionBarOption.x + 'px; top:' + actionBarOption.y + 'px;visibility:' + actionBarOption.display + ';'"
      ref="actionBarRef" @mouseover="mouseOver" @mouseleave="mouseLeave">
      <div class="info-top">
        <div class="info-detail-title">{{ classOptions.class }}</div>
        <div class="time">{{ classOptions.time }}</div>
        <div class="info-item">
          <div class="info-item-left"><i class="el-icon-date"></i>授课课程：<span>{{ classOptions.course }}</span>
          </div>
        </div>
        <div class="info-item">
          <div class="info-item-left"><i class="el-icon-s-custom"></i>上课老师：<span>{{ classOptions.teacher ?
            classOptions.teacher.join() : '' }}</span>
          </div>
        </div>
        <div class="info-item">
          <div class="info-item-left"><i class="el-icon-reading"></i>上课教室：<span>{{ classOptions.classRoom }}</span>
          </div>
        </div>
        <div class="info-item">
          <div class="info-item-left"><i class="el-icon-user-solid"></i>人数/容量：<span>{{
            classOptions.studentNum / classOptions.classCapacity }}(可超额)</span></div>
          <el-progress v-if="classOptions.studentNum" :percentage="classOptions.studentNum / classOptions.classCapacity * 100"></el-progress>
        </div>
        <el-divider></el-divider>
        <div class="info-item">
          <div class="info-item-left"><i class="el-icon-user"></i>上课学员：<span>{{ classOptions.student }}</span>
          </div>
        </div>
      </div>
      <div class="info-bottom">
        <el-divider></el-divider>
        <div v-if="this.params" class="buttonBox">
          <el-button :type="'success'" @click="audition(classOptions)">试听</el-button>
        </div>
        <div v-else class="buttonBox">
          <el-button :type="'success'" @click="rollCall(classOptions)">点名</el-button>
          <el-button :type="'success'" @click="adjust(classOptions)">调整课程</el-button>
          <el-button :type="'success'" @click="viewDetails(classOptions)">查看详情</el-button>
        </div>
      </div>
    </div>
    <courseDetailsDrawer :searchData="modifyCourseData" :drawer="courseDetailsDrawer" :title="'课程详情'"
      @fromCancel="handleClose" @adjust="adjust">
    </courseDetailsDrawer>
    <courseArrangementDrawer ref="courseArrangementDrawerRef" :searchData="searchData" :drawer="courseArrangementDrawer"
      :title="'新建排课'" @fromCancel="handleClose" @fromSubmit="onSubmit">
    </courseArrangementDrawer>
    <modifyCourseDrawer :searchData="modifyCourseData" :drawer="modifyCourseDrawer" :title="'编辑排课'"
      @fromCancel="handleClose" @fromSubmit="onSubmit">
    </modifyCourseDrawer>
  </div>
</template>
<script>
// https://fullcalendar.io/docs#toc   // 日历官网
// https://blog.csdn.net/supingemail/article/details/48371927 // 日历中文官网
import { mapGetters } from 'vuex'
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import listPlugin from '@fullcalendar/list'

import courseArrangementDrawer from "@admin/components/newCompent/courseArrangementDrawer.vue"
import modifyCourseDrawer from "@admin/components/newCompent/modifyCourseDrawer.vue"
import courseDetailsDrawer from "@admin/components/newCompent/courseDetailsDrawer.vue"

export default {
  name: 'timeSchedule',
  components: {
    FullCalendar,
    courseArrangementDrawer,
    modifyCourseDrawer,
    courseDetailsDrawer
  },
  data() {
    return {
      courseArrangementDrawer: false, // 新增课程抽屉
      modifyCourseDrawer: false, // 修改课程抽屉
      courseDetailsDrawer: false, // 课程抽详情屉
      modifyCourseData: {}, // 修改课程参数
      searchData: {}, // 新增课程参数
      event: {}, // 当前视图数据
      params: {}, // router参数  判断是否为试听
      calendarOptions: { // 日历配置
        // 引入的插件，比如fullcalendar/daygrid，fullcalendar/timegrid引入后才可显示月，周，日
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin, listPlugin],
        initialView: 'timeGridWeek', // 默认为那个视图（月：dayGridMonth，周：timeGridWeek，日：timeGridDay）
        firstDay: 1, // 设置一周中显示的第一天是哪天，周日是0，周一是1，类推
        locale: 'zh-cn', // 切换语言，当前为中文
        eventBackgroundColor: 'rgb(255,0,0)', // 全部日历日程背景色
        // eventMinHeight: 100, // 设置事件的最小高度
        // eventShortHeight: 40, // 时间title高度
        aspectRatio: (window.innerWidth - 65) / (window.innerHeight - 100), // 设置日历单元格宽度与高度的比例。
        displayEventTime: true, // 是否显示时间
        allDaySlot: false, // 周，日视图时all-day是否显示
        headerToolbar: { // 日历头部按钮位置
          left: '',
          center: 'prevYear,prev title next,nextYear',
          right: 'today dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: { // 按钮对应显示
          today: '今天',
          month: '月',
          week: '周',
          day: '日'
        },
        slotLabelFormat: {
          hour: 'numeric',
          minute: '2-digit',
          meridiem: 'short',
          hour12: false // 设置时间为24小时
        },
        editable: true, // 是否可以进行（拖动、缩放）修改
        eventStartEditable: true, // Event日程开始时间可以改变，默认true，如果是false其实就是指日程块不能随意拖动，只能上下拉伸改变他的endTime
        eventDurationEditable: true, // Event日程的开始结束时间距离是否可以改变，默认true，如果是false则表示开始结束时间范围不能拉伸，只能拖拽
        selectable: true, // 是否可以选中日历格
        selectMirror: true, // 是否在用户拖动时绘制“占位符”事件
        selectMinDistance: 0, // 选中日历格的最小距离
        dayMaxEvents: 6, // 在月视图中，给定一天内的最大事件数
        weekends: true, // 是否在任何日历视图中展示星期六/星期日
        navLinks: true, // 确定日名和周名是否可单击
        slotEventOverlap: false, // 相同时间段的多个日程视觉上是否允许重叠，默认true允许
        eventClick: this.handleEventClick, // 点击日历日程事件
        eventDrop: this.eventDrop, // 拖动日历日程事件
        eventResize: this.eventResize, // 修改日历日程大小事件
        select: this.handleDateSelect, // 选中日历格事件
        eventDidMount: this.eventDidMount, // 在元素被添加到DOM后立即调用。如果事件数据发生变化，则不会再次调用。
        datesSet: this.handleDatesRender,
        // loading: this.loadingEvent, // 视图数据加载中、加载完成触发（用于配合显示/隐藏加载指示器。）
        // selectAllow: this.selectAllow, //编程控制用户可以选择的地方，返回true则表示可选择，false表示不可选择
        eventMouseEnter: this.eventMouseEnter, // 鼠标滑过
        eventMouseLeave: this.eventMouseLeave, // 鼠标移出
        events: [
          {
            id: 1,
            title: '可以拖动、缩放',
            start: '2023-04-26 12:30',
            end: '2023-04-26 13:30',
            editable: true, //可以拖动、缩放
            className: 'rollCall', // 试听课标识
            backgroundColor: this.coloring(),
          },
          {
            id: 2,
            title: '可以拖动但不能缩放',
            start: '2023-04-26 12:30',
            end: '2023-04-26 13:30',
            editable: true,
            backgroundColor: this.coloring(),
          },
          {
            id: 3,
            title: 'event 2',
            start: '2023-04-26 12:30',
            end: '2023-04-26 13:30',
            color: 'red',
            editable: true,
            backgroundColor: this.coloring(),
          },
          {
            id: 4,
            title: '试听课',
            start: '2023-04-26 12:30',
            end: '2023-04-26 13:30',
            color: '#ff9f89',
            className: 'rollCall',
            backgroundColor: this.coloring(),
          },
        ],
      },
      actionBarOption: { // 文字提示
        x: '0',
        y: '0',
        display: 'hidden',
        blon: true
      },
      tabularData: [], // 当前时间的课程
      classOptions: {}, // 操作获取的课程参数
    }
  },
  mounted() {
    this.params = this.$route.params.row
    console.log(this.params);
  },
  methods: {
    // 鼠标划过的事件
    eventMouseEnter(event) {
      this.debounce(this.actionBarEvent(event))
    },
    // 防抖功能函数，接受传参
    debounce(fn) {
      let timeout = null;
      return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          fn.call(this, arguments);
        }, 1000);
      };
    },
    // 执行事件
    actionBarEvent(event) {
      this.classOptions = this.tabularData.map(item => { return item.id == event.event.id ? item.classOptions : '' })[0]
      this.$nextTick(() => {
        this.$set(this.actionBarOption, 'event', event.event)
        this.$set(this.actionBarOption, 'x', event.jsEvent.x - (this.$refs.actionBarRef.offsetWidth / 2))
        this.$set(this.actionBarOption, 'y', event.jsEvent.y - (this.$refs.actionBarRef.offsetHeight + 10) < 0 ? event.jsEvent.y + 20 : event.jsEvent.y - (this.$refs.actionBarRef.offsetHeight + 10))
      })
      this.actionBarOptionChage('visible')
    },
    // 鼠标移出的事件
    eventMouseLeave(event) {
      this.actionBarOptionChage('hidden')
    },
    // 标签移入事件
    mouseOver() {
      this.actionBarOptionChage('visible')
      this.$set(this.actionBarOption, 'blon', false)
    },
    // 标签移出事件
    mouseLeave() {
      this.actionBarOptionChage('hidden')
    },
    // 标签展示隐藏
    actionBarOptionChage(str) {
      setTimeout(() => {
        if (this.actionBarOption.blon) {
          this.$set(this.actionBarOption, 'display', str)
        }
        this.$set(this.actionBarOption, 'blon', true)
      }, 300)
    },
    // 课程拖拽事件
    eventDrop(event) {
      // delta, el, event, jsEvent, oldEvent, relatedEvents, revert, view
      console.log(event)
    },
    // 课程点击事件
    handleEventClick(event) {
      this.classOptions = this.tabularData.map(item => { return item.id == event.event.id ? item.classOptions : '' })[0]
      this.viewDetails(this.classOptions)
    },
    // 调整课程
    adjust(item) {
      this.modifyCourseData = item
      this.modifyCourseDrawer = true
    },
    // 课程详情
    viewDetails(item) {
      this.modifyCourseData = item
      this.courseDetailsDrawer = true
    },
    // 试听
    audition(item) {
      this.$confirm(`是否将同学安排进入${item.class}课次试听`, '提示').then(_ => {
        let data = Object.assign(item, this.params)
        console.log(data);
      }).catch(_ => { });
    },
    // 点击日程事件
    handleDateSelect(event) {
      // allDay, end, endStr, jsEvent, start, startStr, view
      // console.log(event)
      this.courseArrangementDrawer = true
    },
    // 提交
    onSubmit(row) {
      let { label, searchData } = row
      if (label === 'modifyCourseDrawer') { // 编辑排课

      } else if (label === 'courseArrangementDrawer') { // 新增排课
        let classDate = new Date(searchData.statDate).Format('yyyy-MM-dd HH:mm:ss')
        let selectEvent = {
          ...searchData,
          color: this.coloring(),
          backgroundColor: this.coloring(),
          start: classDate.slice(0, 11) + new Date(searchData.classTime[0]).Format('HH:mm'),
          end: classDate.slice(0, 11) + new Date(searchData.classTime[1]).Format('HH:mm'),
          editable: true,
          title: '新增排课',
          id: 12,
        }
        this.calendarOptions.events.push(selectEvent)
      }
    },
    // 关闭抽屉
    handleClose(row) {
      let { label, blon } = row
      if (blon) return this.courseDetailsDrawer = false
      this.$confirm('确认关闭？').then(_ => {
        if (label === 'modifyCourseDrawer') { // 编辑排课
          this.modifyCourseDrawer = false
        } else if (label === 'courseArrangementDrawer') { // 新增排课
          this.$refs['courseArrangementDrawerRef'].$refs['searchSubmitForm'].$refs['searchFormRef'].resetFields()
          this.courseArrangementDrawer = false
        } else if (label === 'courseDetailsDrawer') { // 新增排课
          this.courseDetailsDrawer = false
        }
      }).catch(_ => { });
    },
    // 获取视图时间
    handleDatesRender(event, search) {
      this.event = event
      this.tabularData = [
        {
          id: 1,
          title: '可以拖动、缩放',
          editable: true, //可以拖动、缩放
          classOptions: {
            class: '【书克】C2-万老师习题营（周三周六...',
            time: '04月19日(周三)19:00-20:30',
            start: '2023-04-19 12:30',
            end: '2023-04-19 13:30',
            classDate: new Date('2023-04-19 12:30'),
            classTime: [new Date('2023-04-19 12:30'), new Date('2023-04-19 13:30')],
            course: '信奥2习题营',
            teacher: ['小奥老师', '万老师'],
            classRoom: '暂无教室',
            studentNum: 7,
            classCapacity: 8,
            student: '查毅凡,陈锦辰,丁峻豪,荆晨熙,宋彦博,陶思成,杨昕怡',
            trialClass: true,
            classHour: 1,
          }
        },
      ]
    },
    // 随机颜色库
    coloring() {
      let r = Math.floor(Math.random() * 255)
      let g = Math.floor(Math.random() * 255)
      let b = Math.floor(Math.random() * 255)
      return `rgb(${r}, ${g}, ${b})`
    }
  },
  computed: {
    ...mapGetters(['classScheduleHeaderData']),
  },
  watch: {
    classScheduleHeaderData: {
      deep: true,
      handler: function (newvalue, oldV) {
        console.log(newvalue);
        this.handleDatesRender(this.event, newvalue)
      }
    }
  }
}
</script>
<style scoped lang="less">
.actionBar {
  position: fixed;
  width: 300px;
  background: #f5f2d6;
  z-index: 300;
  padding: 10px;
  border-radius: 10px;
  box-shadow: -1px 11px 12px 5px rgb(114 110 110);

  .info-top {
    .info-detail-title {
      overflow: hidden;
      text-overflow: ellipsis;
      -webkit-line-clamp: 2;
      line-height: 1.2;
      font-size: 18px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
    }

    .time {
      line-height: 1.2;
      font-size: 16px;
      margin: 8px 0;
    }

    .info-item {
      line-height: 1.2;
      font-size: 15px;
      margin: 5px 0;

      .info-item-left {
        line-height: 1.2;
      }
    }
  }

  .info-bottom {
    .buttonBox {
      display: flex;
      align-items: center;
      justify-content: space-around;

      button {
        width: 50%;
        margin: 0;
        border-radius: 0;
        border: 1px solid;
      }
    }
  }
}
</style>
<style lang="less">
.rollCall {
  background-image: url('../../../../../assets/试听.png');
  background-size: 30px 30px;
  background-position-x: calc(100% - 0px);
  background-origin: padding-box;
  background-repeat: no-repeat;
}

.el-divider--horizontal {
  margin: 12px 0;
}

.fc-toolbar-chunk:nth-child(2) {
  width: 50%;
  display: flex;
}

.fc .fc-timegrid-slot {
  height: 3em;
}
</style>
