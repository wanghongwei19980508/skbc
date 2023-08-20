

<template>
  <div>
    <el-drawer :title="title" :visible.sync="drawer" :direction="direction" :before-close="handleClose" :size="width">
      <vFrom class="searchInput" labelWidth="100px" ref="searchSubmitForm" size="default" :searchData="searchData"
        :searchForm="searchForm" @fromSubmit="onSubmit" :cancelBtn="false">
        <template slot="avatar">
          <div class="imgBox" @click="pictureDialogVisible = true">
            <el-avatar :size="80" :src="searchData.avatar" @error="errorHandler">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png" />
            </el-avatar>
            <div class="avatar-mask">
              <div class="mask-content">
                <i class="el-icon-camera" size="50"></i>
              </div>
            </div>
          </div>
        </template>
      </vFrom>
    </el-drawer>
    <el-dialog :visible="pictureDialogVisible" :title="$t('m.Avatar_Setting')" :fullscreen="pictureFullscreen"
      :close-on-click-modal="false" @close="pictureDialogVisible = false, uploadPic.imgSrc = ''">
      <div slot="title">
        <h2>{{ $t("m.Avatar_Setting") }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="pictureFullscreen = !pictureFullscreen"></el-button>
      </div>
      <template v-if="!uploadPic.imgSrc">
        <el-upload drag class="mini-container" :before-upload="handleSelectFile" action="">
          <div style="padding: 30px 0">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text"> 将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传jpg/png文件,且不超过500kb</div>
          </div>
        </el-upload>
      </template>
      <template v-else>
        <div class="flex-container">
          <div class="cropper-main inline">
            <vueCropper ref="cropper" autoCrop :fixed="true" :autoCropWidth="200" :autoCropHeight="200"
              :img="uploadPic.imgSrc" :outputSize="uploadPic.size" :outputType="uploadPic.outputType" :info="true"
              @realTime="realTime">
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
    </el-dialog>
    <el-dialog :visible.sync="uploadModalVisible" title="头像确认">
      <div class="upload-modal">
        <p class="notice">头像将被设置为:</p>
        <img :src="uploadImgSrc" />
      </div>
      <div slot="footer">
        <el-button @click="doUploadPic" :loading="loadingUploadBtn">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import api from "@admin/api.js"
import vFrom from "@admin/components/vFrom.vue"
import { addCustomerForm } from "./config.js"
import { VueCropper } from "vue-cropper";

export default {
  name: "addCustomer",
  components: {
    vFrom,
    VueCropper
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    direction: {
      type: String,
      default: 'rtl'
    },
    drawer: {
      type: Boolean,
      default: false
    },
    width: {
      type: String,
      default: '40%'
    },
    searchData: {
      type: Object,
      default: () => { }
    },
  },
  data() {
    return {
      searchForm: addCustomerForm, // 表格配置
      pictureDialogVisible: false, // picture dialog
      pictureFullscreen: false, // picture全屏
      uploadPic: { // 头像设置
        imgSrc: "",
        size: 0.8,
        outputType: "png",
      },
      uploadModalVisible: false, // 图象裁剪 dialog
      preview: {}, // 图象裁剪参数
      uploadImgSrc: "",  // 图象裁剪地址
      loadingUploadBtn: false // 确认loading
    };
  },
  mounted() {
    this.configProperty() // 配置回调函数
  },
  methods: {
    // 配置回调函数
    configProperty() {

    },
    // 提交
    onSubmit(item) {
      if (this.searchData.id) {
        api.editClue(this.searchData).then((res) => {
          this.$emit('fromCancel', { label: 'courseArrangementDrawer', showPopover: false })
        })
      } else {
        api.addClue(this.searchData).then((res) => {
          this.$emit('fromCancel', { label: 'courseArrangementDrawer', showPopover: false })
        })
      }
    },
    // 关闭抽屉
    handleClose() {
      this.$emit('fromCancel', { label: 'courseArrangementDrawer', showPopover: true })
    },
    // 图片加载失败
    errorHandler() {
      return true
    },
    // 图片类型校验
    checkFileType(file) {
      if (!/\.(gif|jpg|jpeg|png|bmp|GIF|JPG|PNG)$/.test(file.name)) {
        this.$Notice.warning({
          title: "文件类型不支持", desc: file.name + "的格式不正确，请只选择图像",
        });
        return false;
      }
      return true;
    },
    // 图片大小校验
    checkFileSize(file) {
      if (file.size > 2 * 1024 * 1024) {
        this.$Notice.warning({
          title: "超过最大尺寸限制", desc: "文件 " + file.name + "图片太大,你可以上传大小不超过2MB的图片",
        });
        return false;
      }
      return true;
    },
    // 选择头像文件
    handleSelectFile(file) {
      if (!(this.checkFileType(file) && this.checkFileSize(file))) {
        return false;
      }
      let reader = new window.FileReader();
      reader.onload = (e) => {
        this.uploadPic.imgSrc = e.target.result;
      };
      reader.readAsDataURL(file);
      return false;
    },
    // 图象裁剪
    realTime(data) {
      this.preview = data;
    },
    // 图象旋转
    rotate(direction) {
      if (direction === "left") {
        this.$refs.cropper.rotateLeft();
      } else {
        this.$refs.cropper.rotateRight();
      }
    },
    // 取消图象裁剪
    reselect() {
      this.$confirm("你确定取消更改吗?", "提示", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning", }).then(() => {
        this.uploadPic.imgSrc = "";
      }).catch(() => { });
    },
    // 图象裁剪确认
    finishCrop() {
      this.$refs.cropper.getCropData((data) => {
        this.uploadImgSrc = data;
        this.uploadModalVisible = true;
      });
    },
    // 图象上传
    doUploadPic() {
      this.$refs.cropper.getCropBlob((blob) => {
        let form = new window.FormData();
        let file = new window.File([blob], "avatar." + this.uploadPic.outputType);
        form.append("image", file);
        if (this.searchData.avatar) {
          form.append("original_filepath", this.searchData.avatar);
        }
        this.loadingUploadBtn = true;
        this.$http({
          method: "post",
          url: "admin/upload_image",
          data: form,
          headers: { "content-type": "multipart/form-data" },
        }).then((res) => {
          this.searchData.avatar = res.data.file_path;
          this.loadingUploadBtn = false;
          this.uploadModalVisible = this.pictureDialogVisible = false;
          this.uploadPic.imgSrc = "";
          if (this.searchData.id) {
            api.editClue(this.searchData).then((res) => { })
          }
        }, () => {
          this.uploadModalVisible = this.pictureDialogVisible = false;
          this.uploadPic.imgSrc = "";
        });
      });
    },
  },
  computed: {
    previewStyle() {
      return {
        width: this.preview.w + "px",
        height: this.preview.h + "px",
        overflow: "hidden",
      };
    },
  },
  watch: {
  },
};
</script>
    
<style lang="less" scoped>
.imgBox {
  margin: 0 70px 0 20px;
  cursor: pointer;
  position: relative;

  &:hover {
    .avatar-mask {
      opacity: 0.5;
    }
  }
}

.avatar-mask {
  transition: opacity 0.2s ease-in;
  z-index: 1;
  border-radius: 50%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 80px;
  height: 80px;
  background: black;
  opacity: 0;
  cursor: pointer;

  .mask-content {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 3;
    color: #fff;
    font-size: 16px;
    text-align: center;
    transform: translate(-50%, -50%);

    .text {
      white-space: nowrap;
    }
  }
}

.mini-container {
  display: inline-flex;
  width: 100%;
  justify-content: center;
}


.flex-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  margin-bottom: 10px;

  .inline {
    display: inline-block;
  }

  .cropper-main {
    flex: none;
    width: 400px;
    height: 300px;
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
    width: 400px;
    height: 300px;
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
<style>
.el-upload-dragger {
  height: auto;
}
</style>