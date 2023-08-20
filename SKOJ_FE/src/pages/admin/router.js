import Vue from 'vue'
import VueRouter from 'vue-router'
// 引入 view 组件
import {
  Announcement, Conf, Contest, ContestList, Home, JudgeServer, Login, ObjectiveProblem, Course, CourseList,
  Problem, ProblemList, ObjectiveProblemList, PublicTopicList, User, PruneTestCase, Dashboard, ProblemImportOrExport, LessonList, AssignmentList, Assignment, PPT, PPTList, studentManagementList, customerList, classList, timeSchedule, teacherSchedule, classSchedule, studentDetail, curriculumManagement, courseDetails
} from './views'
Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}
export default new VueRouter({
  mode: 'history',
  base: '/admin/',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      component: Home,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: Dashboard
        },
        {
          path: '/announcement',
          name: 'announcement',
          component: Announcement
        },
        {
          path: '/user',
          name: 'user',
          component: User
        },
        {
          path: '/conf',
          name: 'conf',
          component: Conf
        },
        {
          path: '/judge-server',
          name: 'judge-server',
          component: JudgeServer
        },
        {
          path: '/prune-test-case',
          name: 'prune-test-case',
          component: PruneTestCase
        },
        {
          path: '/problems',
          name: 'problem-list',
          component: ProblemList
        },
        {
          path: '/PPT',
          name: 'PPT-list',
          component: PPTList
        },
        {
          path: '/objective-problems',
          name: 'objective-problem-list',
          component: ObjectiveProblemList
        },
        {
          path: '/problem/create',
          name: 'create-problem',
          component: Problem
        },
        {
          path: '/PPT/create',
          name: 'create-PPT',
          component: PPT
        },
        {
          path: '/objective-problem/create',
          name: 'create-objective-problem',
          component: ObjectiveProblem
        },
        {
          path: '/problem/edit/:problemId',
          name: 'edit-problem',
          component: Problem
        },
        {
          path: '/PPT/edit/:PPTId',
          name: 'edit-PPT',
          component: PPT
        },
        {
          path: '/objective-problem/edit/:objectiveOroblemId',
          name: 'edit-objective-problem',
          component: ObjectiveProblem
        },
        {
          path: '/problem/batch_ops',
          name: 'problem_batch_ops',
          component: ProblemImportOrExport
        },
        {
          path: '/course/create',
          name: 'create-course',
          component: Course
        },
        {
          path: '/course',
          name: 'course-list',
          component: CourseList
        },
        {
          path: '/course/:courseId/edit',
          name: 'edit-course',
          component: Course
        },
        {
          path: '/course/:courseId/announcement',
          name: 'course-announcement',
          component: Announcement
        },
        {
          path: '/course/:courseId/lesson',
          name: 'course-lesson',
          component: LessonList
        },
        {
          path: '/lesson/:lessonId/assignments',
          name: 'lesson-assignment-list',
          component: AssignmentList
        },
        {
          path: '/lesson/:lessonId/assignment/create',
          name: 'create-assignment',
          component: Assignment
        },
        {
          path: '/lesson/:lessonId/assignment/:assignmentId/edit',
          name: 'edit-assignment',
          component: Assignment
        },
        {
          path: '/contest/create',
          name: 'create-contest',
          component: Contest
        },
        {
          path: '/contest',
          name: 'contest-list',
          component: ContestList
        },
        {
          path: '/contest/:contestId/edit',
          name: 'edit-contest',
          component: Contest
        },
        {
          path: '/contest/:contestId/announcement',
          name: 'contest-announcement',
          component: Announcement
        },
        {
          path: '/contest/:contestId/problems',
          name: 'contest-problem-list',
          component: ProblemList
        },
        {
          path: '/contest/:contestId/objective-problems',
          name: 'contest-objective-problem-list',
          component: ObjectiveProblemList
        },
        {
          path: '/contest/:contestId/public-topic',
          name: 'contest-public-topic-list',
          component: PublicTopicList
        },
        {
          path: '/contest/:contestId/problem/create',
          name: 'create-contest-problem',
          component: Problem
        },
        {
          path: '/contest/:contestId/problem/:problemId/edit',
          name: 'edit-contest-problem',
          component: Problem
        },
        {
          path: '/contest/:contestId/objective-problem/create',
          name: 'create-contest-objective-problem',
          component: ObjectiveProblem
        },
        {
          path: '/contest/:contestId/objective-problem/:objectiveProblemId/edit',
          name: 'edit-contest-objective-problem',
          component: ObjectiveProblem
        },
        { // 学员管理列表
          path: '/studentManagement',
          name: 'studentManagement',
          component: studentManagementList
        },
        { // 客户管理列表
          path: '/customerList',
          name: 'customerList',
          component: customerList
        },
        { // 课程管理
          path: '/curriculumManagement',
          name: 'curriculumManagement',
          component: curriculumManagement
        },
        { // 课程详情
          path: '/courseDetails',
          name: 'courseDetails',
          component: courseDetails
        },
        { // 课表管理
          path: '/classList',
          name: 'classList',
          component: classList,
          children: [
            { // 时间课表
              path: '/timeSchedule',
              name: 'timeSchedule',
              component: timeSchedule
            },
            { // 老师课表
              path: '/teacherSchedule',
              name: 'teacherSchedule',
              component: teacherSchedule
            },
            { // 班级课表
              path: '/classSchedule',
              name: 'classSchedule',
              component: classSchedule
            },
          ]
        },
        { // 学生信息
          path: '/studentDetail',
          name: 'studentDetail',
          component: studentDetail
        },
      ]
    },
    {
      path: '*', redirect: '/login'
    }
  ]
})
