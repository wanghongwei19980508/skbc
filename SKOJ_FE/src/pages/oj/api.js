/* eslint-disable */
import Vue from 'vue'
import store from '@/store'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  getWebsiteConf(params) {
    return ajax('website', 'get', {
      params
    })
  },
  getAnnouncementList(offset, limit) {
    let params = {
      offset: offset,
      limit: limit
    }
    return ajax('announcement', 'get', {
      params
    })
  },
  login(data) {
    return ajax('login', 'post', {
      data
    })
  },
  checkUsernameOrEmailOrPhone(username, email, phone) {
    return ajax('check_username_or_email_or_phone', 'post', {
      data: {
        username,
        email,
        phone
      }
    })
  },
  // 注册
  register(data) {
    return ajax('register', 'post', {
      data
    })
  },
  logout() {
    return ajax('logout', 'get')
  },
  getCaptcha() {
    return ajax('captcha', 'get')
  },
  getUserInfo(username = undefined) {
    return ajax('profile', 'get', {
      params: {
        username
      }
    })
  },
  updateProfile(profile) {
    return ajax('profile', 'put', {
      data: profile
    })
  },
  freshDisplayID(userID) {
    return ajax('profile/fresh_display_id', 'get', {
      params: {
        user_id: userID
      }
    })
  },
  twoFactorAuth(method, data) {
    return ajax('two_factor_auth', method, {
      data
    })
  },
  tfaRequiredCheck(username) {
    return ajax('tfa_required', 'post', {
      data: {
        username
      }
    })
  },
  getSessions() {
    return ajax('sessions', 'get')
  },
  deleteSession(sessionKey) {
    return ajax('sessions', 'delete', {
      params: {
        session_key: sessionKey
      }
    })
  },
  applyResetPassword(data) {
    return ajax('apply_reset_password', 'post', {
      data
    })
  },
  resetPassword(data) {
    return ajax('reset_password', 'post', {
      data
    })
  },
  changePassword(data) {
    return ajax('change_password', 'post', {
      data
    })
  },
  changeEmail(data) {
    return ajax('change_email', 'post', {
      data
    })
  },
  getLanguages() {
    return ajax('languages', 'get')
  },
  getProblemTagList() {
    return ajax('problem/tags', 'get')
  },
  getObjectiveProblemTagList() {
    return ajax('objective_problem/tags', 'get')
  },
  getProblemList(offset, limit, searchParams) {
    let params = {
      paging: true,
      offset,
      limit
    }
    Object.keys(searchParams).forEach((element) => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('problem', 'get', {
      params: params
    })
  },
  getObjectiveProblemList(offset, limit, searchParams) {
    let params = {
      paging: true,
      offset,
      limit
    }
    Object.keys(searchParams).forEach((element) => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('objective_problem', 'get', {
      params: params
    })
  },
  pickone() {
    return ajax('pickone', 'get')
  },
  pickoneobjective() {
    return ajax('pickone_objective', 'get')
  },
  getProblem(problemID) {
    return ajax('problem', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  getObjectiveProblem(problemID) {
    return ajax('objective_problem', 'get', {
      params: {
        objective_problem_id: problemID
      }
    })
  },
  getObjectiveProblemById(problemID) {
    return ajax('objective_problem', 'get', {
      params: {
        objective_problem_by_id: problemID
      }
    })
  },
  getContestList(offset, limit, searchParams) {
    let params = {
      offset,
      limit
    }
    if (searchParams !== undefined) {
      Object.keys(searchParams).forEach((element) => {
        if (searchParams[element]) {
          params[element] = searchParams[element]
        }
      })
    }
    return ajax('contests', 'get', {
      params
    })
  },
  getContest(id) {
    return ajax('contest', 'get', {
      params: {
        id
      }
    })
  },
  getContestAccess(contestID) {
    return ajax('contest/access', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  checkContestPassword(contestID, password) {
    return ajax('contest/password', 'post', {
      data: {
        contest_id: contestID,
        password
      }
    })
  },
  getAnnouncement(contestId) {
    return ajax('announcement', 'get', {
      params: {
        announcement_id: contestId,
      }
    })
  },
  getContestAnnouncementList(contestId) {
    return ajax('contest/announcement', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblemList(contestId) {
    return ajax('contest/problem', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestObjectiveProblemList(contestId) {
    return ajax('contest/objective_problem', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblem(problemID, contestID) {
    return ajax('contest/problem', 'get', {
      params: {
        contest_id: contestID,
        problem_id: problemID
      }
    })
  },
  getContestObjectiveProblem(objectiveProblemID, contestID) {
    return ajax('contest/objective_problem', 'get', {
      params: {
        contest_id: contestID,
        objective_problem_id: objectiveProblemID
      }
    })
  },
  getCoursesAsRole(offset, limit, searchParams, role) {
    let params = {
      paging: true,
      offset,
      limit,
      role,
    }
    Object.keys(searchParams).forEach((element) => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('course_as_role/list', 'get', {
      params: params
    })
  },
  getCourse(courseId) {
    return ajax('course', 'get', {
      params: {
        course_id: courseId,
      }
    })
  },
  getCourseLessons(offset, limit, courseId) {
    return ajax('course/lesson', 'get', {
      params: {
        offset: offset,
        limit: limit,
        course_id: courseId,
      }
    })
  },
  getLesson(courseId, lessonId) {
    return ajax('lesson', 'get', {
      params: {
        course_id: courseId,
        lesson_id: lessonId,
      }
    })
  },
  getLessonAssignments(lessonId) {
    let params = {
      lesson_id: lessonId,
    }
    return ajax('contests', 'get', {
      params
    })
  },
  submitCode(data) {
    return ajax('submission', 'post', {
      data
    })
  },
  submitChoice(data) {
    return ajax('objective_submission', 'post', {
      data
    })
  },
  getSubmissionList(offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('submissions', 'get', {
      params
    })
  },
  getContestSubmissionList(offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('contest_submissions', 'get', {
      params
    })
  },
  getSubmission(id) {
    return ajax('submission', 'get', {
      params: {
        id
      }
    })
  },
  getObjectiveSubmission(id) {
    return ajax('objective_submission', 'get', {
      params: {
        id
      }
    })
  },
  submissionExists(problemID) {
    return ajax('submission_exists', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  submissionRejudge(id) {
    return ajax('admin/submission/rejudge', 'get', {
      params: {
        id
      }
    })
  },
  objectiveSubmissionRejudge(id) {
    return ajax('admin/objective_submission/rejudge', 'get', {
      params: {
        id
      }
    })
  },
  updateSubmission(data) {
    return ajax('submission', 'put', {
      data
    })
  },
  updateObjectiveSubmission(data) {
    return ajax('objective_submission', 'put', {
      data
    })
  },
  getObjectiveSubmissionList(offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('objective_submissions', 'get', {
      params
    })
  },
  getContestObjectiveSubmissionList(offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('contest_objective_submissions', 'get', {
      params
    })
  },
  getObjectiveSubmission(id) {
    return ajax('objective_submission', 'get', {
      params: {
        id
      }
    })
  },
  objectiveSubmissionExists(problemID) {
    return ajax('objective_submission_exists', 'get', {
      params: {
        objective_problem_id: problemID
      }
    })
  },
  updateObjectiveSubmission(data) {
    return ajax('objective_submission', 'put', {
      data
    })
  },
  getUserRank(offset, limit, rule = 'acm') {
    let params = {
      offset,
      limit,
      rule
    }
    return ajax('user_rank', 'get', {
      params
    })
  },
  getContestRank(params) {
    return ajax('contest_rank', 'get', {
      params
    })
  },
  getACMACInfo(params) {
    return ajax('admin/contest/acm_helper', 'get', {
      params
    })
  },
  updateACInfoCheckedStatus(data) {
    return ajax('admin/contest/acm_helper', 'put', {
      data
    })
  },
  getSoftwaresConfig() {
    return ajax('softwares', 'get')
  },
  getSlideshowsConfig() {
    return ajax('slideshows', 'get')
  },
  getMemberList(courseID) {
    return ajax('course/user', 'get', {
      params: {
        course_id: courseID,
      }
    })
  },
  getSelfTest(params) {
    return ajax('self_test', 'get', {
      params: params
    })
  },
  // 获取课程PPT
  getContestPPTList(params) {
    return ajax('admin/lesson/attachment', 'get', {
      params
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
        // 若后端返回为登录，则为session失效，应退出当前登录用户
        if (res.data.data.startsWith('Please login')) {
          store.dispatch('changeModalStatus', { 'mode': 'login', 'visible': true })
        }
      } else {
        resolve(res)
        // if (method !== 'get') {
        //   Vue.prototype.$success('Succeeded')
        // }
      }
    }, res => {
      // API请求异常，一般为Server error 或 network error
      reject(res)
      Vue.prototype.$error(res.data.data)
    })
  })
}
