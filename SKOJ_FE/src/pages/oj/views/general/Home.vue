<template>
  <Row type="flex" justify="space-around">
    <Col :span="22">
    <el-carousel v-if="slideshows.length" trigger="hover" :interval="6000" arrow="always" :height="bannerHeight + 'px'"
      type="card" @change="changeSlideshowIndex">
      <el-carousel-item v-for="(slideshow, index) of slideshows" :key="index">
        <el-image :src="slideshow.pic" class="inheritheight" @click="tourl(slideshow.url)">
        </el-image>
      </el-carousel-item>
    </el-carousel>
    </Col>
    <Col :span="22">
    <Announcements class="announcement"></Announcements>
    <panel shadow v-if="contests.length" class="contest">
      <div slot="title">
        <Button type="text" class="contest-title" @click="goContest">{{
          contests[index].title
        }}</Button>
      </div>
      <Carousel ref="carouselDom" v-model="index" trigger="hover" autoplay :autoplay-speed="6000" class="contest">
        <CarouselItem v-for="(contest, index) of contests" :key="index">
          <div class="contest-content">
            <div class="contest-content-tags">
              <Button type="info" shape="circle" size="small" icon="calendar">
                {{ contest.start_time | localtime("YYYY-M-D HH:mm") }}
              </Button>
              <Button type="success" shape="circle" size="small" icon="android-time">
                {{ getDuration(contest.start_time, contest.end_time) }}
              </Button>
              <Button type="warning" shape="circle" size="small" icon="trophy">
                {{ contest.rule_type }}
              </Button>
            </div>
            <div class="contest-content-description">
              <blockquote v-html="contest.description"></blockquote>
            </div>
          </div>
        </CarouselItem>
      </Carousel>
    </panel>
    </Col>
  </Row>
</template>

<script>
import Announcements from "./Announcements.vue";
import api from "@oj/api";
import time from "@/utils/time";
import { CONTEST_STATUS } from "@/utils/constants";

export default {
  name: "home",
  components: {
    Announcements,
  },
  data() {
    return {
      contests: [],
      index: 0,
      screenWidth: 0,
      bannerHeight: 0,
      slideshowIndex: 0,
      slideshows: [],
    };
  },
  mounted() {
    let params = { status: CONTEST_STATUS.UNDERWAY };
    api.getContestList(0, 5, params).then((res) => {
      this.contests = res.data.data.results;
    });
    params = { status: CONTEST_STATUS.NOT_START };
    api.getContestList(0, 5, params).then((res) => {
      this.contests.concat(res.data.data.results);
    });
    // 轮播图自适应高度处理 ref: https://blog.csdn.net/ZHANGYANG_1109/article/details/121103486
    this.screenWidth = window.innerWidth;
    this.bannerHeight = (300 / 1550) * this.screenWidth;
    window.onresize = () => {
      this.screenWidth = window.innerWidth;
      this.bannerHeight = (300 / 1550) * this.screenWidth;
    };
    api.getSlideshowsConfig().then((res) => {
      this.slideshows = res.data.data;
    });
  },
  methods: {
    tourl(url) {
      if (url && url != '/') {
        this.$router.push({
          path: url
        })
      } else {
        this.$success("跳转动作");
      }
    },
    changeSlideshowIndex(index) {
      this.slideshowIndex = index;
    },
    getDuration(startTime, endTime) {
      return time.duration(startTime, endTime);
    },
    goContest() {
      this.$router.push({
        name: "contest-details",
        params: { contestID: this.contests[this.index].id },
      });
    },
  },
};
</script>

<style lang="less" scoped>
.contest {
  &-title {
    font-style: italic;
    font-size: 21px;
  }

  &-content {
    padding: 0 70px 40px 70px;

    &-description {
      margin-top: 25px;
    }
  }
}

.inheritheight {
  width: 100%;
  height: inherit;
}

.announcement {
  margin-bottom: 50px;
}
</style>
