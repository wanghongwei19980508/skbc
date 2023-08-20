const searchForm = [
  {
    label: "手机号码",
    prop: "phone",
  },
  {
    label: "小鹅通号码",
    prop: "xiaoe_phone",
  },
  {
    label: "性别",
    prop: "gender",
  },
  {
    label: "出生日期",
    prop: "age",
    filter: (row) => {
      return new Date(row).Format("yyyy-MM-dd")
    }
  },
  {
    label: "就读学校",
    prop: "school",
  },
  {
    label: "当前年级",
    prop: "grade",
  },
  {
    label: "省份",
    prop: "address",
  },
  {
    label: "学号",
    prop: "id",
  },
  // {
  //   label: "学员来源",
  //   prop: "source",
  // },
  {
    label: "跟进人",
    prop: "follow_up",
  },
  {
    label: "学管师",
    prop: "schoolManager",
  },

  {
    label: "描述",
    prop: "remark",
  },
]

export {
  searchForm
}