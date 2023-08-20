const state = {
  classScheduleHeaderData: 2,
}

const getters = {
  classScheduleHeaderData: (state, getters) => {
    return state.classScheduleHeaderData
  },
}

const mutations = {
  classScheduleHeaderData(state, headerData) {
    state.classScheduleHeaderData = headerData
  },
}

const actions = {
}

export default {
  state,
  mutations,
  getters,
  actions
}
