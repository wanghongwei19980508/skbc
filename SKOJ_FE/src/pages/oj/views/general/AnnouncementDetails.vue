<template>
  <Panel shadow :padding="10">
    <div slot="title">
      <el-page-header @back="goBack" :content="this.announcement.title" style="margin-top: 5px">
      </el-page-header>
    </div>
    <div v-katex v-html="announcement.content" key="content" class="content-container markdown-body"></div>
  </Panel>
</template>
  
<script>
import api from '@oj/api'

export default {
  name: 'AnnouncementDetails',
  components: {
  },
  data() {
    return {
      announcement: {},
    }
  },
  mounted() {
    this.getAnnouncement()
  },
  methods: {
    getAnnouncement() {
      api.getAnnouncement(this.$route.params.announcementID).then(res => {
        this.announcement = res.data.data
      }, () => { })
    },
    goBack() {
      this.$router.go(-1);
    },
  },
  computed: {
  }
}
</script>
  
<style scoped lang="less">
.content-container {
  padding: 0 20px 20px 20px;
}
.content-container{
  height: calc(100vh - 200px);
  overflow-y: auto;
}
</style>
  