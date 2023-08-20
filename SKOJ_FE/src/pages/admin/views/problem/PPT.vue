<template>
  <div class="PPT">
    <Panel :title="title">
      <el-form ref="form" :model="PPT" :rules="rules" label-position="top" label-width="70px">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item prop="_id" :label="$t('m.Display_ID')" required>
              <el-input :placeholder="$t('m.Display_ID')" v-model="PPT._id"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item prop="name" :label="$t('m.Name')" required>
              <el-input :placeholder="$t('m.Name')" v-model="PPT.name"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item prop="description" :label="$t('m.Description')" required>
              <Simditor v-model="PPT.description"></Simditor>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="4">
            <el-form-item :label="$t('m.Visible')">
              <el-switch v-model="PPT.visible" active-text="" inactive-text="">
              </el-switch>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Tag')" :error="error.tags" required>
              <span class="tags">
                <el-tag v-for="tag in PPT.tags" :closable="true" :close-transition="false" :key="tag" type="success"
                  @close="closeTag(tag)">{{ tag }}</el-tag>
              </span>
              <el-autocomplete v-if="inputVisible" size="mini" class="input-new-tag" popper-class="PPT-tag-poper"
                v-model="tagInput" :trigger-on-focus="false" @keyup.enter.native="addTag" @select="addTag"
                :fetch-suggestions="querySearch">
              </el-autocomplete>
              <el-button class="button-new-tag" v-else size="small" @click="inputVisible = true">+ {{
                $t("m.New_Tag") }}</el-button>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Upload_PPT')" :error="error.UploadPPT">
              <el-button v-if="this.mode == 'edit'" type="primary" size="small"
                @click="goOppenPPT(PPT.path)">去查看</el-button>
              <el-upload action="/api/admin/upload_file" name="file" :data="{}" :show-file-list="true"
                :on-success="uploadSucceeded" :on-error="uploadFailed">
                <el-button size="small" type="primary" icon="el-icon-fa-upload">{{ this.mode == 'edit' ?
                  $t('m.Change_File') : $t('m.Choose_File') }}</el-button>
              </el-upload>
            </el-form-item>
          </el-col>
        </el-row>
        <save @click.native="submit()">{{ $t('m.Save') }}</save>
      </el-form>
    </Panel>
    <el-dialog :visible="pdfDialogVisible" :title="$t('m.Look_PPT')" :fullscreen="pdfFullscreen"
      :close-on-click-modal="false" @close="pdfDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.PPT_Preview') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="pdfFullscreen = !pdfFullscreen"></el-button>
      </div>
      <div @click="handleMousedown">
        <pdf :src="pdfobj.pathUrl" :key="1" :page="pdfobj.page"></pdf>
      </div>
      <div slot="footer" class="block">
        <el-pagination @current-change="handleCurrentChange" :current-page="pdfobj.page" :page-size='1'
          layout="total, prev, pager, next, jumper" :total="pdfobj.numPages">
        </el-pagination>
      </div>
    </el-dialog>
  </div>
</template>
  
<script>
import Simditor from "../../components/Simditor";
import api from "../../api";
import pdf from 'vue-pdf'

