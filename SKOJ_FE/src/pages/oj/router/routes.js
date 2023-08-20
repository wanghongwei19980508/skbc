// all routes here.
import {
  About,
  ACMRank,
  Announcements,
  AnnouncementDetails,
  ContestAnnouncements,
  ApplyResetPassword,
  FAQ,
  SoftwareList,
  Home,
  Logout,
  NotFound,
  OIRank,
  Course,
  LessonList,
  MemberList,
  Problem,
  ProblemList,
  ObjectiveProblem,
  ObjectiveProblemList,
  ResetPassword,
  SubmissionDetails,
  SubmissionList,
  ObjectiveSubmissionDetails,
  ObjectiveSubmissionList,
  UserHome,
  CourseList
} from '../views'

import * as Contest from '@oj/views/contest'
import * as Setting from '@oj/views/setting'

export default [
  {
    name: 'home',
    path: '/',
    meta: { title: 'Home' },
    component: Home
  },
  {
    name: 'logout',
    path: '/logout',
    meta: { title: 'Logout' },
    component: Logout
  },
  {
    name: 'apply-reset-password',
    path: '/apply-reset-password',
    meta: { title: 'Apply Reset Password' },
    component: ApplyResetPassword
  },
  {
    name: 'reset-password',
    path: '/reset-password/:token',
    meta: { title: 'Reset Password' },
    component: ResetPassword
  },
  {
    name: 'problem-list',
    path: '/problem',
    meta: { title: 'Problem List' },
    component: ProblemList
  },
  {
    name: 'objective-problem-list',
    path: '/objective-problem',
    meta: { title: 'Objective Problem List' },
    component: ObjectiveProblemList
  },
  {
    name: 'problem-details',
    path: '/problem/:problemID',
    meta: { title: 'Problem Details' },
    component: Problem
  },
  {
    name: 'course-list',
    path: '/course',
    meta: { title: 'Course List' },
    component: CourseList
  },
  {
    name: 'course-details',
    path: '/course/:courseID',
    meta: { title: 'Course Details' },
    component: Course,
    children: [
      {
        name: 'lessons',
        path: 'lessons',
        meta: { title: 'Lesson List' },
        component: LessonList
      },
      {
        name: 'members',
        path: 'members',
        meta: { title: 'Member List' },
        component: MemberList
      },
      {
        name: 'assignment-problem-details',
        path: 'assignment/:contestID/problem/:problemID/',
        component: Problem
      },
      {
        name: 'assignment-objective-problem-details',
        path: 'assignment/:contestID/objective-problem/:objectiveProblemID/',
        component: ObjectiveProblem
      },
      {
        name: 'assignment-submission-list',
        path: 'assignment/:contestID/problem/:problemID/submissions',
        component: SubmissionList
      },
      {
        name: 'assignment-objective-submission-list',
        path: 'assignment/:contestID/objective-problem/:objectiveProblemID/submissions',
        meta: { title: 'Submission List' },
        component: ObjectiveSubmissionList
      }
    ]
  },
  {
    name: 'objective-problem-details',
    path: '/objective-problem/:objectiveProblemID',
    meta: { title: 'Objective Problem Details' },
    component: ObjectiveProblem
  },
  {
    name: 'submission-list',
    path: '/status',
    meta: { title: 'Submission List' },
    component: SubmissionList
  },
  {
    name: 'objective-submission-list',
    path: '/objective-status',
    meta: { title: 'Submission List' },
    component: ObjectiveSubmissionList
  },
  {
    name: 'submission-details',
    path: '/status/:id/',
    meta: { title: 'Submission Details' },
    component: SubmissionDetails
  },
  {
    name: 'objective-submission-details',
    path: '/objective-status/:id/',
    meta: { title: 'Objective Submission Details' },
    component: ObjectiveSubmissionDetails
  },
  {
    name: 'contest-list',
    path: '/contest',
    meta: { title: 'Contest List' },
    component: Contest.ContestList
  },
  {
    name: 'contest-details',
    path: '/contest/:contestID/',
    component: Contest.ContestDetails,
    meta: { title: 'Contest Details' },
    children: [
      {
        name: 'contest-submission-list',
        path: 'submissions',
        component: SubmissionList
      },
      {
        name: 'contest-topic-list',
        path: 'topic',
        component: Contest.ContestTopicList
      },
      {
        name: 'contest-problem-list',
        path: 'problems',
        component: Contest.ContestProblemList
      },
      {
        name: 'contest-objective-problem-list',
        path: 'objective-problems',
        component: Contest.ContestObjectiveProblemList
      },
      {
        name: 'contest-problem-details',
        path: 'problem/:problemID/',
        component: Problem
      },
      {
        name: 'contest-objective-problem-details',
        path: 'objective-problem/:objectiveProblemID/',
        component: ObjectiveProblem
      },
      {
        name: 'contest-announcement-list',
        path: 'announcements',
        component: ContestAnnouncements
      },
      {
        name: 'contest-rank',
        path: 'rank',
        component: Contest.ContestRank
      },
      {
        name: 'acm-helper',
        path: 'helper',
        component: Contest.ACMContestHelper
      }
    ]
  },
  {
    name: 'announcement-details',
    path: '/AnnouncementDetails/:announcementID/',
    meta: { title: 'announcement-details' },
    component: AnnouncementDetails
  },
  {
    name: 'acm-rank',
    path: '/acm-rank',
    meta: { title: 'ACM Rankings' },
    component: ACMRank
  },
  {
    name: 'oi-rank',
    path: '/oi-rank',
    meta: { title: 'OI Rankings' },
    component: OIRank
  },
  {
    name: 'user-home',
    path: '/user-home',
    component: UserHome,
    meta: { requiresAuth: true, title: 'User Home' }
  },
  {
    path: '/setting',
    component: Setting.Settings,
    children: [
      {
        name: 'default-setting',
        path: '',
        meta: { requiresAuth: true, title: 'Default Settings' },
        component: Setting.ProfileSetting
      },
      {
        name: 'profile-setting',
        path: 'profile',
        meta: { requiresAuth: true, title: 'Profile Settings' },
        component: Setting.ProfileSetting
      },
      {
        name: 'account-setting',
        path: 'account',
        meta: { requiresAuth: true, title: 'Account Settings' },
        component: Setting.AccountSetting
      },
      {
        name: 'security-setting',
        path: 'security',
        meta: { requiresAuth: true, title: 'Security Settings' },
        component: Setting.SecuritySetting
      }
    ]
  },
  {
    path: '/about',
    name: 'about',
    meta: { title: 'About' },
    component: About
  },
  {
    path: '/faq',
    name: 'faq',
    meta: { title: 'FAQ' },
    component: FAQ
  },
  {
    path: '/software-list',
    name: 'software-list',
    meta: { title: 'SoftwareList' },
    component: SoftwareList
  },
  {
    path: '*',
    meta: { title: '404' },
    component: NotFound
  }
]
