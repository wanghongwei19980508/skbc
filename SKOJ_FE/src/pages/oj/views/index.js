import ProblemList from './problem/ProblemList.vue'
import ObjectiveProblemList from './problem/ObjectiveProblemList.vue'
import CourseList from './course/CourseList.vue'
import Logout from './user/Logout.vue'
import UserHome from './user/UserHome.vue'
import About from './help/About.vue'
import FAQ from './help/FAQ.vue'
import SoftwareList from './help/SoftwareList.vue'
import NotFound from './general/404.vue'
import Home from './general/Home.vue'
import Announcements from './general/Announcements.vue'
import ContestAnnouncements from './general/ContestAnnouncements.vue'
import AnnouncementDetails from './general/AnnouncementDetails.vue'

// Grouping Components in the Same Chunk
const SubmissionList = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionList.vue')
const ObjectiveSubmissionList = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/ObjectiveSubmissionList.vue')
const SubmissionDetails = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionDetails.vue')
const ObjectiveSubmissionDetails = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/ObjectiveSubmissionDetails.vue')

const ACMRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/ACMRank.vue')
const OIRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/OIRank.vue')

const ApplyResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ApplyResetPassword.vue')
const ResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ResetPassword.vue')

const Problem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/Problem.vue')
const ObjectiveProblem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/ObjectiveProblem.vue')
const LessonList = () => import(/* webpackChunkName: "Lessons" */ '@oj/views/course/children/LessonList.vue')
const MemberList = () => import(/* webpackChunkName: "Members" */ '@oj/views/course/children/MemberList.vue')
const Course = () => import(/* webpackChunkName: "Course" */ '@oj/views/course/Course.vue')
export {
  Home, NotFound, Announcements, ContestAnnouncements, AnnouncementDetails,
  Logout, UserHome, About, FAQ, SoftwareList,
  ProblemList, CourseList, ObjectiveProblemList, Problem, ObjectiveProblem,
  ACMRank, OIRank,
  SubmissionList, SubmissionDetails, ObjectiveSubmissionList, ObjectiveSubmissionDetails,
  ApplyResetPassword, ResetPassword, LessonList, MemberList, Course
}
/* 组件导出分为两类, 一类常用的直接导出，另一类诸如Login, Logout等用懒加载,懒加载不在此处导出
 *   在对应的route内加载
 *   见https://router.vuejs.org/en/advanced/lazy-loading.html
 */
