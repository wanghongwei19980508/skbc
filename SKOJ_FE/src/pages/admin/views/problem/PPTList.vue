<template>
  <div class="view">
    <Panel :title="this.$i18n.t('m.PPT_List')">
      <div slot="header">
        <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords">
        </el-input>
      </div>
      <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="PPTList"
        @row-dblclick="handleDblclick" style="width: 100%">
        <el-table-column width="100" prop="id" label="ID"> </el-table-column>
        <el-table-column width="150" :label="$t('m.Display_ID')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row._id }}</span>
            <el-input v-show="row.isEditing" v-model="row._id" @keyup.enter.native="handleInlineEdit(row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="name" :label="$t('m.Name')">
          <template slot-scope="{ row }">
            <span v-show="!row.isEditing">{{ row.name }}</span>
            <el-input v-show="row.isEditing" v-model="row.name" @keyup.enter.native="handleInlineEdit(row)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="upload_by.username" :label="$t('m.Author')">
        </el-table-column>
        <el-table-column width="200" prop="create_time" :label="$t('m.Create_Time')">
          <template slot-scope="scope">
            {{ scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column width="100" prop="visible" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text="" @change="updatePPT(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('m.Operation')" width="250">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEdit(scope.row.id)"></icon-btn>
            <icon-btn icon="download" :name="$t('m.Download_PPT')"
              @click.native="downloadTestCase(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_PPT')" @click.native="deletePPT(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goCreatePPT" icon="el-icon-plus">{{ $t('m.Create') }}
        </el-button>
        <el-pagination class="page" layout="prev, pager, next" @current-change="currentChange" :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
    <el-dialog :title="$t('m.Sure_To_Update_The_PPT')" width="20%" :visible.sync="InlineEditDialogVisible"
      @close-on-click-modal="false">
      <div>
        <p>{{ $t('m.Display_ID') }}: {{ currentRow._id }}</p>
        <p>{{ $t('m.Name') }}: {{ currentRow.name }}</p>
      </div>
      <span slot="footer">
        <cancel @click.native="
          InlineEditDialogVisible = false;
        getPPTList(currentPage);"></cancel>
        <save @click.native="updatePPT(currentRow)"></save>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import api from "../../api.js";
import utils from "@/utils/utils";

export default {
  name: "PPTList",
  components: {
  },
  data() {
    return {
      pageSize: 10,
      total: 0,
      PPTList: [],
      keyword: "",
      loading: false,
      currentPage: 1,
      currentPPTID: "",
      currentRow: {},
      InlineEditDialogVisible: false,
      makePublicDialogVisible: false,
    };
  },
  mounted() {
    this.getPPTList(this.currentPage);
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    handleDblclick(row) {
      row.isEditing = true;
    },
    goEdit(PPTId) {
      this.$router.push({ name: "edit-PPT", params: { PPTId } });
    },
    goCreatePPT() {
      this.$router.push({ name: "create-PPT" });
    },
    // 切换页码回调
    currentChange(page) {
      this.currentPage = page;
      this.getPPTList(page);
    },
    getPPTList(page = 1) {
      this.loading = true;
      let params = {
        limit: this.pageSize,
        offset: (page - 1) * this.pageSize,
        keyword: this.keyword,
      };
      api.getPPTList(params).then((res) => {
        this.loading = false;
        this.total = res.data.data.total;
        for (let item of res.data.data.results) {
          item.isEditing = false;
        }
        this.PPTList = res.data.data.results;
      }, (res) => {
        this.loading = false;
      });
    },
    deletePPT(id) {
      this.$confirm(this.$i18n.t('m.Sure_To_Delete_This_PPT') + '?' + this.$i18n.t('m.The_Associated_Submissions_Will_Be_Deleted_As_Well'), this.$i18n.t('m.Delete_PPT'), { type: "warning", }).then(() => {
        api.deletePPT(id).then(() => [
          this.getPPTList(this.currentPage - 1)
        ]).catch(() => { });
      }, () => { });
    },
    updatePPT(row) {
      let data = Object.assign({}, row);
      api.editPPT(data).then((res) => {
        this.InlineEditDialogVisible = false;
        this.getPPTList(this.currentPage);
      }).catch(() => {
        this.InlineEditDialogVisible = false;
      });
    },
    handleInlineEdit(row) {
      this.currentRow = row;
      this.InlineEditDialogVisible = true;
    },
    downloadTestCase(PPTID) {
      let url = "/admin/PPT?PPT_id=" + PPTID;
      utils.downloadFile(url);
    },
  },
  watch: {
    $route(newVal, oldVal) {
      this.getPPTList(this.currentPage);
    },
    keyword() {
      this.currentChange();
    },
  },
};
</script>

<style scoped lang="less"></style>
