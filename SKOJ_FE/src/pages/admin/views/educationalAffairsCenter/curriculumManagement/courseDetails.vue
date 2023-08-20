

<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Course_Details')" :style="'minHeight:calc(100vh - 170px); overflow-y: auto;'">
      <vFrom class="searchInput" labelWidth="100px" ref="searchSubmitForm" size="default" :searchData="searchData"
        :searchForm="searchForm" @fromSubmit="onSubmit" @fromCancel="onCancel">
        <template slot="chargeMethod">
          <div style="border: 1px solid #ddd9d9;padding: 10px 20px;min-width: 55vw;">
            <el-switch v-model="perClassHourSwitch" active-text="按课时收费">
            </el-switch>
            <div v-if="perClassHourSwitch">
              <h5>【温馨提示】为方便报名时更灵活的选择购买数量，建议您在定价标准中添加/保留数量为1的单价价目哦~ </h5>
              <h4>定价标准</h4>
              <el-table :data="perClassHourList" :border="true" style="width: 100%">
                <el-table-column label="名称" width="180">
                  <template #default="scope">
                    <el-input v-model="scope.row.name" placeholder="请输入名称"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="数量(课时)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.classHour"
                      placeholder="请输入数量(课时)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column label="总价(元)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.totalPrice"
                      placeholder="请输入总价(元)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column prop="date" label="单价(元/课时)">
                  <template #default="scope">
                    {{ automaticCalculation(scope) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="180">
                  <template #default="scope">
                    <el-button type="danger" icon="el-icon-delete" circle
                      @click="perClassHourList.length > 1 ? perClassHourList.splice(scope.$index, 1) : ''"></el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div class="addButton">
                <el-button type="text" @click="perClassHourList.push({})">添加</el-button>
              </div>
              <h4>扣课时规则</h4>
              <span>请假是否扣课时</span>
              <el-radio-group v-model="askForLeaveRadio">
                <el-radio :label="1">扣</el-radio>
                <el-radio :label="2">不扣</el-radio>
                <el-radio :label="3">部分免扣</el-radio>
              </el-radio-group>
              <div v-if="askForLeaveRadio == 3" style="border: 1px solid #ddd9d9;display: flex;padding: 10px;"
                class="selectBox">
                <el-select v-model="askForLeaveList.type" placeholder="请选择">
                  <el-option :label="'不限时间'" :value="'不限时间'"></el-option>
                  <el-option :label="'每月'" :value="'每月'"></el-option>
                  <el-option :label="'自定义事件'" :value="'自定义事件'"></el-option>
                </el-select>
                <div v-if="askForLeaveList.type !== '自定义事件'" class="selectBox">
                  前<el-input-number :controls="false" v-model="askForLeaveList.num"
                    placeholder="请输入次数次"></el-input-number>不扣课时
                </div>
                <div v-else>
                  <div v-for="(item, index) in askForLeaveList.list" :key="index" class="selectBox">
                    <el-date-picker v-model="item.date" type="daterange" range-separator="至" start-placeholder="开始日期"
                      end-placeholder="结束日期">
                    </el-date-picker> 前<el-input-number :controls="false" v-model="item.num"
                      placeholder="请输入次数次"></el-input-number>不扣课时
                    <span style="color: #ff7519;"
                      @click="askForLeaveList.list.push({ date: [new Date(), new Date()], num: undefined })">添加</span>
                    <span style="color: #ff7519;"
                      @click="askForLeaveList.list.length > 1 ? askForLeaveList.list.splice(index, 1) : ''">删除</span>
                  </div>
                </div>
              </div>
              <div>
                <span>未到是否扣课时</span>
                <el-radio-group v-model="notArriveRadio">
                  <el-radio :label="1">扣</el-radio>
                  <el-radio :label="2">不扣</el-radio>
                </el-radio-group>
              </div>
            </div>
            <el-divider></el-divider>
            <el-switch v-model="monthlySwitch" active-text="按月收费">
            </el-switch>
            <div v-if="monthlySwitch">
              <h5>【温馨提示】为方便报名时更灵活的选择购买数量，建议您在定价标准中添加/保留数量为1的单价价目哦~ </h5>
              <h4>定价标准</h4>
              <el-table :data="monthlyList" :border="true" style="width: 100%">
                <el-table-column label="名称" width="180">
                  <template #default="scope">
                    <el-input v-model="scope.row.name" placeholder="请输入名称"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="数量(课时)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.classHour"
                      placeholder="请输入数量(课时)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column label="总价(元)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.totalPrice"
                      placeholder="请输入总价(元)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column prop="date" label="单价(元/课时)">
                  <template #default="scope">
                    {{ automaticCalculation(scope) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="180">
                  <template #default="scope">
                    <el-button type="danger" icon="el-icon-delete" circle
                      @click="monthlyList.length > 1 ? monthlyList.splice(scope.$index, 1) : ''"></el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div class="addButton">
                <el-button type="text" @click="monthlyList.push({})">添加</el-button>
              </div>
            </div>
            <el-divider></el-divider>
            <el-switch v-model="dailyRateSwitch" active-text="按天收费">
            </el-switch>
            <div v-if="dailyRateSwitch">
              <h5>【温馨提示】为方便报名时更灵活的选择购买数量，建议您在定价标准中添加/保留数量为1的单价价目哦~ </h5>
              <h4>定价标准</h4>
              <el-table :data="dailyRateList" :border="true" style="width: 100%">
                <el-table-column label="名称" width="180">
                  <template #default="scope">
                    <el-input v-model="scope.row.name" placeholder="请输入名称"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="数量(课时)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.classHour"
                      placeholder="请输入数量(课时)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column label="总价(元)" width="220">
                  <template #default="scope">
                    <el-input-number :controls="false" v-model="scope.row.totalPrice"
                      placeholder="请输入总价(元)"></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column prop="date" label="单价(元/课时)">
                  <template #default="scope">
                    {{ automaticCalculation(scope) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="180">
                  <template #default="scope">
                    <el-button type="danger" icon="el-icon-delete" circle
                      @click="dailyRateList.length > 1 ? dailyRateList.splice(scope.$index, 1) : ''"></el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div class="addButton">
                <el-button type="text" @click="dailyRateList.push({})">添加</el-button>
              </div>
            </div>
          </div>
        </template>
        <template slot="classArrangement">
          <span style="color:yellowgreen" @click="classArrangementAdd">添加</span>
          <div v-if="classArrangementList.length">
            <div v-for="(  item, index  ) in   classArrangementList  " :key="index" class="classArrangementListBox">
              {{ `${item.name} (${item.list.length}次课)` }}
              <span @click="deleteClassArrangement(item, index)">删除</span>
              <span @click="modifyClassArrangement(item, index)">修改</span>
            </div>
          </div>
        </template>
      </vFrom>
    </Panel>
    <el-dialog :visible.sync="addClassArrangementVisible" title="新增上课安排" @close="closeClassArrangement()">
      名称：<el-input v-model="addClassArrangement.name" placeholder="请输入名称" />
      <el-divider></el-divider>
      <p>安排课次</p>
      <div v-for="(  item, index  ) in   addClassArrangement.list  " :key="index" class="classArrangementList">
        <span>{{ `第${index + 1} 次课` }}</span>
        <el-input v-model="item.content" placeholder="请输入本次排课上课内容" />
        <span @click="delectClassArrangementList(item, index)">删除</span>
      </div>
      <div class="addButton">
        <el-button type="text" @click="addClassArrangementList()">添加</el-button>
      </div>
      <div slot="footer">
        <el-button @click="confirmClassArrangement()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import vFrom from "@admin/components/vFrom.vue"
import { courseDetailsForm } from "./config.js"

export default {
  name: "courseDetails",
  components: {
    vFrom,
  },
  data() {
    return {
      searchForm: courseDetailsForm, // 表格配置
      searchData: {}, // 表格数据
      perClassHourSwitch: true, // 按课时收费滑块
      perClassHourList: [{}], // 按课时收费数据
      askForLeaveRadio: 1, // 请假是否扣课时
      askForLeaveList: {
        type: '不限时间',
        num: undefined,
        list: [
          { date: [new Date(), new Date()], num: undefined }
        ],
      },
      notArriveRadio: 1, // 未到是否扣课时
      monthlySwitch: false, // 按月收费滑块
      monthlyList: [{}], // 按月收费数据
      dailyRateSwitch: false, // 按天收费滑块
      dailyRateList: [{}], // 按天收费数据
      addClassArrangementVisible: false, // 添加上课安排 dialog
      addClassArrangement: { // 上课安排内容
        name: '',
        list: [{ content: '' }],
        modify: false
      },
      classArrangementList: [], // 安排内容列表
    };
  },
  mounted() {
    this.configProperty() // 配置回调函数
    if (this.$route.params) {
      this.searchData = this.$route.params
      console.log(this.searchData);
    } else {
      this.getFormData() // 重置页面数据
    }
  },
  methods: {
    // 配置回调函数
    configProperty() {

    },
    // 重置页面数据
    getFormData() {
      let Data = {}
      this.searchForm.forEach(item => {
        item.forEach(i => {
          if (i.prop) {
            if (i.type === 'tags') {
              Data[i.prop] = []
            } else {
              Data[i.prop] = undefined
            }
          }
        })
      })
      this.searchData = Data
    },
    // 提交
    onSubmit(item) {
      if (this.perClassHourSwitch || this.monthlySwitch || this.dailyRateSwitch) {
        let data = Object.assign({}, this.searchData)
        if (this.monthlySwitch) {
          if (this.pricingStandardContentDetection(this.monthlyList)) {
            data = Object.assign({ monthlyList: this.monthlyList }, data)
          } else {
            return
          }
        }
        if (this.dailyRateSwitch) {
          if (this.pricingStandardContentDetection(this.dailyRateList)) {
            data = Object.assign({ dailyRateList: this.dailyRateList }, data)
          } else {
            return
          }
        }
        if (this.perClassHourSwitch) {
          if (this.pricingStandardContentDetection(this.perClassHourList)) {
            data = Object.assign({ perClassHourList: this.perClassHourList }, data)
          } else {
            return
          }
          if (this.askForLeaveRadio === 3) {
            if (this.askForLeaveList.type === '自定义事件') {
              try {
                this.askForLeaveList.list.forEach((item) => {
                  if (!(item.num && item.num != undefined && item.num != null && item.num != '')) {
                    throw new Error('请输入扣课时规则--次数')
                  }
                  if (!(item.date && item.date != undefined && item.date != null && item.date != '')) {
                    throw new Error('请输入扣课时规则--起始时间')
                  }
                })
              } catch (e) {
                this.$error(e)
                return
              }
            } else {
              if (!(this.askForLeaveList.num && this.askForLeaveList.num != undefined && this.askForLeaveList.num != null && this.askForLeaveList.num != '')) {
                this.$error('请输入扣课时规则--次数')
                return
              }
            }
            Object.assign({ askForLeaveList: this.askForLeaveList }, data)
          }
          data = Object.assign({ askForLeaveRadio: this.askForLeaveRadio, notArriveRadio: this.notArriveRadio }, data)
        }
        data = Object.assign({ classArrangementList: this.classArrangementList }, data)
      } else {
        this.$error('请选择一种收费方式');
      }
    },
    // 定价标准内容检测
    pricingStandardContentDetection(row) {
      let blon = true
      try {
        row.forEach((item) => {
          function determineWhetherItIsEmpty(key) {
            return key && key != undefined && key != null && key != '' ? true : false
          }
          if (!determineWhetherItIsEmpty(item.name)) {
            throw new Error('请输入定价标准--名称')
          } else if (!determineWhetherItIsEmpty(item.classHour)) {
            throw new Error('请输入定价标--准课时数量')
          } else if (!determineWhetherItIsEmpty(item.totalPrice)) {
            throw new Error('请输入定价标准--总价')
          }
        })
      } catch (e) {
        this.$error(e)
        blon = false
      }
      return blon
    },
    // 取消
    onCancel() {
      this.$router.go(-1);
    },
    // 新增上课安排
    classArrangementAdd() {
      this.addClassArrangement.modify = false
      this.addClassArrangementVisible = true
    },
    // 修改上课安排
    modifyClassArrangement(item, index) {
      this.addClassArrangement = item
      this.$set(this.addClassArrangement, 'modify', index)
      this.addClassArrangementVisible = true
    },
    // 删除上课安排
    deleteClassArrangement(item, index) {
      this.classArrangementList.splice(index, 1)
    },
    // 新增上课安排列表
    addClassArrangementList() {
      this.addClassArrangement.list.push({ content: '' })
    },
    // 删除上课安排列表
    delectClassArrangementList(item, index) {
      if (this.addClassArrangement.list.length > 1) {
        this.addClassArrangement.list.splice(index, 1)
      }
    },
    // 添加上课安排
    confirmClassArrangement() {
      if (!this.addClassArrangement.name) {
        this.$error('请输入上课安排标题');
      } else if (!this.addClassArrangement.list.length) {
        this.$error('至少添加一条记录！');
      } else {
        let blon = true
        this.addClassArrangement.list.forEach((item) => {
          if (item.content === '') blon = false
        })
        if (blon) {
          let list = JSON.parse(JSON.stringify(this.addClassArrangement))
          if (typeof (this.addClassArrangement.modify) == 'boolean') {
            this.classArrangementList.push(list)
          } else {
            this.classArrangementList.splice(this.addClassArrangement.modify, 1, list)
          }
          this.closeClassArrangement()
        } else {
          this.$error('上课内容不能为空');
        }
      }
    },
    // 关闭上课安排弹窗
    closeClassArrangement() {
      this.addClassArrangementVisible = false
      this.addClassArrangement = { // 上课安排内容
        name: '',
        list: [{ content: '' }],
        modify: false
      }
    }
  },
  computed: {
    automaticCalculation() {
      return function (scope) {
        return (scope.row.totalPrice / scope.row.classHour).toFixed(2) > 0 ? (scope.row.totalPrice /
          scope.row.classHour).toFixed(2) : '自动计算'
      };
    }
  },
  watch: {
  },
};
</script>
        
<style lang="less" scoped>
.baseInfo {
  padding: 30px 20px 0;
}

.classArrangementList {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 15px 0;

  span {
    width: 100px;
    margin: 10px;
  }
}

.classArrangementListBox {
  width: 300px;

  span {
    float: right;
    margin: 0 10px;
    color: #ff7519;
  }
}

.addButton {
  display: flex;
  justify-content: center;
  border: 1px solid #efd8d8;
}

.selectBox {

  /deep/ .el-date-editor--daterange {
    width: 320px;
    margin: 0 20px;
    height: 30px;
    padding: 0;
    line-height: 30px;
  }

  /deep/ .el-input-number {
    width: 180px;
    margin: 0 20px;
    height: 30px;
    padding: 0;
    line-height: 30px;
  }

  /deep/ .el-input__inner {
    height: 30px;
    padding: 0;
    line-height: 30px;
  }

  /deep/ .el-date-editor .el-range-separator {
    width: 20%;
  }

  /deep/ .el-select--default {
    margin: 0 10px;
  }

  /deep/ .el-date-editor .el-range__icon {
    margin-left: 10px;
  }
}
</style>