const ContestList = () => import(/* webpackChunkName: "contest" */ './ContestList.vue')
const ContestDetails = () => import(/* webpackChunkName: "contest" */ './ContestDetail.vue')
const ContestTopicList = () => import(/* webpackChunkName: "contest" */ './children/ContestTopicList.vue')
const ContestProblemList = () => import(/* webpackChunkName: "contest" */ './children/ContestProblemList.vue')
const ContestObjectiveProblemList = () => import(/* webpackChunkName: "contest" */ './children/ContestObjectiveProblemList.vue')
const ContestRank = () => import(/* webpackChunkName: "contest" */ './children/ContestRank.vue')
const ACMContestHelper = () => import(/* webpackChunkName: "contest" */ './children/ACMHelper.vue')

export { ContestDetails, ContestList, ContestTopicList, ContestProblemList, ContestObjectiveProblemList, ContestRank, ACMContestHelper }
