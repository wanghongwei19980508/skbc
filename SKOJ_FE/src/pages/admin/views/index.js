import Dashboard from './general/Dashboard.vue'
import Announcement from './general/Announcement.vue'
import User from './general/User.vue'
import Conf from './general/Conf.vue'
import JudgeServer from './general/JudgeServer.vue'
import PruneTestCase from './general/PruneTestCase.vue'
import Problem from './problem/Problem.vue'
import ProblemList from './problem/ProblemList.vue'
import ObjectiveProblemList from './problem/ObjectiveProblemList.vue'
import ObjectiveProblem from './problem/ObjectiveProblem.vue'
import PublicTopicList from './problem/PublicTopicList.vue'
import ContestList from './contest/ContestList.vue'
import Contest from './contest/Contest.vue'
import CourseList from './course/CourseList.vue'
import Course from './course/Course.vue'
import Login from './general/Login.vue'
import Home from './Home.vue'
import ProblemImportOrExport from './problem/ImportAndExport.vue'
import LessonList from './course/LessonList.vue'
import AssignmentList from './course/AssignmentList.vue'
import Assignment from './course/Assignment.vue'
import PPT from './problem/PPT.vue'
import PPTList from './problem/PPTList.vue'
import studentManagementList from './schoolManagement/studentManagement/studentManagementList.vue'
// 课程管理
import curriculumManagement from './educationalAffairsCenter/curriculumManagement/curriculumManagement.vue' // 课程列表
import courseDetails from './educationalAffairsCenter/curriculumManagement/courseDetails.vue' // 课程详情
// 课表管理
import classList from './schoolManagement/classScheduleManagement/classList.vue' // 课表table页
import timeSchedule from './schoolManagement/classScheduleManagement/timeSchedule.vue' // 时间课表
import teacherSchedule from './schoolManagement/classScheduleManagement/teacherSchedule.vue' // 老师课表
import classSchedule from './schoolManagement/classScheduleManagement/classSchedule.vue' // 班级课表
// 销售中心
import customerList from './salesCenter/customer/customerList.vue'
// 学生信息
import studentDetail from './userInformation/studentDetail.vue'

export {
  Announcement, User, Conf, JudgeServer, Problem, ProblemList, ObjectiveProblemList, ObjectiveProblem, PublicTopicList, Contest, Course, CourseList,
  ContestList, Login, Home, PruneTestCase, Dashboard, ProblemImportOrExport, LessonList, AssignmentList, Assignment, PPT, PPTList, studentManagementList, customerList, classList, timeSchedule, teacherSchedule, classSchedule, studentDetail, curriculumManagement, courseDetails
}
