<template>
  <Row :gutter="32">
    <Col :span="8" v-for="(sw, index) in softwares" :key="index" class="col-card">
    <Card>
      <h3 slot="title">
        {{ sw.title }}
      </h3>
      <a href="#" slot="extra" @click.prevent="downloadSW(index)">
        <Icon type="ios-download-outline"></Icon>
        {{ $t("m.ClickToDownload") }}
      </a>
      <Row>
        <Col :span="7" style="height: 150px">
        <el-image :src="sw.pic" style="height: 80%; width: 80%">
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
        </Col>
        <Col :offset="2" :span="12">
        <h2>
          {{ sw.title }}
        </h2>
        <el-tooltip effect="dark" :content="sw.description" placement="bottom-start">
          <span type="text"
            style="color: rgb(158, 167, 180);display: -webkit-box;-webkit-line-clamp: 2;-webkit-box-orient: vertical;overflow: hidden;">
            {{ sw.description }}
          </span>
        </el-tooltip>
        <br />
        <br />
        <Button type="ghost" shape="circle" @click="downloadSW(index)">
          {{ $t("m.ClickToDownload") }}
          <Icon type="chevron-right"></Icon>
        </Button>
        </Col>
      </Row>
    </Card>
    </Col>
  </Row>
</template>

<script>
import api from "../../api.js";
export default {
  name: "SoftwareList",
  data() {
    return {
      softwares: [],
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      api.getSoftwaresConfig().then((res) => {
        this.softwares = res.data.data;
      }).catch(() => { });
    },
    downloadSW(index) {
      window.open(this.softwares[index].url);
      this.$success("已跳转下载");
    },
  },
};
</script>

<style scoped lang="less">
.col-card {
  margin-bottom: 30px;
}
</style>