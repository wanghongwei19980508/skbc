<template>
  <Panel shadow :padding="10">
    <div slot="title">
      {{ title }}
    </div>
    <div slot="extra">
      <Button type="info" @click="init" :loading="btnLoading">{{ $t('m.Refresh') }}</Button>
    </div>
    <transition-group name="announcement-animate" mode="in-out">
      <div class="no-announcement" v-if="!announcements.length" key="no-announcement">
        <p>{{ $t('m.No_Announcements') }}</p>
      </div>
      <template>
        <ul class="announcements-container" key="list">
          <li v-for="announcement in announcements" :key="announcement.title">
            <div class="flex-container">
              <div class="title"><a class="entry" @click="goAnnouncement(announcement)">{{ announcement.title }}</a></div>
              <div class="date">{{ announcement.create_time | localtime }}</div>
              <div class="creator"> {{ $t('m.By') }} {{ announcement.created_by.username }}</div>
            </div>
          </li>
        </ul>
        <Pagination v-if="!isContest" key="page" :total="total" :page-size="limit" @on-change="getAnnouncementList">
        </Pagination>
      </template>
    </transition-group>
  </Panel>
</template>

<script>
import api from '@oj/api'
import Pagination from '@oj/components/Pagination'

export default {
  name: 'Announcement',
  components: {
    Pagination
  },
  data() {
    return {
      limit: 10,
      total: 10,
      btnLoading: false,
      announcements: [],
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.getAnnouncementList()
    },
    getAnnouncementList(page = 1) {
      this.btnLoading = true
      api.getAnnouncementList((page - 1) * this.limit, this.limit).then(res => {
        this.btnLoading = false
        this.announcements = res.data.data.results
        this.total = res.data.data.total
      }, () => {
        this.btnLoading = false
      })
    },
    goAnnouncement(announcement) {
      this.$router.push({
        name: "announcement-details",
        params: { announcementID: announcement.id },
      });
    },
  },
  computed: {
    title() {
      return this.isContest ? this.$i18n.t('m.Contest_Announcements') : this.$i18n.t('m.Announcements')
    },
    isContest() {
      return !!this.$route.params.contestID
    }
  }
}
</script>

<style scoped lang="less">
.announcements-container {
  margin-top: -10px;
  margin-bottom: 10px;

  li {
    padding-top: 15px;
    list-style: none;
    padding-bottom: 15px;
    margin-left: 20px;
    font-size: 16px;
    border-bottom: 1px solid rgba(187, 187, 187, 0.5);

    &:last-child {
      border-bottom: none;
    }

    .flex-container {
      .title {
        flex: 1 1;
        text-align: left;
        padding-left: 10px;

        a.entry {
          color: #495060;

          &:hover {
            color: #2d8cf0;
            border-bottom: 1px solid #2d8cf0;
          }
        }
      }

      .creator {
        flex: none;
        width: 200px;
        text-align: center;
      }

      .date {
        flex: none;
        width: 200px;
        text-align: center;
      }
    }
  }
}

.content-container {
  padding: 0 20px 20px 20px;
}

.no-announcement {
  text-align: center;
  font-size: 16px;
}

changeLocale .announcement-animate-enter-active {
  animation: fadeIn 1s;
}
</style>
