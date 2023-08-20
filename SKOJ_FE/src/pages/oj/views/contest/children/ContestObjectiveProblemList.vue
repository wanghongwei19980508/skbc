<template>
  <div>
    <Panel>
      <div slot="title">
        {{ $t("m.Objective_Problem_List") }}
      </div>

      <Table
        :columns="ACMTableColumns"
        :data="objectiveProblems"
        @on-row-click="goContestObjectiveProblem"
        :no-data-text="$t('m.No_Objective_Problems')"
      ></Table>
      <!-- <Table
        :data="objectiveProblems"
        :columns="OITableColumns"
        @on-row-click="goContestObjectiveProblem"
        :no-data-text="$t('m.No_Objective_Problems')"
      ></Table> -->
    </Panel>
  </div>
</template>
  
  <script>
import { mapState, mapGetters } from "vuex";
import { ProblemMixin } from "@oj/components/mixins";

export default {
  name: "ContestObjectiveProblemList",
  mixins: [ProblemMixin],
  data() {
    return {
      ACMTableColumns: [
        {
          title: "#",
          key: "_id",
          sortType: "asc",
          width: 150,
        },
        {
          title: this.$i18n.t("m.Title"),
          key: "title",
        },
        {
          title: this.$i18n.t("m.Total"),
          key: "submission_number",
        },
        {
          title: this.$i18n.t("m.AC_Rate"),
          render: (h, params) => {
            return h(
              "span",
              this.getACRate(
                params.row.accepted_number,
                params.row.submission_number
              )
            );
          },
        },
      ],
    };
  },
  mounted() {
    this.getContestObjectiveProblems();
  },
  methods: {
    getContestObjectiveProblems() {
      this.$store.dispatch("getContestObjectiveProblems").then((res) => {
        if (this.isAuthenticated) {
          if (this.contestRuleType === "ACM") {
            this.addStatusColumn(this.ACMTableColumns, res.data.data);
          } else if (this.OIContestRealTimePermission) {
            this.addStatusColumn(this.ACMTableColumns, res.data.data);
          }
        }
      });
    },
    goContestObjectiveProblem(row) {
      this.$router.push({
        name: "contest-objective-problem-details",
        params: {
          contestID: this.$route.params.contestID,
          objectiveProblemID: row._id,
        },
      });
    },
  },
  computed: {
    ...mapState({
      objectiveProblems: (state) => state.contest.contestObjectiveProblems,
    }),
    ...mapGetters([
      "isAuthenticated",
      "contestRuleType",
      "OIContestRealTimePermission",
    ]),
  },
};
</script>
  
  <style scoped lang="less">
</style>
  