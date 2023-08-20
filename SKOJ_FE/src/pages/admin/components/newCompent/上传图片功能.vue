

<template>
  <div>
    <el-button @click="transactionRecordDialogVisible = true">图片上传框</el-button>
    <el-dialog :visible="transactionRecordDialogVisible" :title="$t('m.Transaction_Record')"
      :fullscreen="transactionRecordFullscreen" :close-on-click-modal="false"
      @close="transactionRecordDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Transaction_Record') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="transactionRecordFullscreen = !transactionRecordFullscreen"></el-button>
      </div>
      <el-upload action="/api/admin/upload_file" list-type="picture-card" accept=".jpg,.jpeg,.png,.bmp,.gif"
        :file-list="transactionRecord.fileList" :on-preview="handlePictureCardPreview" :on-remove="handleRemove"
        :on-success="handleSuccess">
        <i class="el-icon-plus"></i>
      </el-upload>
    </el-dialog>
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>
  </div>
</template>
<script>

export default {
  data() {
    return {
      transactionRecordDialogVisible: false, // 成交记录dialog
      transactionRecordFullscreen: false, // 成交记录全屏
      transactionRecord: { // 成交记录
        fileList: [{
          response: { success: true, msg: 'Success', file_path: '/public/upload/ed59481f3c.png', file_name: '截图20230415134912.png' },
          url: "http://localhost:8080/public/upload/ed59481f3c.png"
        }]
      },
      dialogImageUrl: '', // dialog图片地址
      dialogVisible: false, // 图片查看弹窗
      pathAddress: 'http://localhost:8080', // 图片地址
    };
  },
  mounted() {

  },
  methods: {
    // 上传成功
    handleSuccess(response, file, fileList) {
      this.transactionRecord.fileList = fileList.map((item) => {
        return { response: item.response, url: this.pathAddress + item.response.file_path }
      })
    },
    // 上传移除
    handleRemove(file, fileList) {
      this.transactionRecord.fileList = fileList.map((item) => {
        return { response: item.response, url: this.pathAddress + item.response.file_path }
      })
    },
    // 查看图片
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    // 提交
    onSubmit(item) {
      if (this.transactionRecord.fileList.length == 0) {
        this.$error('请提交成交记录图片');
        return
      }
    }
  },
  watch: {
  },
};
</script>
      
<style lang="less" scoped></style>