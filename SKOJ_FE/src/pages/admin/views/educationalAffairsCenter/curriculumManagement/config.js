

const curriculumManagementTableColumn = [
  {
    prop: 'courseTitle',
    label: '课程名称',
    fixed: true,
  },
  {
    prop: 'type',
    label: '类型',
  },
  {
    prop: 'chargeMethod',
    label: '收费方式',
  },
  {
    prop: 'pricingStandard',
    label: '定价标准',
  },
  {
    prop: 'numberOfStudentsInSchool',
    label: '在读学员数',
  },
  {
    label: '启用状态',
    slot: 'enabledState'
  },
]
const curriculumManagementHeaderForm = [
  [
    {
      span: 8,
      type: "input",
      label: "搜索课程",
      prop: "courseTitle",
      placeholder: "请输入课程名称",
    },
    {
      span: 8,
      type: "radio",
      label: "课程类型",
      prop: "type",
      radios: [
        { label: "一对多", value: "一对多" },
        { label: "一对一", value: "一对一" },
      ],
    },
    {
      span: 8,
      type: "radio",
      label: "课程类型",
      prop: "enabledState",
      radios: [
        { label: "启用", value: 1 },
        { label: "停用", value: 2 },
      ],
    },
  ],
  [
    {
      span: 2,
      type: "button",
      Type: "success",
      label: "新建课程",
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
      span: 14,
    }
  ]
]

const courseDetailsForm = [
  [
    {
      span: 24,
      type: "input",
      label: "课程名称",
      prop: "courseTitle",
      placeholder: "请输入课程名称",
      rules: [{ required: true, message: '请输入课程名称', trigger: "blur" }]
    },
    {
      span: 24,
      type: "radio",
      label: "课程类型",
      prop: "type",
      radios: [
        { label: "一对多", value: "一对多" },
        { label: "一对一", value: "一对一" },
      ],
      rules: [{ required: true, message: '请选择课程类型', trigger: "blur" }]
    },
    {
      span: 24,
      type: "color",
      label: "课表颜色",
      prop: "backgroundColor",
      rules: [{ required: true, message: '请选择课表颜色', trigger: "blur" }]
    },
    {
      span: 24,
      type: "slot",
      label: "收费方式",
      prop: "chargeMethod",
    },
    {
      span: 24,
      type: "slot",
      label: "上课安排",
      prop: "classArrangement",
    },
    {
      span: 24,
      type: "textarea",
      label: "备注",
      prop: "remarks",
      placeholder: "请输入备注",
    },
  ],

]

export {
  curriculumManagementTableColumn, curriculumManagementHeaderForm, courseDetailsForm
}