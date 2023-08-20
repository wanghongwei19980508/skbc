<template>
  <Panel>
    <div slot="title">
      <h3 @click="isOpen = !isOpen" v-if="assignments.length != 0 || pptList.length != 0">
        <i :class="{ rotate: isOpen }" class="el-icon-caret-right"></i>
        {{ title }}
      </h3>
      <h3 v-else style="margin-left: 15px">
        {{ title }}
      </h3>
    </div>
    <div v-html="content" style="font-size: large; margin-left: 3%; margin-right: 3%"></div>
    <div class="body" v-show="isOpen" v-if="pptList.length != 0">
      <el-descriptions v-for="PPT in pptList" :key="'ppt' + PPT.id" :title="'【' + $t('m.PPT') + '】' + PPT.name">
        <div slot="extra">
          <el-button type="primary" size="small" @click="goOppenPPT(PPT.path)">去查看</el-button>
        </div>
      </el-descriptions>
    </div>
    <div class="body" v-show="isOpen" v-if="assignments.length != 0">
      <Card v-for="assignment in assignments" :key="assignment.id" :title="assignment.title">
        <el-descriptions v-for="objectiveProblem in assignment.objectiveProblem"
          :key="'objectiveProblem' + objectiveProblem.id"
          :title="'【' + $t('m.Objective_Problems') + '】' + objectiveProblem.title">
          <div slot="extra">
            <el-button type="primary" size="small"
              @click="goObjectiveProblem(assignment.id, objectiveProblem._id)">去做题</el-button>
          </div>
        </el-descriptions>
        <el-descriptions v-for="problem in assignment.problem" :key="'problem' + problem.id"
          :title="'【' + $t('m.Problems') + '】' + problem.title">
          <div slot="extra">
            <el-button type="primary" size="small" @click="goProblem(assignment.id, problem._id)">去做题</el-button>
          </div>
        </el-descriptions>
      </Card>
    </div>
    <el-dialog :visible="pdfDialogVisible" :title="$t('m.Historical_Record')" :fullscreen="pdfFullscreen"
      :close-on-click-modal="false" @close="pdfDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.PPT_Preview') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="pdfFullscreen = !pdfFullscreen"></el-button>
      </div>
      <div @click="handleMousedown">
        <pdf :src="pdfobj.pathUrl" key="pdf" :page="pdfobj.page"></pdf>
      </div>
      <div slot="footer" class="block">
        <el-pagination @current-change="handleCurrentChange" :current-page="pdfobj.page" :page-size='1'
          layout="total, prev, pager, next, jumper" :total="pdfobj.numPages">
        </el-pagination>
      </div>
    </el-dialog>
  </Panel>
</template>
  
<script>
import Panel from "../../admin/components/Panel.vue";
import pdf from 'vue-pdf'

export default {
  name: "AssignmentRow",
  components: {
    Panel,
    pdf
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: false,
    },
    assignments: {
      type: Array,
      required: false,
    },
    pptList: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      isOpen: false,
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
  },
  methods: {
    goProblem(a_id, p_id) {
      this.$router.push({
        name: "assignment-problem-details",
        params: {
          contestID: a_id,
          problemID: p_id,
        },
      });
    },
    goObjectiveProblem(a_id, p_id) {
      this.$router.push({
        name: "assignment-objective-problem-details",
        params: {
          contestID: a_id,
          objectiveProblemID: p_id,
        },
      });
      // let routeUrl = this.$router.resolve({
      //   name: "assignment-objective-problem-details",
      //   params: {
      //     contestID: a_id,
      //     objectiveProblemID: p_id,
      //   },
      // });
      // window.open(routeUrl.href, '_blank');
    },
    // 打开PPT
    goOppenPPT(url) {
      this.pdfobj.pathUrl = pdf.createLoadingTask(url)
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
.rotate {
  transform: rotate(90deg);
}
</style>
  