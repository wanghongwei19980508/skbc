/* eslint-disable */
import Vue from 'vue'
import router from './router'
import axios from 'axios'
import utils from '@/utils/utils'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  // 登录
  login(username, password) {
    return ajax('login', 'post', {
      data: {
        username,
        password
      }
    })
  },
  logout() {
    return ajax('logout', 'get')
  },
  getProfile() {
    return ajax('profile', 'get')
  },
  // 获取公告列表
  getAnnouncementList(offset, limit) {
    return ajax('admin/announcement', 'get', {
      params: {
        paging: true,
        offset,
        limit
      }
    })
  },
  // 删除公告
  deleteAnnouncement(id) {
    return ajax('admin/announcement', 'delete', {
      params: {
        id
      }
    })
  },
  // 修改公告
  updateAnnouncement(data) {
    return ajax('admin/announcement', 'put', {
      data
    })
  },
  // 添加公告
  createAnnouncement(data) {
    return ajax('admin/announcement', 'post', {
      data
    })
  },
  // 获取用户列表
  getUserList(offset, limit, keyword) {
    let params = { paging: true, offset, limit }
    if (offset == undefined) {
      params.paging = false
    }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/user', 'get', {
      params: params
    })
  },
  // 获取单个用户信息
  getUser(id) {
    return ajax('admin/user', 'get', {
      params: {
        id
      }
    })
  },
  // 编辑用户
  editUser(data) {
    return ajax('admin/user', 'put', {
      data
    })
  },
  deleteUsers(id) {
    return ajax('admin/user', 'delete', {
      params: {
        id
      }
    })
  },
  importUsers(users) {
    return ajax('admin/user', 'post', {
      data: {
        users
      }
    })
  },
  generateUser(data) {
    return ajax('admin/generate_user', 'post', {
      data
    })
  },
  getLanguages() {
    return ajax('languages', 'get')
  },
  getSMTPConfig() {
    return ajax('admin/smtp', 'get')
  },
  createSMTPConfig(data) {
    return ajax('admin/smtp', 'post', {
      data
    })
  },
  editSMTPConfig(data) {
    return ajax('admin/smtp', 'put', {
      data
    })
  },
  testSMTPConfig(email) {
    return ajax('admin/smtp_test', 'post', {
      data: {
        email
      }
    })
  },
  getWebsiteConfig() {
    return ajax('admin/website', 'get')
  },
  editWebsiteConfig(data) {
    return ajax('admin/website', 'post', {
      data
    })
  },
  getSoftwaresConfig() {
    return ajax('admin/softwares', 'get')
  },
  clearSWPicCached() {
    return ajax('admin/clearSWPicCached', 'delete')
  },
  editSoftwaresConfig(data) {
    return ajax('admin/softwares', 'post', {
      data
    })
  },
  getSlideshows() {
    return ajax('admin/slideshows', 'get')
  },
  clearSSPicCached() {
    return ajax('admin/clearSSPicCached', 'delete')
  },
  editSlideshows(data) {
    return ajax('admin/slideshows', 'post', {
      data
    })
  },
  getJudgeServer() {
    return ajax('admin/judge_server', 'get')
  },
  deleteJudgeServer(hostname) {
    return ajax('admin/judge_server', 'delete', {
      params: {
        hostname: hostname
      }
    })
  },
  updateJudgeServer(data) {
    return ajax('admin/judge_server', 'put', {
      data
    })
  },
  getInvalidTestCaseList() {
    return ajax('admin/prune_test_case', 'get')
  },
  pruneTestCase(id) {
    return ajax('admin/prune_test_case', 'delete', {
      params: {
        id
      }
    })
  },
  createCourse(data) {
    return ajax('admin/course', 'post', {
      data
    })
  },
  getCourse(id) {
    return ajax('admin/course', 'get', {
      params: {
        id
      }
    })
  },
  editCourse(data) {
    return ajax('admin/course', 'put', {
      data
    })
  },
  getCourseUsers(courseID, courseRole) {
    return ajax('course/user', 'get', {
      params: {
        course_id: courseID,
        role: courseRole
      }
    })
  },
  addCourseUser(courseId, userId, role) {
    return ajax('admin/course/user', 'post', {
      data: {
        course_id: courseId,
        user_id: userId,
        role: role
      }
    })
  },
  deleteCourseUser(courseId, userId, role) {
    return ajax('admin/course/user', 'delete', {
      params: {
        course_id: courseId,
        user_id: userId,
        role: role
      }
    })
  },
  getCourseList(offset, limit, keyword) {
    let params = { paging: true, offset, limit }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/course', 'get', {
      params: params
    })
  },
  getCourseLessonList(courseID, offset, limit, keyword) {
    let params = { paging: true, offset, limit, course_id: courseID }
    if (offset == undefined) {
      params.paging = false
    }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/course/lesson', 'get', {
      params: params
    })
  },
  createCourseLesson(data) {
    return ajax('admin/course/lesson', 'post', {
      data
    })
  },
  deleteCourseLesson(id) {
    return ajax('admin/course/lesson', 'delete', {
      params: {
        id
      }
    })
  },
  updateCourseLesson(data) {
    return ajax('admin/course/lesson', 'put', {
      data
    })
  },
  getCourseAnnouncementList(courseID) {
    return ajax('admin/course/announcement', 'get', {
      params: {
        course_id: courseID
      }
    })
  },
  createCourseAnnouncement(data) {
    return ajax('admin/course/announcement', 'post', {
      data
    })
  },
  deleteCourseAnnouncement(id) {
    return ajax('admin/course/announcement', 'delete', {
      params: {
        id
      }
    })
  },
  updateCourseAnnouncement(data) {
    return ajax('admin/course/announcement', 'put', {
      data
    })
  },
  getCourseTagList(params) {
    return ajax('course/tags', 'get', {
      params
    })
  },
  getAssignmentList(lessonId, offset, limit, keyword) {
    let params = { paging: true, offset, limit, lesson_id: lessonId }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/contest', 'get', {
      params: params
    })
  },
  createAssignment(data) {
    return ajax('admin/contest', 'post', {
      data
    })
  },
  getAssignment(id) {
    return ajax('admin/contest', 'get', {
      params: {
        id
      }
    })
  },
  editAssignment(data) {
    return ajax('admin/contest', 'put', {
      data
    })
  },
  createContest(data) {
    return ajax('admin/contest', 'post', {
      data
    })
  },
  getContest(id) {
    return ajax('admin/contest', 'get', {
      params: {
        id
      }
    })
  },
  editContest(data) {
    return ajax('admin/contest', 'put', {
      data
    })
  },
  getContestList(offset, limit, keyword) {
    let params = { paging: true, offset, limit }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/contest', 'get', {
      params: params
    })
  },
  getContestAnnouncementList(contestID) {
    return ajax('admin/contest/announcement', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  createContestAnnouncement(data) {
    return ajax('admin/contest/announcement', 'post', {
      data
    })
  },
  deleteContestAnnouncement(id) {
    return ajax('admin/contest/announcement', 'delete', {
      params: {
        id
      }
    })
  },
  updateContestAnnouncement(data) {
    return ajax('admin/contest/announcement', 'put', {
      data
    })
  },
  getProblemTagList(params) {
    return ajax('problem/tags', 'get', {
      params
    })
  },
  getObjectiveProblemTagList(params) {
    return ajax('objective_problem/tags', 'get', {
      params
    })
  },
  compileSPJ(data) {
    return ajax('admin/compile_spj', 'post', {
      data
    })
  },
  createProblem(data) {
    return ajax('admin/problem', 'post', {
      data
    })
  },
  createObjectiveProblem(data) {
    return ajax('admin/objective_problem', 'post', {
      data
    })
  },
  editObjectiveProblem(data) {
    return ajax('admin/objective_problem', 'put', {
      data
    })
  },
  deleteObjectiveProblem(id) {
    return ajax('admin/objective_problem', 'delete', {
      params: {
        id
      }
    })
  },
  editProblem(data) {
    return ajax('admin/problem', 'put', {
      data
    })
  },
  deleteProblem(id) {
    return ajax('admin/problem', 'delete', {
      params: {
        id
      }
    })
  },
  getProblem(id) {
    return ajax('admin/problem', 'get', {
      params: {
        id
      }
    })
  },
  getObjectiveProblem(id) {
    return ajax('admin/objective_problem', 'get', {
      params: {
        id
      }
    })
  },
  getProblemList(params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/problem', 'get', {
      params
    })
  },
  getObjectiveProblemList(params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/objective_problem', 'get', {
      params
    })
  },
  getContestProblemList(params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/contest/problem', 'get', {
      params
    })
  },
  getContestObjectiveProblemList(params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/contest/objective_problem', 'get', {
      params
    })
  },
  getContestProblem(id) {
    return ajax('admin/contest/problem', 'get', {
      params: {
        id
      }
    })
  },
  getContestObjectiveProblem(id) {
    return ajax('admin/contest/objective_problem', 'get', {
      params: {
        id
      }
    })
  },
  createContestProblem(data) {
    return ajax('admin/contest/problem', 'post', {
      data
    })
  },
  editContestProblem(data) {
    return ajax('admin/contest/problem', 'put', {
      data
    })
  },
  deleteContestProblem(id) {
    return ajax('admin/contest/problem', 'delete', {
      params: {
        id
      }
    })
  },
  makeContestProblemPublic(data) {
    return ajax('admin/contest_problem/make_public', 'post', {
      data
    })
  },
  addContestProblemFromPublic(data) {
    return ajax('admin/contest/add_problem_from_public', 'post', {
      data
    })
  },
  createContestObjectiveProblem(data) {
    return ajax('admin/contest/objective_problem', 'post', {
      data
    })
  },
  editContestObjectiveProblem(data) {
    return ajax('admin/contest/objective_problem', 'put', {
      data
    })
  },
  deleteContestObjectiveProblem(id) {
    return ajax('admin/contest/objective_problem', 'delete', {
      params: {
        id
      }
    })
  },
  makeContestObjectiveProblemPublic(data) {
    return ajax('admin/contest_objective_problem/make_public', 'post', {
      data
    })
  },
  addContestObjectiveProblemFromPublic(data) {
    return ajax('admin/contest/add_objective_problem_from_public', 'post', {
      data
    })
  },
  // lesson
  getCourseLesson(id) {
    return ajax('admin/course/lesson', 'get', {
      params: {
        id
      }
    })
  },
  // getLessonProblemList(params) {
  //   params = utils.filterEmptyValue(params)
  //   return ajax('admin/lesson/problem', 'get', {
  //     params
  //   })
  // },
  // getLessonObjectiveProblemList(params) {
  //   params = utils.filterEmptyValue(params)
  //   return ajax('admin/lesson/objective_problem', 'get', {
  //     params
  //   })
  // },
  // getLessonProblem(id) {
  //   return ajax('admin/lesson/problem', 'get', {
  //     params: {
  //       id
  //     }
  //   })
  // },
  // getLessonObjectiveProblem(id) {
  //   return ajax('admin/lesson/objective_problem', 'get', {
  //     params: {
  //       id
  //     }
  //   })
  // },
  // createLessonProblem(data) {
  //   return ajax('admin/lesson/problem', 'post', {
  //     data
  //   })
  // },
  // editLessonProblem(data) {
  //   return ajax('admin/lesson/problem', 'put', {
  //     data
  //   })
  // },
  // deleteLessonProblem(id) {
  //   return ajax('admin/lesson/problem', 'delete', {
  //     params: {
  //       id
  //     }
  //   })
  // },
  // makeLessonProblemPublic(data) {
  //   return ajax('admin/lesson_problem/make_public', 'post', {
  //     data
  //   })
  // },
  // addLessonProblemFromPublic(data) {
  //   return ajax('admin/lesson/add_problem_from_public', 'post', {
  //     data
  //   })
  // },
  // addLessonObjectiveProblemFromPublic(data) {
  //   return ajax('admin/lesson/add_objective_problem_from_public', 'post', {
  //     data
  //   })
  // },

  getReleaseNotes() {
    return ajax('admin/versions', 'get')
  },
  getDashboardInfo() {
    return ajax('admin/dashboard_info', 'get')
  },
  getSessions() {
    return ajax('sessions', 'get')
  },
  exportProblems(data) {
    return ajax('export_problem', 'post', {
      data
    })
  },
  // 获取PPT列表
  getPPTList(params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/attachment', 'get', {
      params
    })
  },
  // 新增PPT
  createPPT(data) {
    return ajax('admin/attachment', 'post', {
      data
    })
  },
  // 获取PPT内容
  getPPT(id) {
    return ajax('admin/attachment', 'get', {
      params: {
        id
      }
    })
  },
  // 修改PPT
  editPPT(data) {
    return ajax('admin/attachment', 'put', {
      data
    })
  },
  // 删除PPT
  deletePPT(id) {
    return ajax('admin/attachment', 'delete', {
      params: {
        id
      }
    })
  },
  // 新增课程PPT
  createLessonPPT(data) {
    return ajax('admin/lesson/attachment', 'post', {
      data
    })
  },
  // 获取课程PPT
  getLessonPPT(params) {
    return ajax('admin/lesson/attachment', 'get', {
      params
    })
  },
  // 删除课程PPT
  deleteLessonPPT(params) {
    return ajax('admin/lesson/attachment', 'delete', {
      params
    })
  },
  // PPT标签列表
  getPPTTagList(params) {
    return ajax('attachment/tags', 'get', {
      params
    })
  },
  // 客户库列表
  getClueList(params) {
    return ajax('admin/clue', 'get', {
      params
    })
  },
  // 添加客户
  addClue(data) {
    return ajax('admin/clue', 'post', {
      data
    })
  },
  // 修改用户
  editClue(data) {
    return ajax('admin/clue', 'put', {
      data
    })
  },
  // 删除用户
  deleteClue(id) {
    return ajax('admin/clue', 'delete', {
      params: {
        id
      }
    })
  },
  // 跟进记录列表
  getFollowUpRecordList(params) {
    return ajax('admin/follow_up_record', 'get', {
      params
    })
  },
  // 添加跟进记录
  addFollowUpRecord(data) {
    return ajax('admin/follow_up_record', 'post', {
      data
    })
  },
  // 修改跟进记录
  editFollowUpRecord(data) {
    return ajax('admin/follow_up_record', 'put', {
      data
    })
  },
  // 删除跟进记录
  deleteFollowUpRecord(id) {
    return ajax('admin/follow_up_record', 'delete', {
      params: {
        id
      }
    })
  },
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param params like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * @param data post data, use for method put|post
 * @returns {Promise}
 */
function ajax(url, method, options) {
  if (options !== undefined) {
    var { params = {}, data = {} } = options
  } else {
    params = data = {}
  }
  return new Promise((resolve, reject) => {
    axios({
      url,
      method,
      params,
      data
    }).then(res => {
      // API正常返回(status=20x), 是否错误通过有无error判断
      if (res.data.error !== null) {
        Vue.prototype.$error(res.data.data)
        reject(res)
        // // 若后端返回为登录，则为session失效，应退出当前登录用户
        if (res.data.data.startsWith('Please login')) {
          router.push({ name: 'login' })
        }
      } else {
        resolve(res)
        if (method !== 'get') {
          Vue.prototype.$success('Succeeded')
        }
      }
    }, res => {
      // API请求异常，一般为Server error 或 network error
      reject(res)
      Vue.prototype.$error(res.data.data)
    })
  })
}
