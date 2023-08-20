import api from "@admin/api";

// 排课方式
const arrangementOfCoursesList = [
  { label: "规则排课", value: 1 },
  { label: "日历排课", value: 2 }
]
// 重复方式
const repetitiveModeList = [
  { label: "每天重复", value: 1 },
  { label: "隔天重复", value: 2 },
  { label: "每周重复", value: 3 },
  { label: "隔周重复", value: 4 },
]
// 结束方式
const endMethodList = [
  { label: "按日期结束", value: 1 },
  { label: "按次数结束", value: 2 },
]
// 星期列表
const weekList = [
  { label: "星期一", value: 1 },
  { label: "星期二", value: 2 },
  { label: "星期三", value: 3 },
  { label: "星期四", value: 4 },
  { label: "星期五", value: 5 },
  { label: "星期六", value: 6 },
  { label: "星期日", value: 7 },
]
// 电话判断
let checkPhone = (rule, value, callback) => {
  if (!value) {
    return callback(new Error("手机号不能为空"))
  } else {
    const reg = /^1[3|4|5|7|8][0-9]\d{8}$/
    if (reg.test(value)) {
      callback()
    } else {
      return callback(new Error("请输入正确的手机号"))
    }
  }
}
// 性别
const genderList = [
  { label: "未知", value: "未知" },
  { label: "男", value: "男" },
  { label: "女", value: "女" },
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


const courseArrangementDrawerForm = [
  [
    {
      span: 24,
      type: "select",
      label: "课程",
      prop: "course",
      placeholder: "请选择课程",
      options: [],
      change: row => { },
      // rules: [{ required: true, message: '请选择课程', trigger: "blur" }]
    },
    {
      span: 24,
      type: "select",
      label: "班级",
      prop: "class",
      placeholder: "请选择班级",
      options: [],
      // rules: [{ required: true, message: '请选择班级', trigger: "blur" }]
    },
    {
      span: 24,
      type: "radio",
      label: "排课方式",
      prop: "arrangementOfCourses",
      radios: arrangementOfCoursesList,
      // rules: [{ required: true, message: '请选择排课方式', trigger: "blur" }]
    },
    {
      span: 24,
      type: "date",
      label: "开始日期",
      prop: 'statDate',
      boundField: 'arrangementOfCourses',
      judgmentParameter: 1,
      // rules: [{ required: true, message: '请选择开始日期', trigger: "blur" }]
    },
    {
      span: 24,
      type: "radio",
      label: "重复方式",
      prop: "repetitiveMode",
      radios: repetitiveModeList,
      boundField: 'arrangementOfCourses',
      judgmentParameter: 1,
      // rules: [{ required: true, message: '请选择重复方式', trigger: "blur" }]
    },
    {
      span: 24,
      type: "slot",
      prop: 'classTime',
      label: "上课时间",
      boundField: 'classTimeShow',
      judgmentParameter: 1,
    },
    {
      span: 24,
      type: "slot",
      prop: 'weekTime',
      boundField: 'classTimeShow',
      judgmentParameter: 2,
    },
    {
      span: 24,
      type: "radio",
      label: "结束方式",
      prop: "endMethod",
      radios: endMethodList,
      boundField: 'arrangementOfCourses',
      judgmentParameter: 1,
      // rules: [{ required: true, message: '请选择结束方式', trigger: "blur" }]
    },
    {
      span: 24,
      type: "date",
      label: "结束日期",
      prop: 'endDate',
      boundField: 'endMethod',
      judgmentParameter: 1,
      // rules: [{ required: true, message: '请选择结束日期', trigger: "blur" }]
    },
    {
      span: 24,
      type: "number",
      label: "排课次数",
      position: 'right',
      prop: 'scheduleTimes',
      boundField: 'endMethod',
      judgmentParameter: 2,
      // rules: [{ required: true, message: '请选择结束日期', trigger: "blur" }]
    },
    {
      span: 24,
      type: "slot",
      prop: 'classDate',
      label: "上课日期",
      boundField: 'arrangementOfCourses',
      judgmentParameter: 2,
    },
    {
      span: 24,
      type: "select",
      label: "上课老师",
      prop: "teacher",
      multiple: true,
      placeholder: "请选择上课老师",
      options: [],
      // rules: [{ required: true, message: '请选择上课老师', trigger: "blur" }]
    },
    {
      span: 24,
      type: "select",
      label: "上课教室",
      prop: "classRoom",
      placeholder: "请选择上课教室",
      options: [],
      // rules: [{ required: true, message: '请选择上课教室', trigger: "blur" }]
    },
    {
      span: 24,
      type: "textarea",
      label: "上课内容",
      prop: "classContent",
      placeholder: "请选择上课内容",
      // rules: [{ required: true, message: '请选择上课内容', trigger: "blur" }]
    },
  ]
]

const modifyCourseDrawerForm = [
  [
    {
      span: 24,
      type: "select",
      label: "课程",
      prop: "course",
      placeholder: "请选择课程",
      options: [],
      disabled: true,
      change: row => { },
      // rules: [{ required: true, message: '请选择课程', trigger: "blur" }]
    },
    {
      span: 24,
      type: "select",
      label: "班级",
      prop: "class",
      placeholder: "请选择班级",
      options: [],
      disabled: true,
      // rules: [{ required: true, message: '请选择班级', trigger: "blur" }]
    },
    {
      span: 24,
      type: "date",
      label: "上课日期",
      prop: "classDate",
      placeholder: "请选择上课日期",
      // rules: [{ required: true, message: '请选择班级', trigger: "blur" }]
    },
    {
      span: 24,
      type: "slot",
      prop: 'classTime',
      label: "上课时间",
    },
    {
      span: 24,
      type: "select",
      label: "上课老师",
      prop: "teacher",
      multiple: true,
      placeholder: "请选择上课老师",
      options: [],
      // rules: [{ required: true, message: '请选择上课老师', trigger: "blur" }]
    },
    {
      span: 24,
      type: "select",
      label: "上课教室",
      prop: "classRoom",
      placeholder: "请选择上课教室",
      options: [],
      // rules: [{ required: true, message: '请选择上课教室', trigger: "blur" }]
    },
    {
      span: 24,
      type: "textarea",
      label: "上课内容",
      prop: "classContent",
      placeholder: "请选择上课内容",
      // rules: [{ required: true, message: '请选择上课内容', trigger: "blur" }]
    },
  ]
]

const courseDetailsDrawerForm = [
  [
    {
      label: "上课时间",
      prop: "classDate",
      filter: (row) => {
        return new Date(row).Format("yyyy-MM-dd HH:mm:ss")
      }
    },
    {
      label: "上课老师",
      prop: "teacher",
      filter: (row) => {
        return row.join()
      }
    },
    {
      label: "班级容量",
      prop: "classCapacity",
    },
    {
      label: "开课人数",
      prop: "studentNum",
    },
    {
      label: "授课课程",
      prop: "course",
    },
    {
      label: "授课课时",
      prop: "classHour",
    },
    {
      label: "上课教室",
      prop: "classRoom",
    },
    {
      label: "上课内容",
      prop: "classContent",
    },
  ]
]

const courseDetailsDrawerColumn = [
  {
    prop: 'name',
    label: '姓名',
    fixed: true,
    handle: (data) => { }
  },
  {
    prop: 'mode',
    label: '消耗方式',
  },
  {
    prop: 'residualLimit',
    label: '剩余额度',
  },
]

const addCustomerForm = [
  [
    {
      span: 24,
      type: "slot",
      label: "个人头像",
      prop: "avatar",
    },
    {
      span: 24,
      type: "input",
      label: "学生姓名",
      prop: "student_name",
      placeholder: "请输入学生姓名",
      rules: [{ required: true, message: '请输入学生姓名', trigger: "blur" }]
    },
    {
      span: 24,
      type: "input",
      label: "手机号码",
      prop: "phone",
      placeholder: "请输入手机号码",
      rules: [{ required: true, validator: checkPhone, trigger: "blur" }]
    },
    {
      span: 24,
      type: "input",
      label: "小鹅通号码",
      prop: "xiaoe_phone",
      placeholder: "请输入小鹅通号码",
    },
    {
      span: 24,
      type: "select",
      label: "性别",
      prop: "gender",
      placeholder: "请选择性别",
      options: genderList,
    },
    {
      span: 24,
      type: "date",
      label: "出生日期",
      prop: "age",
      placeholder: "请选择出生日期",
    },
    {
      span: 24,
      type: "input",
      label: "就读学校",
      prop: "school",
      placeholder: "请输入就读学校",
    },
    {
      span: 24,
      type: "select",
      label: "当前年级",
      prop: "grade",
      options: gradeList,
      placeholder: "请选择当前年级",
    },
    {
      span: 24,
      type: "select",
      label: "意向级别",
      prop: "intention_level",
      placeholder: "请选择意向级别",
      options: intentionLevelList,
    },
    {
      span: 24,
      type: "select",
      label: "省份",
      prop: "address",
      filterable: true,
      placeholder: "请选择省份",
      options: provinceList,
    },
    {
      span: 24,
      type: "select",
      label: "跟进人",
      prop: "follow_up",
      options: [],
      filterable: true,
      placeholder: "请选择跟进人",
    },
    {
      span: 24,
      width: 400,
      type: "textarea",
      label: "描述",
      prop: "remark",
      autosize: { minRows: 3, maxRows: 6 },
      placeholder: "请输入描述",
    },
  ]
]

const classRecordTableColumn = [
  {
    prop: 'name',
    label: '点名时间',
  },
  {
    prop: 'source',
    label: '班级名称',
  },
  {
    prop: 'date',
    label: '上课时间',
    width: 180,
    filter: (row) => {
      return new Date(row.date).Format("yyyy-MM-dd HH:mm:ss")
    }
  },
  {
    prop: 'age',
    label: '上课老师',
  },
  {
    prop: 'class',
    label: '到课状态',
  },
  {
    prop: 'grade',
    label: '补课状态',
  },
  {
    prop: 'school',
    label: '消耗方式',
  },
  {
    prop: 'school',
    label: '扣除额度',
  },
  {
    prop: 'province',
    label: '课消金额',
  },
  {
    prop: 'salesman',
    label: '上课内容',
  },
  {
    prop: 'schoolManager',
    label: '备注',
  },
]

const classRecordHeaderForm = [
  [
    {
      span: 8,
      type: "dateRange",
      label: "上课日期",
      prop: "name",
    },
    {
      span: 8,
      type: "select",
      label: "所在班级",
      prop: "source",
      options: [],
      placeholder: "请选择所在班级",
    },
    {
      span: 8,
      type: "select",
      label: "上课老师",
      prop: "source",
      options: [],
      placeholder: "请选择上课老师",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "报读课程",
      prop: "birthdayMonth",
      options: [],
      placeholder: "请选择报读课程",
    },
    {
      span: 8,
      type: "select",
      label: "到课状态",
      prop: "class",
      options: [],
      placeholder: "请选择到课状态",
    },
    {
      span: 8,
      type: "select",
      label: "补课状态",
      prop: "grade",
      options: [],
      placeholder: "请选择补课状态",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "课时/天数超上",
      prop: "province",
      options: [],
      placeholder: "请选择超上状态",
    },
    {
      span: 8,
      type: "select",
      label: "消耗方式",
      prop: "salesman",
      options: [],
      placeholder: "请选择消耗方式",
    }
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "导出",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "查看处理记录",
      handle: (data) => { }
    },
    {
      span: 14,
    }
  ]
]

const waitForClassRecordTableColumn = [
  {
    prop: 'name',
    label: '班级名称',
  },
  {
    prop: 'date',
    label: '上课时间',
    width: 180,
    filter: (row) => {
      return new Date(row.date).Format("yyyy-MM-dd HH:mm:ss")
    }
  },
  {
    prop: 'age',
    label: '上课教室',
  },
  {
    prop: 'class',
    label: '上课老师',
  },
  {
    prop: 'grade',
    label: '上课内容',
  },
]

export {
  courseArrangementDrawerForm, weekList, modifyCourseDrawerForm, courseDetailsDrawerForm, courseDetailsDrawerColumn, addCustomerForm, classRecordTableColumn, classRecordHeaderForm, waitForClassRecordTableColumn
}