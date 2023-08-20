import api from "@admin/api";

const sourceList = [
  { label: "电话邀约", value: "电话邀约" },
  { label: "门店到访", value: "门店到访" },
  { label: "转介绍", value: "转介绍" },
  { label: "地推活动", value: "地推活动" },
  { label: "家长分享", value: "家长分享" },
  { label: "视频课", value: "视频课" },
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
const classEndStatusList = [
  { label: "未结课", value: "未结课" },
  { label: "已结课", value: "已结课" },
]
const courseTypeList = [
  { label: "一对一", value: "一对一" },
  { label: "一对多", value: "一对多" },
]
const suspendClassesList = [
  { label: "未停课", value: "未停课" },
  { label: "停课中", value: "停课中" },
]
const overList = [
  { label: "有超上", value: "有超上" },
  { label: "未超上", value: "未超上" },
]

const studentInSchoolListTableColumn = [
  {
    prop: 'student_name',
    label: '学员姓名',
    fixed: true,
    handle: (data) => { }
  },
  {
    prop: 'source',
    label: '学员来源',
    // filter: (row) => {
    //   let obj = sourceList.filter(item => item.value == row.source)[0]
    //   return obj ? obj['label'] : ''
    // }
  },
  {
    prop: 'age',
    label: '年龄',
    filter: (row) => {
      let date = new Date(new Date().getTime() - new Date(row.age).getTime());
      return date.getFullYear() - 1969
    }
  },
  {
    prop: 'age1',
    label: '出生日期',
    width: 180,
    filter: (row) => {
      return new Date(row.age).Format("yyyy-M-d H:m:s")
    }
  },
  {
    prop: 'class',
    label: '所在班级',
  },
  {
    prop: 'grade',
    label: '年级',
  },
  {
    prop: 'school',
    label: '学校',
  },
  {
    prop: 'address',
    label: '省份',
  },
  {
    prop: 'follow_up',
    label: '跟进人',
  },
  {
    prop: 'schoolManager',
    label: '学管师',
  },
]

const studentInSchoolListHeaderForm = [
  [
    {
      span: 8,
      type: "input",
      label: "搜索学员",
      prop: "student_name",
      placeholder: "请输入搜索学员",
    },
    {
      span: 8,
      type: "select",
      label: "学员来源",
      prop: "source",
      options: sourceList,
      placeholder: "请选择学员来源",
    },
    {
      span: 8,
      type: "input",
      label: "学员年龄",
      prop: "age",
      placeholder: "请输入学员年龄",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "班级老师",
      prop: "teacher",
      options: [],
      placeholder: "请选择班级老师",
    },
    {
      span: 8,
      type: "select",
      label: "所在班级",
      prop: "class",
      options: [],
      placeholder: "请选择所在班级",
    },
    {
      span: 8,
      type: "select",
      label: "年级",
      prop: "grade",
      options: gradeList,
      placeholder: "请选择年级",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "省份",
      prop: "address",
      options: provinceList,
      placeholder: "请选择省份",
    },
    {
      span: 8,
      type: "select",
      label: "跟进人",
      prop: "follow_up",
      options: [],
      placeholder: "请选择跟进人",
    },
    {
      span: 8,
      type: "select",
      label: "学管师",
      prop: "schoolManager",
      options: [],
      placeholder: "请选择学管师",
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "发消息",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "分配跟进人",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "分配学管师",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "导入学员",
      handle: (data) => { }
    },
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
      label: "批量删除",
      handle: (data) => { }
    },
    {
      span: 6,
    }
  ]
]

