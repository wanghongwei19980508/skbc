<template>
  <div>
    <el-input v-model="keyword" placeholder="Keywords" prefix-icon="el-icon-search">
    </el-input>
    <el-table :data="PPTs" v-loading="loading">
      <el-table-column :label="$t('m.ID')" width="100" prop="id"> </el-table-column>
      <el-table-column :label="$t('m.Display_ID')" width="200" prop="_id">
      </el-table-column>
      <el-table-column :label="$t('m.Title')" prop="title"> </el-table-column>
      <el-table-column :label="$t('m.Option')" align="center" width="100" fixed="right">
        <template slot-scope="{ row }">
          <icon-btn icon="plus" :name="$t('m.Add_PPT')" @click.native="handleAddPPT(row.id)"></icon-btn>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination class="page" layout="prev, pager, next" @current-change="getPublicPPT" :page-size="limit"
      :total="total">
    </el-pagination>
  </div>
</template>
<script>
import api from "@admin/api";

export default {
  name: "add-PPT-from-public",
  props: ["contestID"],
  data() {
    return {
      page: 1,
      limit: 10,
      total: 0,
      loading: false,
      PPTs: [],
      contest: {},
      keyword: "",
    };
  },
  mounted() {
    if (this.contestID) {
      api.getContest(this.contestID).then((res) => {
        this.contest = res.data.data;
        this.getPublicPPT();
      }).catch(() => { });
    }
  },
  methods: {
    getPublicPPT(page) {
      this.loading = true;
      let params = {
        keyword: this.keyword,
        offset: (page - 1) * this.limit,
        limit: this.limit,
        rule_type: this.contest.rule_type,
      };
      api.getPPTList(params).then((res) => {
        this.loading = false;
        this.total = res.data.data.total;
        this.PPTs = res.data.data.results;
      }).catch(() => { });
    },
    handleAddPPT(PPTID) {
      this.$prompt(this.$i18n.t('m.Please_Input_Display_Id_For_The_Public_PPT'), this.$i18n.t('m.Confirm')).then(({ value }) => {
        let data = {
          PPT_id: PPTID,
          contest_id: this.contestID,
          display_id: value,
        };
        
      }, () => { });
      api.getLessonPPTList(params).then((res) => {
      })
      api.deleteLessonPPT(params).then((res) => {
      })
      api.getLessonPPT(params).then((res) => {
      })
      api.createLessonPPT(params).then((res) => {
      })
    },
  },
  watch: {
    keyword() {
      this.getPublicPPT(this.page);
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
  