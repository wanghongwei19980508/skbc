const state = {
  tableLength: 2,
}

const getters = {
  tableLength: (state, getters) => {
    return state.tableLength
  },
}

const mutations = {
  tableLength(state, length) {
    state.tableLength = length
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
