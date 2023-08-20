<template>
  <div class="view">
    <Panel :title="$t('m.SMTP_Config')">
      <el-form label-position="left" label-width="70px" :model="smtp">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item :label="$t('m.Server')" required>
              <el-input v-model="smtp.server" placeholder="SMTP Server Address"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="$t('m.Port')" required>
              <el-input type="number" v-model="smtp.port" placeholder="SMTP Server Port"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="$t('m.Email')" required>
              <el-input v-model="smtp.email" placeholder="Account Used To Send Email"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="$t('m.Password')" label-width="90px" required>
              <el-input v-model="smtp.password" type="password" placeholder="SMTP Server Password"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-button type="primary" @click="saveSMTPConfig">{{ $t('m.Save') }}</el-button>
      <el-button type="warning" @click="testSMTPConfig" v-if="saved" :loading="loadingBtnTest">{{ $t('m.Send_Test_Email')
      }}</el-button>
    </Panel>

    <Panel :title="$t('m.Website_Config')">
      <el-form label-position="left" label-width="100px" ref="form" :model="websiteConfig">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item :label="$t('m.Base_Url')" required>
              <el-input v-model="websiteConfig.website_base_url" placeholder="Website Base Url"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Name')" required>
              <el-input v-model="websiteConfig.website_name" placeholder="Website Name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Shortcut')" required>
              <el-input v-model="websiteConfig.website_name_shortcut" placeholder="Website Name Shortcut"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.Footer')" required>
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" v-model="websiteConfig.website_footer"
                placeholder="Website Footer HTML"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-col :span="12">
              <el-form-item :label="$t('m.Allow_Register')" label-width="200px">
                <el-switch v-model="websiteConfig.allow_register" active-color="#13ce66" inactive-color="#ff4949">
                </el-switch>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="$t('m.Submission_List_Show_All')" label-width="200px">
                <el-switch v-model="websiteConfig.submission_list_show_all" active-color="#13ce66"
                  inactive-color="#ff4949">
                </el-switch>
              </el-form-item>
            </el-col>
          </el-col>
        </el-row>
      </el-form>
      <save @click.native="saveWebsiteConfig"></save>
    </Panel>

    <Panel :title="$t('m.Slide_Shows')">
      <div slot="header">
        <el-button icon="el-icon-delete" type="danger" plain @click="clearSWPCached">
          {{ $t('m.Clear_cached_image') }}
        </el-button>
      </div>
      <el-table v-loading="ssloading" element-loading-text="loading" ref="table" :data="slideshows" style="width: 100%">
        <el-table-column width="200" prop="pic" :label="$t('m.PIC')">
          <template slot-scope="scope">
            <el-image :src="scope.row.pic" :preview-src-list="[scope.row.pic]">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
        <el-table-column prop="uploader" :label="$t('m.Uploader')"> </el-table-column>
        <el-table-column width="200" prop="visible" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text="" @change="updateSlideshows()">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('m.Operation')" width="200">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEditSlideshow(scope)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_Slide_Show')"
              @click.native="deleteSlideshow(scope.row)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goUploadSlideshow" icon="el-icon-plus">{{ $t('m.Upload') }}
        </el-button>
      </div>
    </Panel>

    <Panel :title="$t('m.Softwares')">
      <div slot="header">
        <el-button icon="el-icon-delete" type="danger" plain @click="clearSWPCached">
          {{ $t('m.Clear_cached_image') }}
        </el-button>
      </div>
      <el-table v-loading="loading" element-loading-text="loading" ref="table" :data="softwares" style="width: 100%">
        <el-table-column width="200" prop="pic" :label="$t('m.PIC')">
          <template slot-scope="scope">
            <el-image :src="scope.row.pic" style="width: 40%"> </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" :label="$t('m.Title')"> </el-table-column>
        <el-table-column prop="uploader" :label="$t('m.Uploader')"> </el-table-column>
        <el-table-column width="200" prop="visible" :label="$t('m.Visible')">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.visible" active-text="" inactive-text="" @change="updateSoftwares()">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column fixed="right" :label="$t('m.Operation')" width="200">
          <div slot-scope="scope">
            <icon-btn :name="$t('m.Edit')" icon="edit" @click.native="goEditSoftware(scope)"></icon-btn>
            <icon-btn icon="trash" :name="$t('m.Delete_Softwares')" @click.native="deleteSoftware(scope.row)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-button type="primary" size="small" @click="goUploadSoftware" icon="el-icon-plus">{{ $t('m.Upload') }}
        </el-button>
      </div>
    </Panel>
    <el-dialog :title="dialogTitle" width="80%" :visible.sync="EditDialogVisible">
      <el-form label-width="100px">
        <el-form-item :label="$t('m.Title')">
          <el-input v-model="currentRow.title"></el-input>
        </el-form-item>
        <el-form-item :label="$t('m.Description')" v-if="currentRow.description != undefined">
          <el-input v-model="currentRow.description"></el-input>
        </el-form-item>
        <el-form-item :label="$t('m.Url')">
          <el-input v-model="currentRow.url"></el-input>
        </el-form-item>
        <el-form-item :label="$t('m.Visible')">
          <el-switch v-model="currentRow.visible" active-text="" inactive-text="">
          </el-switch>
        </el-form-item>
        <el-form-item :label="$t('m.Picture')">
          <el-row>
            <el-col :span="6">
              <img :src="currentRow.pic" style="width: 40%" v-if="currentRow.description != undefined" />
              <img :src="currentRow.pic" style="width: 100%" v-else />
            </el-col>
            <el-col :span="18">
              <template v-if="!uploadPic.imgSrc">
                <el-upload drag class="mini-container" action="" :before-upload="handleSelectFile">
                  <div style="padding: 30px 0">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">
                      将文件拖到此处，或<em>点击上传</em>
                    </div>
                    <div class="el-upload__tip" slot="tip">
                      只能上传jpg/png文件，且不超过500kb
                    </div>
                  </div>
                </el-upload>
              </template>

              <template v-else>
                <div class="flex-container">
                  <div class="cropper-main inline">
                    <vueCropper ref="cropper" autoCrop :fixed="currentRow.description != undefined" :autoCropWidth="200"
                      :autoCropHeight="200" :img="uploadPic.imgSrc" :outputSize="uploadPic.size"
                      :outputType="uploadPic.outputType" :info="true" @realTime="realTime">
                    </vueCropper>
                  </div>
                  <el-button-group vertical class="cropper-btn">
                    <el-button @click="rotate('left')" icon="el-icon-refresh-left">
                    </el-button>
                    <el-button @click="rotate('right')" icon="el-icon-refresh-right">
                    </el-button>
                    <el-button @click="reselect" icon="el-icon-close">
                    </el-button>
                    <el-button @click="finishCrop" icon="el-icon-check">
                    </el-button>
                  </el-button-group>
                  <div class="cropper-preview" :style="previewStyle">
                    <div :style="preview.div">
                      <img :src="uploadPic.imgSrc" :style="preview.img" />
                    </div>
                  </div>
                </div>
              </template>
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>

      <span slot="footer">
        <cancel @click.native="EditDialogVisible = false"></cancel>
        <save @click.native="
          currentRow.description != undefined
            ? updateSoftwares()
            : updateSlideshows()
        "></save>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="uploadModalVisible" title="Upload the avatar">
      <div class="upload-modal">
        <p class="notice">The pic will be set to:</p>
        <img :src="uploadImgSrc" />
      </div>
      <div slot="footer">
        <el-button @click="doUploadPic" :loading="loadingUploadBtn">
          upload
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "../../api.js";
import { VueCropper } from "vue-cropper";
export default {
  components: {
    VueCropper,
  },
  name: "Conf",
  data() {
    return {
      init: false,
      saved: false,
      loadingBtnTest: false,
      uploadModalVisible: false,
      preview: {},
      loadingSaveBtn: false,
      smtp: {
        server: "smtp.example.com",
        port: 465,
        password: "",
        email: "email@example.com",
      },
      dialogTitle: "",
      currentRow: {},
      loading: false,
      ssloading: false,
      EditDialogVisible: false,
      websiteConfig: {},
      softwares: [],
      uploadImgSrc: "",
      uploadPic: {
        imgSrc: "",
        size: 0.8,
        outputType: "png",
      },
      slideshows: [],
      loadingUploadBtn: false // 确认loading
    };
  },
  mounted() {
    api.getSMTPConfig().then((res) => {
      if (res.data.data) {
        this.smtp = res.data.data;
      } else {
        this.init = true;
        this.$warning("Please setup SMTP config at first");
      }
    });
    api
      .getWebsiteConfig()
      .then((res) => {
        this.websiteConfig = res.data.data;
      })
      .catch(() => { });
    this.getSoftwares();
    this.getSlideshows();
  },
  methods: {
    saveSMTPConfig() {
      if (!this.init) {
        api.editSMTPConfig(this.smtp).then(
          () => {
            this.saved = true;
          },
          () => { }
        );
      } else {
        api.createSMTPConfig(this.smtp).then(
          () => {
            this.saved = true;
          },
          () => { }
        );
      }
    },
    checkFileType(file) {
      if (!/\.(gif|jpg|jpeg|png|bmp|GIF|JPG|PNG)$/.test(file.name)) {
        this.$Notice.warning({
          title: "File type not support",
          desc:
            "The format of " +
            file.name +
            " is incorrect ，please choose image only.",
        });
        return false;
      }
      return true;
    },
    checkFileSize(file) {
      // max size is 2MB
      if (file.size > 2 * 1024 * 1024) {
        this.$Notice.warning({
          title: "Exceed max size limit",
          desc:
            "File " +
            file.name +
            " is too big, you can upload a image up to 2MB in size",
        });
        return false;
      }
      return true;
    },
    handleSelectFile(file) {
      let isOk = this.checkFileType(file) && this.checkFileSize(file);
      if (!isOk) {
        return false;
      }
      let reader = new window.FileReader();
      reader.onload = (e) => {
        this.uploadPic.imgSrc = e.target.result;
      };
      reader.readAsDataURL(file);
      return false;
    },
    realTime(data) {
      this.preview = data;
    },
    rotate(direction) {
      if (direction === "left") {
        this.$refs.cropper.rotateLeft();
      } else {
        this.$refs.cropper.rotateRight();
      }
    },
    reselect() {
      this.$confirm("Are you sure to disgard the changes?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.uploadPic.imgSrc = "";
        })
        .catch(() => { });
    },
    finishCrop() {
      this.$refs.cropper.getCropData((data) => {
        this.uploadImgSrc = data;
        this.uploadModalVisible = true;
      });
    },
    doUploadPic() {
      this.$refs.cropper.getCropBlob((blob) => {
        let form = new window.FormData();
        let file = new window.File(
          [blob],
          "avatar." + this.uploadPic.outputType
        );
        form.append("image", file);
        form.append("itemId", this.currentRow.id);
        if (this.currentRow.description != undefined) {
          form.append("subject", "softwares");
        } else {
          form.append("subject", "slideshows");
        }
        this.loadingUploadBtn = true;
        this.$http({
          method: "post",
          url: "admin/pic_upload",
          data: form,
          headers: { "content-type": "multipart/form-data" },
        }).then(
          (res) => {
            this.currentRow.pic = res.data.data;
            this.loadingUploadBtn = false;
            this.$success("Successfully set new pic");
            this.uploadModalVisible = false;
            this.uploadPic.imgSrc = "";
          },
          () => {
            this.loadingUploadBtn = false;
          }
        );
      });
    },
    getSlideshows() {
      api
        .getSlideshows()
        .then((res) => {
          this.slideshows = res.data.data;
        })
        .catch(() => { });
    },
    goUploadSlideshow() {
      this.currentRow = {
        id: this.slideshows.length,
        pic: "",
        visible: false,
        title: "",
        uploader: this.user.username,
      };
      this.dialogTitle = "Sure to upload the Slide Show?";
      this.EditDialogVisible = true;
    },
    updateSlideshows() {
      if (this.currentRow.id == this.slideshows.length) {
        this.slideshows.push(this.currentRow);
      }
      for (let ss of this.slideshows) {
        ss = {
          title: ss.title,
          url: ss.url,
          pic: ss.pic,
          visible: ss.visible,
          uploader: ss.uploader,
        };
      }
      api
        .editSlideshows({ slideshows: this.slideshows })
        .then(() => { })
        .catch(() => { });
      this.EditDialogVisible = false;
      this.dialogTitle = "";
    },
    goEditSlideshow(scope) {
      this.EditDialogVisible = false;
      this.dialogTitle = "Sure to update the Slide Show?";
      this.handleEdit(scope.row);
    },
    clearSSPCached() {
      api
        .clearSSPCached()
        .then((res) => { })
        .catch(() => { });
    },
    deleteSlideshow(row) {
      this.$confirm("此操作将永久删除该轮播图, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.slideshows.splice(row.id, 1);
          this.currentRow = {};
          this.updateSlideshows();
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    getSoftwares() {
      api
        .getSoftwaresConfig()
        .then((res) => {
          this.softwares = res.data.data;
          let i = 0;
          for (let sf of this.softwares) {
            sf.id = i;
            i++;
          }
        })
        .catch(() => { });
    },
    updateSoftwares() {
      if (this.currentRow.id == this.softwares.length) {
        this.softwares.push(this.currentRow);
      }
      for (let sf of this.softwares) {
        sf = {
          title: sf.title,
          description: sf.description,
          url: sf.url,
          pic: sf.pic,
          visible: sf.visible,
          uploader: sf.uploader,
        };
      }
      api
        .editSoftwaresConfig({ softwares: this.softwares })
        .then(() => { })
        .catch(() => { });
      this.EditDialogVisible = false;
    },
    goUploadSoftware() {
      this.currentRow = {
        id: this.softwares.length,
        pic: "",
        visible: false,
        title: "",
        description: "",
        uploader: this.user.username,
      };
      this.dialogTitle = "Sure to upload the Software?";
      this.EditDialogVisible = true;
    },
    goEditSoftware(scope) {
      this.EditDialogVisible = false;
      this.dialogTitle = "Sure to update the Software?";
      this.handleEdit(scope.row);
    },
    clearSWPCached() {
      api
        .clearSWPicCached()
        .then((res) => { })
        .catch(() => { });
    },
    deleteSoftware(row) {
      this.$confirm("此操作将永久删除该软件信息, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.softwares.splice(row.id, 1);
          this.currentRow = {};
          this.updateSoftwares();
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    handleEdit(row) {
      this.currentRow = row;
      this.EditDialogVisible = true;
    },
    testSMTPConfig() {
      this.$prompt("Please input your email", "", {
        inputPattern:
          /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: "Error email format",
      })
        .then(({ value }) => {
          this.loadingBtnTest = true;
          api.testSMTPConfig(value).then(
            () => {
              this.loadingBtnTest = false;
            },
            () => {
              this.loadingBtnTest = false;
            }
          );
        })
        .catch(() => { });
    },
    saveWebsiteConfig() {
      api
        .editWebsiteConfig(this.websiteConfig)
        .then(() => { })
        .catch(() => { });
    },
  },
  computed: {
    ...mapGetters(["user"]),
    previewStyle() {
      return {
        width: this.preview.w + "px",
        height: this.preview.h + "px",
        overflow: "hidden",
      };
    },
  },
};
</script>

<style scoped lang="less">
.setting-main {
  position: relative;
  margin: 10px 40px;
  padding-bottom: 20px;

  .setting-content {
    margin-left: 20px;
  }

  .mini-container {
    display: inline-flex;
    width: 300px;
  }
}

.inline {
  display: inline-block;
}

.copper-img {
  width: 400px;
  height: 300px;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  margin-bottom: 10px;

  .cropper-main {
    flex: none;
    .copper-img;
  }

  .cropper-btn {
    display: grid;
    flex: none;
    vertical-align: top;
  }

  .cropper-preview {
    flex: none;
    /*margin: 10px;*/
    margin-left: 20px;
    box-shadow: 0 0 1px 0;
    .copper-img;
  }
}

.upload-modal {
  .notice {
    font-size: 16px;
    display: inline-block;
    vertical-align: top;
    padding: 10px;
    padding-right: 15px;
  }
}
</style>
