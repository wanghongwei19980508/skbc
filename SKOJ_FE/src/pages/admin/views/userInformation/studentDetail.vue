

<template>
  <div class="baseInfo">
    <Panel :title="this.$i18n.t('m.Student_Details')" :style="'minHeight:calc(100vh - 170px); overflow-y: auto;'">
      <div slot="title">
        <el-page-header @back="goBack" :content="this.$i18n.t('m.Student_Details')" style="margin-top: 5px">
        </el-page-header>
      </div>
      <div class="basicInformation">
        <div class="basicInformationHeard">
          <div class="userBox">
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
            <div class="rigthBox">
              <p>{{ searchData.student_name }}</p>
              <div class="tagsBox">
                <el-tag v-for="(item, index) in searchData.tags" :type="item.type" :key="index">{{ item.content
                }}</el-tag>
              </div>
            </div>
          </div>
          <div class="buttonBox">
            <el-button size="mini" :type="'success'" @click="audition(searchData)">试听</el-button>
            <el-button size="mini" :type="'success'" @click="editData(searchData)">编辑资料</el-button>
            <el-button size="mini" :type="'success'" @click="audition(searchData)">转为历史学员</el-button>
            <el-button size="mini" :type="'success'" @click="deleteClue(searchData)">删除学员</el-button>
          </div>
        </div>
      </div>
      <vDescriptions class="searchInput" ref="searchSubmitForm" size="default" :searchData="searchData"
        :searchForm="searchForm" :title="'成员信息'" @fromCancel="goBack">
      </vDescriptions>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="报读课程" name="a">报读课程</el-tab-pane>
        <el-tab-pane label="跟进管理" name="b">
          <followUpRecord ref="followUpRecordRefq" :userData="searchData" />
        </el-tab-pane>
        <el-tab-pane label="消费管理" name="c">消费管理</el-tab-pane>
        <el-tab-pane label="上课记录" name="classRecord">
          <el-tabs type="border-card" v-model="classRecordModel" @tab-click="classRecordHandleClick">
            <el-tab-pane label="已上课记录" name="attendanceRecord">
              <classRecord v-if="classRecordModel == 'attendanceRecord'" ref="attendanceRecord" :userData="searchData">
              </classRecord>
            </el-tab-pane>
            <el-tab-pane label="待上课记录" name="waitForClassRecord">
              <waitForClassRecord v-if="classRecordModel == 'waitForClassRecord'" ref="waitForClassRecord"
                :userData="searchData"></waitForClassRecord>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
        <el-tab-pane label="考勤记录" name="e">考勤记录
        </el-tab-pane>
        <el-tab-pane label="成长档案" name="growthFile">
          <growthFile ref="growthFile" :userData="searchData"></growthFile>
        </el-tab-pane>
        <el-tab-pane label="成绩单" name="g">成绩单</el-tab-pane>
        <el-tab-pane label="小麦粒" name="h">小麦粒</el-tab-pane>
        <el-tab-pane label="优惠券" name="i">优惠券</el-tab-pane>
      </el-tabs>
    </Panel>
    <el-dialog :visible="pictureDialogVisible" :title="$t('m.Avatar_Setting')" :fullscreen="pictureFullscreen"
      :close-on-click-modal="false" @close="pictureDialogVisible = false, uploadPic.imgSrc = ''">
      <div slot="title">
        <h2>{{ $t("m.Avatar_Setting") }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="pictureFullscreen = !pictureFullscreen"></el-button>
      </div>
      <template v-if="!uploadPic.imgSrc">
        <el-upload drag class="mini-container" action="" :before-upload="handleSelectFile">
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
    <addCustomer ref="addCustomerDrawerRef" :searchData="searchData" :drawer="addCustomerDrawer" :title="'修改客户'"
      @fromCancel="handleClose" />
  </div>
</template>
<script>
import api from "@admin/api";
import vDescriptions from "@admin/components/vDescriptions.vue"
import followUpRecord from "@admin/components/newCompent/followUpRecord.vue"
import classRecord from "@admin/components/newCompent/classRecord.vue"
import addCustomer from "@admin/components/newCompent/addCustomer.vue"
import waitForClassRecord from "@admin/components/newCompent/waitForClassRecord.vue"
import growthFile from "@admin/components/newCompent/growthFile.vue"
import { searchForm } from "./config.js"
import { VueCropper } from "vue-cropper";

export default {
  name: "studentManagementView",
  components: {
    vDescriptions,
    VueCropper,
    followUpRecord,
    addCustomer,
    waitForClassRecord,
    classRecord,
    growthFile
  },
  data() {
    return {
      params: {}, // 页面传参
      activeName: 'a', // 用户tab当前页
      searchForm: searchForm,
      searchData: {},
      addCustomerDrawer: false, // 新增客户抽屉
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
      loadingUploadBtn: false, // 确认loading
      classRecordModel: 'attendanceRecord' // 上课记录tab当前页
    };
  },
  mounted() {
    this.params = this.$route.params
    if (this.params.id) {
      this.changeFormData() // 页面数据
    } else {
      this.goBack()
    }
  },
  methods: {
    // 页面数据
    changeFormData() {
      api.getClueList({ id: this.params.id }).then((res) => {
        let tags = []
        tags.push({ content: res.data.data.student_status, type: 'success' })
        if (res.data.data.student_status == '潜在学员') {
          tags.push({ content: '' + res.data.data.follow_stage, type: 'warning' })
          tags.push({ content: '意向级别:' + res.data.data.intention_level, type: 'info' })
        }
        res.data.data.tags = tags
        this.searchData = res.data.data
      })

    },
    // 返回上一页
    goBack() {
      this.$router.go(-1);
    },
    // 用户tab切换
    handleClick(tab, item) {
      if (tab.name === 'classRecord') {
        this.recaptureData()
      } else if (tab.name === 'growthFile') {
        this.$refs[tab.name].getTableData()
      }
    },
    // 上课记录tab切换
    classRecordHandleClick(tab, item) {
      this.recaptureData()
    },
    // table页面重新获取数据
    recaptureData() {
      setTimeout(() => {
        this.$refs[this.classRecordModel].$refs['tableRef'].tableChange()
      }, 100)
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
          api.editClue(this.searchData).then((res) => {
            this.changeFormData()
          })
        }, () => {
          this.uploadModalVisible = this.pictureDialogVisible = false;
          this.uploadPic.imgSrc = "";
        });
      });
    },
    // 开启抽屉
    editData(row) {
      this.addCustomerDrawer = true
    },
    // 关闭抽屉
    handleClose(row) {
      if (row.showPopover) {
        this.$confirm('确认关闭？').then(_ => {
          this.addCustomerDrawer = false
          this.$refs['addCustomerDrawerRef'].$refs['searchSubmitForm'].$refs['searchFormRef'].resetFields()
          this.changeFormData()
        }).catch(_ => { });
      } else {
        this.addCustomerDrawer = false
        this.$refs['addCustomerDrawerRef'].$refs['searchSubmitForm'].$refs['searchFormRef'].resetFields()
        this.changeFormData()
      }
    },
    // 删除用户
    deleteClue(row) {
      api.deleteClue(this.searchData.id).then((res) => { })
    }
  },
  watch: {
  },
  computed: {
    previewStyle() {
      return {
        width: this.preview.w + "px",
        height: this.preview.h + "px",
        overflow: "hidden",
      };
    },
  }
};
</script>
      
<style lang="less" scoped>
.baseInfo {
  padding: 30px 20px 0;
}

.basicInformation {
  display: flex;

  .basicInformationHeard {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;

    .userBox {
      display: flex;
      position: relative;

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

      .rigthBox {

        .tagsBox {
          height: 60px;

          span {
            margin: 0 5px;
          }
        }
      }
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