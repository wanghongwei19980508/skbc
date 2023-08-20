<template>
  <div>
    <el-drawer :title="title" :visible.sync="drawer" :direction="direction" :before-close="handleClose" :size="width"
      :append-to-body="true">
      <vFrom labelWidth="100px" ref="searchSubmitForm" size="default" :searchData="searchData" :searchForm="searchForm"
        @fromSubmit="onSubmit" :cancelBtn="false">
        <template slot="classTime">
          <el-time-picker is-range v-model="searchData['classTime']" range-separator="至" start-placeholder="开始时间"
            end-placeholder="结束时间" placeholder="选择时间范围" format='HH:mm'>
          </el-time-picker>
          <el-dropdown @command="handleCommand">
            <span class="el-dropdown-link">
              常用设置<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-for="(item, index) in commonSettingList" :key="index"
                :command="{ item: item, row: null }">{{ item.value }}
              </el-dropdown-item>
              <el-dropdown-item :command="{ item: 'addDropDown' }">设置</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </vFrom>
    </el-drawer>
    <el-dialog :visible.sync="commonSettingsVisible" title="配置上课时间段">
      <el-button size="mini" type="danger" @click="addCommonSettings" v-show="addCommonSettingsShow">新增时间段</el-button>
      <el-table :data="commonSettingList">
        <el-table-column :width="300" label="时间">
          <template slot-scope="scope">
            <span v-if="!scope.row.disabled">{{ scope.row.value }}</span>
            <el-time-picker v-else is-range v-model="scope.row['time']" range-separator="至" start-placeholder="开始时间"
              end-placeholder="结束时间" placeholder="选择时间范围" size="samll" format='HH:mm'>
            </el-time-picker>
          </template>
        </el-table-column>
        <el-table-column align="right" :width="160" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="danger" @click="editCommonSettings(scope.$index, scope.row)">{{
              scope.row.disabled ? '保存' : '编辑' }}</el-button>
            <el-button size="mini" type="danger"
              @click="deleteCommonSettings(scope.$index, commonSettingList)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>
      
<script>
import vFrom from "@admin/components/vFrom.vue"
import { modifyCourseDrawerForm } from "./config.js"

export default {
  name: 'modifyCourseDrawer',
  components: {
    vFrom,
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    direction: {
      type: String,
      default: 'rtl'
    },
    drawer: {
      type: Boolean,
      default: false
    },
    width: {
      type: String,
      default: '40%'
    },
    searchData: {
      type: Object,
      default: () => { }
    }
  },
  data() {
    return {
      searchForm: modifyCourseDrawerForm, // 表格配置
      commonSettingList: [ // 常用时间列表
        { value: '11:40-13:40', time: ['2022-01-31 11:40', '2022-01-31 13:40'], disabled: false }
      ],
      commonSettingsVisible: false, // 常用时间配置展示
      // searchData: {}, // 表格数据
    }
  },
  mounted() {
  },
  methods: {
    // 提交
    onSubmit() {
      this.$emit('fromSubmit', { label: 'modifyCourseDrawer', searchData: this.searchData })
    },
    // 关闭抽屉
    handleClose() {
      this.$emit('fromCancel', { label: 'modifyCourseDrawer' })
    },
    // 常用设置
    handleCommand(obj) {
      let { item, row } = obj
      if (item === 'addDropDown') {
        this.commonSettingsVisible = true
      } else {
        if (row) {
          row.time = item.time.map((i) => {
            return new Date(i)
          })
        } else {
          this.searchData['classTime'] = item.time.map((i) => {
            return new Date(i)
          })
        }
      }
    },
    // 编辑常用设置
    editCommonSettings(index, row) {
      if (row.disabled) {
        this.$set(this.commonSettingList[index], 'value', new Date(this.commonSettingList[index].time[0]).Format('HH:mm') + '-' + new Date(this.commonSettingList[index].time[1]).Format('HH:mm'))
        '接口保存'
      }
      this.$set(this.commonSettingList[index], 'disabled', !this.commonSettingList[index].disabled)
    },
    // 删除常用设置
    deleteCommonSettings(index, item) {
      item.splice(index, 1);
    },
    // 新增常用设置
    addCommonSettings() {
      this.commonSettingList.push(
        { time: [new Date(), new Date()], disabled: true }
      )
    },
  },
  computed: {
    addCommonSettingsShow() {
      let blon = true
      this.commonSettingList.map((item) => {
        if (item.disabled) blon = false
      })
      return blon
    }
  },
  watch: {

  },
}
</script>
<style lang="less" scoped>
.addButton {
  display: flex;
  justify-content: center;
  border: 1px solid #efd8d8;
}
</style>
<style lang="less">
.el-date-editor .el-range__icon {
  width: 0 !important;
}

.el-date-editor .el-range-input {
  width: 45%;
}

.el-date-editor .el-range-separator {
  width: 10%;
}

.el-date-editor.el-input__inner {
  width: 230px !important;
}
</style>
    
      