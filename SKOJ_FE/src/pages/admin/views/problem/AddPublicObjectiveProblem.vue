<template>
  <div>
    <el-input
      v-model="keyword"
      placeholder="Keywords"
      prefix-icon="el-icon-search"
    >
    </el-input>
    <el-table :data="objectiveProblems" v-loading="loading">
      <el-table-column label="ID" width="100" prop="id"> </el-table-column>
      <el-table-column :label="$t('m.Display_ID')" width="200" prop="_id">
      </el-table-column>
      <el-table-column :label="$t('m.Title')" prop="title"> </el-table-column>
      <el-table-column :label="$t('m.Description')" prop="description">
        <template slot-scope="scope">
          <div v-html="scope.row.description"></div>
        </template>
      </el-table-column>
      <el-table-column :label="$t('m.option')" :align="'center'" width="100" fixed="right">
        <template slot-scope="{ row }">
          <icon-btn
            icon="plus"
            :name="$t('m.Add_the_objective_problem')"
            @click.native="handleAddObjectiveProblem(row.id)"
          ></icon-btn>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="page"
      layout="prev, pager, next"
      @current-change="getPublicObjectiveProblem"
      :page-size="limit"
      :total="total"
    >
    </el-pagination>
  </div>
</template>
  <script>
import api from "@admin/api";

export default {
  name: "add-objective-problem-from-public",
  props: ["contestID"],
  data() {
    return {
      page: 1,
      limit: 10,
      total: 0,
      loading: false,
      objectiveProblems: [],
      contest: {},
      keyword: "",
    };
  },
  mounted() {
    api
      .getContest(this.contestID)
      .then((res) => {
        this.contest = res.data.data;
        this.getPublicObjectiveProblem(1);
      })
      .catch(() => {});
  },
  methods: {
    getPublicObjectiveProblem(page) {
      this.loading = true;
      let params = {
        keyword: this.keyword,
        offset: (page - 1) * this.limit,
        limit: this.limit,
      };
      api
        .getObjectiveProblemList(params)
        .then((res) => {
          this.loading = false;
          this.total = res.data.data.total;
          this.objectiveProblems = res.data.data.results;
        })
        .catch(() => {});
    },
    handleAddObjectiveProblem(objectiveProblemID) {
      this.$prompt(
        "Please input display id for the contest problem",
        "confirm"
      ).then(
        ({ value }) => {
          let data = {
            objective_problem_id: objectiveProblemID,
            contest_id: this.contestID,
            display_id: value,
          };
          api.addContestObjectiveProblemFromPublic(data).then(
            () => {
              this.$emit("on-change");
            },
            () => {}
          );
        },
        () => {}
      );
    },
  },
  watch: {
    keyword() {
      this.getPublicObjectiveProblem(this.page);
    },
  },
};
</script>
  <style scoped>
.page {
  margin-top: 20px;
  text-align: right;
}
</style>
  