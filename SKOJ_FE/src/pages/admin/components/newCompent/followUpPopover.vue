<template>
  <div>
    <el-dialog :visible="dialogVisible" @close="close" :title="'添加跟进记录'">
      <div v-if="showTable">
        <p style="background-color: #fff0e7;  line-height: 30px; padding: 10px 20px;">
          {{ `系统检测到此线索有${followUpPlanData.length}条跟进任务未开始或已逾期,请先选择要跟进的任务。` }}</p>
        <el-button style="float: right;" @click="followUp({
          follow_up_method: '',
          follow_up_stage: '',
          follow_up_content: '',
          next_follow_up_time: null,
          next_follow_up_task: null,
        })" type="text" size="small">添加新的跟进记录</el-button>
        <el-table :data="followUpPlanData" style="width: 100%">
          <el-table-column label="任务状态">
            <template #default="scope">
              {{ '未开始' }}
            </template>
          </el-table-column>
          <el-table-column prop="follow_up_person" label="跟进人">
            <template #default="scope">
              {{ scope.row.follow_up_person.username }}
            </template>
          </el-table-column>
          <el-table-column prop="plan_follow_up_time" label="计划时间" width="180">
            <template #default="scope">
              {{ new Date(scope.row.plan_follow_up_time).Format("yyyy-MM-dd HH:mm:ss") }}
            </template>
          </el-table-column>
          <el-table-column prop="follow_up_content" label="备注">
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="followUp(scope.row)" type="text" size="small">跟进</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else>
        <vFrom labelWidth="100px" ref="searchSubmitForm" size="default" :searchData="searchData" :searchForm="searchForm"
          @fromSubmit="onSubmit" :cancelBtn="false">
          <template slot="next_follow_up_task" slot-scope="row">
            <div style="width: 500px;" v-if="row.row.next_follow_up_time">
              <el-input type="textarea" :rows="2" placeholder="情输入下次跟进任务备注内容，对下次跟进出的一个补充说明(200字以内)"
                v-model="row.row.next_follow_up_task">
              </el-input>
            </div>
          </template>
        </vFrom>
      </div>
    </el-dialog>
  </div>
</template>
    
<script>
import api from "@admin/api"
import vFrom from "@admin/components/vFrom.vue"

const followUpStageList = [
  { label: "建立联系", value: "建立联系" },
  { label: "确认意向", value: "确认意向" },
  { label: "预约试听", value: "预约试听" },
  { label: "完成试听", value: "完成试听" },
]
const followUpModeList = [
  { label: "电话", value: "电话" },
  { label: "微信", value: "微信" },
  { label: "短信", value: "短信" },
  { label: "其他", value: "其他" },
]

export default {
  name: 'followUpPopover',
  components: {
    vFrom,
  },
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    },
    userData: {
      type: Object,
      default: () => { }
    }
  },
  data() {
    return {
      parentComponentControl: false, // 判断是否为父组件修改
      showTable: false, // 是否展示跟进计划
      followUpPlanData: [], // 跟进计划数据
      searchData: { // 跟进记录数据
        follow_up_method: '',
        follow_up_stage: '',
        follow_up_content: '',
        next_follow_up_time: null,
        next_follow_up_task: null,
      },
      searchForm: [ // 跟进记录表单
        [
          {
            span: 12,
            type: "select",
            label: "跟进方式",
            prop: "follow_up_method",
            options: followUpModeList,
            placeholder: "请选择跟进进度",
            rules: [{ required: true, message: '请选择跟进进度', trigger: "blur" }]
          },
          {
            span: 12,
            type: "select",
            label: "跟进阶段",
            prop: "follow_up_stage",
            options: followUpStageList,
            placeholder: "请选择跟进进度",
            rules: [{ required: true, message: '请选择跟进进度', trigger: "blur" }]
          },
          {
            span: 24,
            width: 400,
            type: "textarea",
            label: "跟进描述",
            prop: "follow_up_content",
            autosize: { minRows: 3, maxRows: 6 },
            placeholder: "请输入跟进描述",
          },
          {
            span: 24,
            type: "date",
            label: "下次跟进时间",
            prop: "next_follow_up_time",
            dateType: 'datetime',
            pickerOptions: {
              disabledDate(time) {
                return time.getTime() < Date.now() - (24 * 60 * 60 * 1000);
              }
            },
          },
          {
            span: 24,
            type: "slot",
            label: "",
            prop: "next_follow_up_task",
          },
        ]
      ],
    }
  },
  methods: {
    getTableData() {
      this.showTable = false
      if (!this.parentComponentControl) {
        api.getFollowUpRecordList({ student: this.userData.id }).then((res) => {
          let followUpPlanData = []
          res.data.data.results.map((item) => {
            if (!item.actual_follow_up_time) {
              followUpPlanData.push(item)
            }
          })
          this.followUpPlanData = followUpPlanData
          if (this.followUpPlanData.length) this.showTable = true
        })
        this.searchData = {
          follow_up_method: '',
          follow_up_stage: '',
          follow_up_content: '',
          next_follow_up_time: null,
          next_follow_up_task: null,
        }
      }
    },
    followUp(row) {
      this.searchData = row
      this.showTable = false
    },
    close() {
      this.parentComponentControl = false
      this.$emit('closeFollowUpPopover')
    },
    // 提交
    onSubmit() {
      let params = Object.assign(this.searchData, { student: this.userData.id, actual_follow_up_time: new Date() })
      if (this.searchData.id) {
        api.editFollowUpRecord(params).then((res) => {
          this.close()
        })
      } else {
        api.addFollowUpRecord(params).then((res) => {
          this.close()
        })
      }
    }
  },
  watch: {
    dialogVisible: {
      deep: true,
      handler: function (newvalue, oldV) {
        if (newvalue) this.getTableData()
      }
    }
  },
}
</script>
<style scoped lang="less">
.followUpCard {
  margin: 20px 10px;

  .followUpBox {
    line-height: 2.5;

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
</style>