export default {
  name: "PPT",
  components: {
    Simditor,
    pdf
  },
  data() {
    return {
      rules: {
        _id: {
          required: true,
          message: this.$i18n.t("m.Display_ID_Is_Required"),
          trigger: "blur",
        },
        title: {
          required: true,
          message: this.$i18n.t("m.Title_Is_Required"),
          trigger: "blur",
        }
      }, // from表单判断规则
      PPT: {
        visible: true,
        tags: [],
      }, // PPTfrom表单
      title: '', // 标题
      mode: '', // 修改还是新增
      inputVisible: false, // 标签是否显示输入框
      error: { // 错误提示
        tags: "",
        UploadPPT: ""
      },
      tagInput: '', // tag输入框
      routeName: '', // 路由名称
      pdfDialogVisible: false, // pdf dialog
      pdfFullscreen: false, // pdf全屏
      pdfobj: {
        pathUrl: '', // pdf路径
        numPages: undefined, // pdf页数
        page: 1,
      }
    };
  },
  mounted() {
    this.routeName = this.$route.name;
    if (this.routeName === "edit-PPT") {
      this.mode = "edit";
      this.title = this.$i18n.t("m.Edit_PPT");
      api.getPPT(this.$route.params.PPTId).then((res) => {
        let data = res.data.data;
        this.PPT = data;
        this.testCaseUploaded = true;
      });
    } else {
      this.mode = "add";
      this.title = this.$i18n.t("m.Add_PPT");
    }
  },
  watch: {
    $route() {
      this.$refs.form.resetFields();
      this.PPT = this.rePPT;
    },
  },
  methods: {
    querySearch(queryString, cb) {
      api.getPPTTagList({ keyword: queryString }).then((res) => {
        let tagList = [];
        for (let tag of res.data.data) {
          tagList.push({ value: tag.name });
        }
        cb(tagList);
      }).catch(() => { });
    },
    addTag() {
      let inputValue = this.tagInput;
      if (inputValue) {
        this.PPT.tags.push(inputValue);
      }
      this.inputVisible = false;
      this.tagInput = "";
    },
    closeTag(tag) {
      this.PPT.tags.splice(this.PPT.tags.indexOf(tag), 1);
    },
    uploadSucceeded(response) {
      if (response.error) {
        this.$error(response.data);
        return;
      }
      this.PPT.path = response.file_path
      this.testCaseUploaded = true;
    },
    uploadFailed() {
      this.$error(this.$i18n.t('m.Upload_Failed'));
    },
    submit() {
      if (!this.PPT.tags.length) {
        this.error.tags = this.$i18n.t('m.Please_Add_At_Least_One_Tag');
        this.$error(this.error.tags);
        return;
      }
      if (!this.testCaseUploaded) {
        this.error.testCase = this.$i18n.t('m.PPT_Is_Not_Uploaded_Yet');
        this.$error(this.error.testCase);
        return;
      }
      let funcName = {
        "create-PPT": "createPPT",
        "edit-PPT": "editPPT",
      }[this.routeName];
      api[funcName](this.PPT).then((res) => {
        this.$router.push({ name: "PPT-list" });
      }).catch(() => { });
    },
    // 打开PPT
    goOppenPPT(url) {
      this.pdfobj.pathUrl = pdf.createLoadingTask(url)
      console.log(this.pdfobj.pathUrl);
      this.pdfobj.pathUrl.promise.then(pdf => {
        this.pdfobj.numPages = pdf.numPages;
      });
      this.pdfDialogVisible = true
      // window.open('http://view.xdocin.com/view?src=' + encodeURIComponent(url) + '&printable=false&watermark=书客编程')
    },
    // PPT换页
    handleCurrentChange(item) {
      this.pdfobj.page = item
    },
    // 鼠标点击事件
    handleMousedown(e) {
      this.pdfobj.page = this.pdfobj.page + 1 > this.pdfobj.numPages ? this.pdfobj.numPages : this.pdfobj.page + 1
    }
  },
  destroyed() {
    document.onkeydown = null // 取消键盘监听事件
  },
  watch: {
    // 监听PDF事件
    pdfDialogVisible(newvalue, oldvalue) {
      if (newvalue) {
        document.onkeydown = (e) => {
          //事件对象兼容
          let e1 = e || event || window.event || arguments.callee.caller.arguments[0]
          //键盘按键判断:左箭头-37;上箭头-38；右箭头-39;下箭头-40
          if ((e1 && e1.keyCode == 37) || (e1 && e1.keyCode == 38)) {
            this.pdfobj.page = this.pdfobj.page - 1 < 1 ? 1 : this.pdfobj.page - 1
          } else if ((e1 && e1.keyCode == 39) || (e1 && e1.keyCode == 40)) {
            this.pdfobj.page = this.pdfobj.page + 1 > this.pdfobj.numPages ? this.pdfobj.numPages : this.pdfobj.page + 1
          }
        }
      } else {
        document.onkeydown = null
      }
    }
  }
};
</script>
  
<style lang="less" scoped>
.PPT {

  .input-new-tag {
    width: 78px;
  }

  .button-new-tag {
    height: 24px;
    line-height: 22px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .tags {
    .el-tag {
      margin-right: 10px;
    }
  }
}
</style>
  
<style>
.PPT-tag-poper {
  width: 200px !important;
}

.dialog-compile-error {
  width: auto;
  max-width: 80%;
  overflow-x: scroll;
}
</style>
  
  