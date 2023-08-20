import api from "@admin/api";

// 省份
const provinceList = [
  { value: "北京市", label: "北京市", ProSort: 1, ProRemark: "直辖市" },
  { value: "天津市", label: "天津市", ProSort: 2, ProRemark: "直辖市" },
  { value: "河北省", label: "河北省", ProSort: 5, ProRemark: "省份" },
  { value: "山西省", label: "山西省", ProSort: 6, ProRemark: "省份" },
  { value: "内蒙古自治区", label: "内蒙古自治区", ProSort: 32, ProRemark: "自治区" },
  { value: "辽宁省", label: "辽宁省", ProSort: 8, ProRemark: "省份" },
  { value: "吉林省", label: "吉林省", ProSort: 9, ProRemark: "省份" },
  { value: "黑龙江省", label: "黑龙江省", ProSort: 10, ProRemark: "省份" },
  { value: "上海市", label: "上海市", ProSort: 3, ProRemark: "直辖市" },
  { value: "江苏省", label: "江苏省", ProSort: 11, ProRemark: "省份" },
  { value: "浙江省", label: "浙江省", ProSort: 12, ProRemark: "省份" },
  { value: "安徽省", label: "安徽省", ProSort: 13, ProRemark: "省份" },
  { value: "福建省", label: "福建省", ProSort: 14, ProRemark: "省份" },
  { value: "江西省", label: "江西省", ProSort: 15, ProRemark: "省份" },
  { value: "山东省", label: "山东省", ProSort: 16, ProRemark: "省份" },
  { value: "河南省", label: "河南省", ProSort: 17, ProRemark: "省份" },
  { value: "湖北省", label: "湖北省", ProSort: 18, ProRemark: "省份" },
  { value: "湖南省", label: "湖南省", ProSort: 19, ProRemark: "省份" },
  { value: "广东省", label: "广东省", ProSort: 20, ProRemark: "省份" },
  { value: "海南省", label: "海南省", ProSort: 24, ProRemark: "省份" },
  { value: "广西壮族自治区", label: "广西壮族自治区", ProSort: 28, ProRemark: "自治区" },
  { value: "甘肃省", label: "甘肃省", ProSort: 21, ProRemark: "省份" },
  { value: "陕西省", label: "陕西省", ProSort: 27, ProRemark: "省份" },
  { value: "新疆维吾尔自治区", label: "新疆维吾尔自治区", ProSort: 31, ProRemark: "自治区" },
  { value: "青海省", label: "青海省", ProSort: 26, ProRemark: "省份" },
  { value: "宁夏回族自治区", label: "宁夏回族自治区", ProSort: 30, ProRemark: "自治区" },
  { value: "重庆市", label: "重庆市", ProSort: 4, ProRemark: "直辖市" },
  { value: "四川省", label: "四川省", ProSort: 22, ProRemark: "省份" },
  { value: "贵州省", label: "贵州省", ProSort: 23, ProRemark: "省份" },
  { value: "云南省", label: "云南省", ProSort: 25, ProRemark: "省份" },
  { value: "西藏自治区", label: "西藏自治区", ProSort: 29, ProRemark: "自治区" },
  { value: "台湾省", label: "台湾省", ProSort: 7, ProRemark: "省份" },
  { value: "澳门特别行政区", label: "澳门特别行政区", ProSort: 33, ProRemark: "特别行政区" },
  { value: "香港特别行政区", label: "香港特别行政区", ProSort: 34, ProRemark: "特别行政区" }
]
// 意向级别
const intentionLevelList = [
  { label: "A", value: "A" },
  { label: "B", value: "B" },
  { label: "C", value: "C" },
  { label: "D", value: "D" },
]
// 当前年级
const gradeList = [
  { label: "一年级", value: "一年级" },
  { label: "二年级", value: "二年级" },
  { label: "三年级", value: "三年级" },
  { label: "四年级", value: "四年级" },
  { label: "五年级", value: "五年级" },
  { label: "六年级", value: "六年级" },
  { label: "初中一年级", value: "初中一年级" },
  { label: "初中二年级", value: "初中二年级" },
  { label: "初中三年级", value: "初中三年级" },
  { label: "高中一年级", value: "高中一年级" },
  { label: "高中二年级", value: "高中二年级" },
  { label: "高中三年级", value: "高中三年级" },
]
const followUpList = [
  { label: "跟进中", value: "跟进中" },
  { label: "待跟进", value: "待跟进" },
  { label: "未分配", value: "未分配" },
  { label: "已成交", value: "已成交" },
]

const tableColumn = [
  {
    prop: 'student_name',
    label: '姓名',
    fixed: true,
    handle: (data) => { }
  },
  {
    prop: 'phone',
    label: '电话',
    fixed: true,
    width: 130
  },
  {
    slot: 'intention_level',
    label: '意向级别',
    width: 120
  },
  {
    prop: 'follow_up',
    label: '跟进人'
  },
  {
    prop: 'follow_status',
    label: '跟进状态',
    // filter: (row) => {
    //   let obj = followUpList.filter(item => item.value == row.follow_status)[0]
    //   return obj ? obj['label'] : row.follow_status
    // }
  },
  {
    prop: 'address',
    label: '省份',
    // filter: (row) => {
    //   let obj = provinceList.filter(item => item.value == row.address)[0]
    //   return obj ? obj['label'] : row.address
    // }
  },
  {
    prop: 'grade',
    label: '当前年级',
    // filter: (row) => {
    //   let obj = gradeList.filter(item => item.value == row.grade)[0]
    //   return obj ? obj['label'] : row.grade
    // }
  },
  {
    prop: 'update_time',
    label: '日期',
    width: '180px',
    filter: (row) => {
      return new Date(row.update_time).Format("yyyy-MM-dd HH:mm:ss")
    }
  },
]

const headerForm = [
  [
    {
      span: 8,
      type: "input",
      label: "姓名",
      prop: "student_name",
      placeholder: "请输入姓名",
    },
    {
      span: 8,
      type: "input",
      label: "电话",
      prop: "phone",
      placeholder: "请输入电话",
    },
    {
      span: 8,
      type: "select",
      label: "省份",
      prop: "address",
      filterable: true,
      options: provinceList,
      placeholder: "请选择省份",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "意向级别",
      prop: "intention_level",
      options: intentionLevelList,
      placeholder: "请选择意向级别",
    },
    {
      span: 8,
      type: "select",
      label: "跟进状态",
      prop: "follow_status",
      options: followUpList,
      placeholder: "请选择跟进状态",
    },
    {
      span: 8,
      type: "select",
      label: "跟进人",
      prop: "follow_up",
      options: [],
      filterable: true,
      placeholder: "请选择跟进人",
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "新增",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量导入",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量导出",
      handle: (data) => { }
    },
    {
      span: 12,
    }
  ]
]

export {
  tableColumn, headerForm, intentionLevelList
}