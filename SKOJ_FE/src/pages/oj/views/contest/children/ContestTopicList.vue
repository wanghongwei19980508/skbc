<template>
  <div>
    <Panel v-if="Topics.length">
      <div slot="title">{{ $t('m.Topic_List') }}</div>
      <Table v-if="contestRuleType == 'ACM' || OIContestRealTimePermission" :columns="ACMTableColumns" :data="Topics"
        @on-row-click="goContestProblem" :no-data-text="$t('m.No_Problems')">
      </Table>
      <Table v-else :data="Topics" :columns="OITableColumns" @on-row-click="goContestProblem"
        no-data-text="$t('m.No_Problems')"></Table>
    </Panel>
  </div>
</template>
  
<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import { ProblemMixin } from '@oj/components/mixins'

export default {
  name: 'ContestTopicList',
  mixins: [ProblemMixin],
  data() {
    return {
      ACMTableColumns: [
        {
          title: '#',
          key: '_id',
          sortType: 'asc',
          width: 150
        },
        {
          title: this.$i18n.t('m.Title'),
          key: 'title'
        },
        {
          title: this.$i18n.t('m.Total'),
          key: 'submission_number'
        },
        {
          title: this.$i18n.t('m.AC_Rate'),
          render: (h, params) => {
            return h('span', this.getACRate(params.row.accepted_number, params.row.submission_number))
          }
        },
        {
          title: '题目类型',
          key: 'problem_type'
        }
      ],
      OITableColumns: [
        {
          title: '#',
          key: '_id',
          width: 150
        },
        {
          title: this.$i18n.t('m.Title'),
          key: 'title'
        },
        {
          title: '题目类型',
          key: 'problem_type'
        }
      ],
      problems: [],
      objectiveProblems: []
    }
  },
  mounted() {
    this.getContestProblems().then((res) => {
      this.problems = res.data.data
    })
    this.getContestObjectiveProblems().then((res) => {
      this.objectiveProblems = res.data.data
    })
  },
  methods: {
    ...mapActions(['getContestProblems', 'getContestObjectiveProblems']),
    goContestProblem(row) {
      if (row.problem_type === '编程题') {
        this.$router.push({
          name: 'contest-problem-details',
          params: {
            contestID: this.$route.params.contestID,
            problemID: row._id
          }
        })
      } else if (row.problem_type === '客观题') {
        this.$router.push({
          name: "contest-objective-problem-details",
          params: {
            contestID: this.$route.params.contestID,
            objectiveProblemID: row._id,
          },
        });
      }
    }
  },
  computed: {
    Topics() {
      let data = [...this.objectiveProblems, ...this.problems]
      if (data.length > 0) {
        data.sort((a, b) => {
          if (a._id === b._id) {
            return 0
          } else if (a._id > b._id) {
            return 1
          }
          return -1
        })
        if (this.isAuthenticated) {
          if (this.contestRuleType === "ACM") {
            this.addStatusColumn(this.ACMTableColumns, data);
          } else if (this.OIContestRealTimePermission) {
            this.addStatusColumn(this.ACMTableColumns, data);
          }
        }
      }
      return data
    },
    // ...mapState({
    //   problems: state => state.contest.contestProblems,
    //   objectiveProblems: (state) => state.contest.contestObjectiveProblems,
    // }),
    ...mapGetters(['isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission'])
  }
}
</script>
  
<style scoped lang="less"></style>
  