const applicationStatusTableColumn = [
  {
    prop: 'student_name',
    label: '学员姓名',
    fixed: true,
    handle: (data) => { }
  },
  {
    prop: 'source',
    label: '报读课程',
  },
  {
    prop: 'purchaseNum',
    label: '购买数量',
  },
  {
    prop: 'giftNum',
    label: '赠送数量',
  },
  {
    prop: 'quantityNum',
    label: '已消耗数量',
  },
  {
    prop: 'reverseNum',
    label: '退转数量',
  },
  {
    prop: 'surplusNum',
    label: '剩余数量',
  },
  {
    prop: 'classCancellationAmount',
    label: '课消金额',
  },
  {
    prop: 'surplusClassCancellationAmount',
    label: '剩余课消金额',
  },
  {
    prop: 'dueDate',
    label: '到期日期',
  },
  {
    prop: 'absencesNum',
    label: '缺课次数',
  },
  {
    prop: 'follow_up',
    label: '跟进人',
  },
  {
    prop: 'schoolManager',
    label: '学管师',
  },
]
const applicationStatusHeaderForm = [
  [
    {
      span: 8,
      type: "input",
      label: "搜索学员",
      prop: "student_name",
      placeholder: "请选择搜索学员",
    },
    {
      span: 8,
      type: "select",
      label: "报读课程",
      prop: "applyForSource",
      options: [],
      multiple: true,
      placeholder: "请选择报读课程",
    },
    {
      span: 8,
      type: "select",
      label: "结课状态",
      prop: "classEndStatus",
      options: classEndStatusList,
      placeholder: "请选择结课状态",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "课程类型",
      prop: "courseType",
      options: courseTypeList,
      placeholder: "请选择课程类型",
    },
    {
      span: 8,
      type: "select",
      label: "所在班级",
      prop: "class",
      options: [],
      placeholder: "请选择所在班级",
    },
    {
      span: 8,
      type: "select",
      label: "班级老师",
      prop: "teacher",
      options: [],
      placeholder: "请选择班级老师",
    },
  ],
  [
    {
      span: 8,
      type: "input",
      label: "剩余数量",
      prop: "surplusQuantity",
      options: [],
      placeholder: "请输入剩余数量",
    },
    {
      span: 8,
      type: "dateRange",
      label: "到期日期",
      prop: "dueDate",
      placeholder: "请选择到期日期",
    },
    {
      span: 8,
      type: "select",
      label: "是否停课",
      prop: "suspendClasses",
      options: suspendClassesList,
      placeholder: "请选择是否停课",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "是否超上",
      prop: "over",
      options: overList,
      placeholder: "请选择是否超上",
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "导入报读信息",
      handle: (data) => { }
    },
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
      label: "修正剩余课时",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量课时清零",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量结课",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量停课",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量复课",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "超上课时处理",
      handle: (data) => { }
    },
    {
      span: 2,
    }
  ]
]


const historyStudentTableColumn = [
  {
    prop: 'student_name',
    label: '学员姓名',
    fixed: true,
    handle: (data) => { }
  },
  {
    prop: 'phone',
    label: '手机号',
  },
  {
    prop: 'age',
    label: '年龄',
    filter: (row) => {
      let date = new Date(new Date().getTime() - new Date(row.age).getTime());
      return date.getFullYear() - 1969
    }
  },
  {
    prop: 'age1',
    label: '出生日期',
    width: 180,
    filter: (row) => {
      return new Date(row.age).Format("yyyy-M-d H:m:s")
    }
  },
  {
    prop: 'grade',
    label: '年级',
  },
  {
    prop: 'creationTime',
    label: '创建时间',
  },
  {
    prop: 'completionTime',
    label: '结业时间',
  },
  {
    prop: 'lastCourseAttended',
    label: '最后就读课程',
  },
  {
    prop: 'follow_up',
    label: '跟进人',
  },
  {
    prop: 'schoolManager',
    label: '学管师',
  },
]
const historyStudentHeaderForm = [
  [
    {
      span: 8,
      type: "input",
      label: "搜索学员",
      prop: "student_name",
      placeholder: "请输入搜索学员",
    },
    {
      span: 8,
      type: "input",
      label: "手机号",
      prop: "phone",
      placeholder: "请输入手机号",
    },
    {
      span: 8,
      type: "dateRange",
      label: "结业时间",
      prop: "completionTime",
      placeholder: "请选择结业时间",
    },
  ],
  [
    {
      span: 8,
      type: "select",
      label: "省份",
      prop: "address",
      options: provinceList,
      placeholder: "请选择省份",
    },
    {
      span: 8,
      type: "select",
      label: "跟进人",
      prop: "follow_up",
      options: [],
      placeholder: "请选择跟进人",
    },
    {
      span: 8,
      type: "select",
      label: "学管师",
      prop: "schoolManager",
      options: [],
      placeholder: "请选择学管师",
    },
  ],
  [
    {
      span: 8,
      type: "input",
      label: "学员年龄",
      prop: "age",
      placeholder: "请输入学员年龄",
    },
    {
      span: 8,
      type: "select",
      label: "最后就读课程",
      prop: "source",
      options: [],
      placeholder: "请选择最后就读课程",
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "分配跟进人",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "分配学管师",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量转为在读",
      handle: (data) => { }
    },
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "批量删除",
      handle: (data) => { }
    },
    {
      span: 10,
    }
  ]
]

export {
  studentInSchoolListTableColumn, studentInSchoolListHeaderForm, applicationStatusTableColumn, applicationStatusHeaderForm,
  historyStudentTableColumn, historyStudentHeaderForm,
}