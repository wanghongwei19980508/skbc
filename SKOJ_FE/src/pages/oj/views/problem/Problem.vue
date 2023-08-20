<template>
  <div class="flex-container">
    <div id="problem-main">
      <splitpanes class="default-theme">
        <pane min-size="30">
          <!-- problem main -->
          <Panel :padding="40" shadow class="problemBox">
            <div slot="title">
              {{ problem.title }}
              <el-tooltip placement="right" :content="$t('m.Submissions')">
                <el-button type="text" @click="goSubmission()">
                  <i class="el-icon-tickets" style="font-size: 20px"></i>
                </el-button>
              </el-tooltip>
            </div>
            <div slot="extra">
              <el-button type="text" @click="codeEditorBoxShow = !codeEditorBoxShow">
                <i :class="['challenge-btn', codeEditorBoxShow ? 'el-icon-caret-right' : 'el-icon-caret-left']">{{
                  codeEditorBoxShow ? $t("m.Just_Look_At_The_Problem") : $t("m.Edit_Code") }}</i>
              </el-button>
            </div>
            <div id="problem-content" class="markdown-body" v-katex>
              <Row>
                <el-tooltip placement="bottom-start" :content="$t('m.Time_Limit')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="problem.time_limit + 'ms'"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
                <el-tooltip placement="bottom-start" :content="$t('m.Memory_Limit')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="problem.memory_limit + 'MB'"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
                <el-tooltip placement="bottom-start" :content="$t('m.IOMode')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="problem.io_mode.io_mode"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
                <el-tooltip placement="bottom-start" :content="$t('m.Level')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="$t('m.' + problem.difficulty)"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
              </Row>
              <p class="title">{{ $t("m.Description") }}</p>
              <p class="content" v-html="problem.description"></p>
              <p class="title">
                {{ $t("m.Input") }}
                <span v-if="problem.io_mode.io_mode == 'File IO'">({{ $t("m.FromFile") }}: {{ problem.io_mode.input
                }})</span>
              </p>
              <p class="content" v-html="problem.input_description"></p>

              <p class="title">
                {{ $t("m.Output") }}
                <span v-if="problem.io_mode.io_mode == 'File IO'">({{ $t("m.ToFile") }}: {{ problem.io_mode.output
                }})</span>
              </p>
              <p class="content" v-html="problem.output_description"></p>

              <div v-for="(sample, index) of problem.samples" :key="index">
                <div class="flex-container sample">
                  <div class="sample-input">
                    <p class="title">
                      {{ $t("m.Sample_Input") }} {{ index + 1 }}
                      <a class="copy" v-clipboard:copy="sample.input" v-clipboard:success="onCopy"
                        v-clipboard:error="onCopyError">
                        <Icon type="clipboard"></Icon>
                      </a>
                    </p>
                    <pre>{{ sample.input }}</pre>
                  </div>
                  <div class="sample-output">
                    <p class="title">
                      {{ $t("m.Sample_Output") }} {{ index + 1 }}
                    </p>
                    <pre>{{ sample.output }}</pre>
                  </div>
                </div>
              </div>

              <div v-if="problem.hint">
                <p class="title">{{ $t("m.Hint") }}</p>
                <Card dis-hover>
                  <div class="content" v-html="problem.hint"></div>
                </Card>
              </div>

              <div v-if="problem.source">
                <p class="title">{{ $t("m.Source") }}</p>
                <p class="content">{{ problem.source }}</p>
              </div>
            </div>
          </Panel>
        </pane>
        <pane min-size="40" v-if="codeEditorBoxShow">
          <!-- problem main end -->
          <Card :padding="20" id="submit-code" dis-hover
            :class="codeEditorBoxScreenfull ? 'codeEditorBoxScreenfull' : 'codeEditorBox'">
            <CodeMirror :value.sync="code" :languages="problem.languages" :language="language" :theme="theme"
              :screenfull="true" :screenfullBtn="codeEditorBoxScreenfull" @resetCode="onResetToTemplate"
              @changeTheme="onChangeTheme" @changeLang="onChangeLang"
              @changescreenfull="codeEditorBoxScreenfull = !codeEditorBoxScreenfull"></CodeMirror>
            <Row type="flex" justify="space-between">
              <Col :span="10">
              <div class="status" v-if="statusVisible">
                <template v-if="!this.contestID ||
                  (this.contestID && OIContestRealTimePermission)
                  ">
                  <span>{{ $t("m.Status") }}</span>
                  <Tag type="dot" :color="submissionStatus.color" @click.native="handleRoute('/status/' + submissionId)">
                    {{
                      $t("m." + submissionStatus.text.replace(/ /g, "_"))
                    }}
                  </Tag>
                </template>
                <template v-else-if="this.contestID && !OIContestRealTimePermission">
                  <Alert type="success" show-icon>{{
                    $t("m.Submitted_successfully")
                  }}</Alert>
                </template>
              </div>
              <div v-else-if="problem.my_status === 0">
                <Alert type="success" show-icon>{{
                  $t("m.You_have_solved_the_problem")
                }}</Alert>
              </div>
              <div v-else-if="this.contestID &&
                  !OIContestRealTimePermission &&
                  submissionExists
                  ">
                <Alert type="success" show-icon>{{
                  $t("m.You_have_submitted_a_solution")
                }}</Alert>
              </div>
              <div v-if="contestEnded">
                <Alert type="warning" show-icon>{{
                  $t("m.Contest_has_ended")
                }}</Alert>
              </div>
              </Col>

              <Col :span="12">
              <template v-if="captchaRequired">
                <div class="captcha-container">
                  <Tooltip v-if="captchaRequired" content="Click to refresh" placement="top">
                    <img :src="captchaSrc" @click="getCaptchaSrc" />
                  </Tooltip>
                  <Input v-model="captchaCode" class="captcha-code" />
                </div>
              </template>
              </Col>
            </Row>
          </Card>
        </pane>
      </splitpanes>
    </div>
    <div class="footer">
      <Button v-if="this.problem.std_code && Object.keys(this.problem.std_code).length"
        @click="viewSampleCodeDialogVisible = true" class="footerBtn">
        <span>{{ $t("m.View_Sample_Code") }}</span>
      </Button>
      <Button @click="code = ''" class="footerBtn">
        <span>{{ $t("m.Redo") }}</span>
      </Button>
      <Button @click="historicalRecord" class="footerBtn">
        <span>{{ $t("m.Historical_Record") }}</span>
      </Button>
      <Button @click="trialRun" class="footerBtn">
        <span>{{ $t("m.Trial_Run") }}</span>
      </Button>
      <Button type="warning" icon="edit" :loading="submitting" @click="submitCode"
        :disabled="problemSubmitDisabled || submitted" class="footerBtn">
        <span v-if="submitting">{{ $t("m.Submitting") }}</span>
        <span v-else>{{ $t("m.Submit") }}</span>
      </Button>
    </div>
    <el-dialog :visible="historyDialogVisible" :title="$t('m.Historical_Record')" :fullscreen="historyFullscreen"
      @close="historyDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Historical_Record') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="historyFullscreen = !historyFullscreen"></el-button>
      </div>
      <Table class="historyTable" :style="{ maxHeight: + historyFullscreen ? '85vh' : '60vh' }" stripe
        :disabled-hover="true" :columns="columns" :data="historyList"></Table>
    </el-dialog>
    <el-dialog :visible="trialRunDialogVisible" :title="$t('m.Historical_Record')" :fullscreen="trialRunFullscreen"
      @close="trialRunDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Trial_Run') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="trialRunFullscreen = !trialRunFullscreen"></el-button>
      </div>
      <div style="display: flex;justify-content: space-around;align-items: center;">
        <div style="width: 48%;">
          {{ $t('m.Input_Instance') }}
          <el-input type="textarea" :rows="2" :placeholder="'请输入' + $t('m.Input_Instance')" v-model="inputCode">
          </el-input>
        </div>
        <div style="width: 48%;">
          {{ $t('m.Output_Instance') }}
          <el-input type="textarea" :rows="2" :placeholder="'请输入' + $t('m.Output_Instance')" v-model="outputCode">
          </el-input>
        </div>
      </div>
      <div v-if="error !== ''" style="margin: 10px;">
        <Highlight :code="error" :language="language.content_type" :border-color="'yellow'"></Highlight>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-dropdown @command="fillInTheSampleColumn" v-if="problem.samples && problem.samples.length > 1"
          class="floatleft">
          <span class="el-dropdown-link">
            {{ $t("m.Fill_In_The_Sample_Column") }}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="(item, index) in problem.samples" :command="item" :key="index">{{
              $t("m.Fill_In_The_Sample_Column") + index }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <Button v-else-if="problem.samples" @click="fillInTheSampleColumn(problem.samples[0])" class="floatleft">
          <span>{{ $t("m.Fill_In_The_Sample_Column") }}</span>
        </Button>
        <Button @click="inputCode = '', outputCode = ''">
          <span>{{ $t("m.Reset") }}</span>
        </Button>
        <Button type="primary" @click="getTrialRun">
          <span>{{ $t("m.Trial_Run") }}</span>
        </Button>
      </span>
    </el-dialog>
    <el-dialog :visible="resultDialogVisible" :title="$t('m.Running_Result')" :fullscreen="resultFullscreen"
      @close="resultDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Running_Result') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="resultFullscreen = !resultFullscreen"></el-button>
      </div>
      <div style="display: flex;justify-content: space-around;">
        <div style="width: 48%;">
          <div class="markdown-body">
            <span>{{ $t('m.Actual_Output_Instance') }}</span>
            <pre>{{ resultCode.output }}</pre>
          </div>
          <div class="markdown-body">
            <span>{{ $t('m.Expected_Output_Instance') }}</span>
            <pre>{{ outputCode }}</pre>
          </div>
        </div>
        <div style="width: 30%;display: flex;flex-direction: column;justify-content: space-around;">
          <div class="markdown-body">
            <p>{{ $t('m.Time') }}</p>
            <el-tag>
              <span v-html="resultCode.cpu_time + 'ms'"></span>
            </el-tag>
          </div>
          <div class="markdown-body">
            <p>{{ $t('m.Memory') }}</p>
            <el-tag>
              <span v-html="(resultCode.memory / 1024 / 1024).toFixed(2) + 'MB'"></span>
            </el-tag>
          </div>
        </div>
      </div>
    </el-dialog>
    <el-dialog :visible="historyCodeDialogVisible" :title="$t('m.Historical_Content')" :fullscreen="historyCodeFullscreen"
      @close="historyCodeDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Historical_Content') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="historyCodeFullscreen = !historyCodeFullscreen"></el-button>
      </div>
      <div><span>{{ $t('m.Current_Commit') }}</span>{{ historyCode.create_time | localtime }}</div>
      <Highlight style="border: 1px solid #7c5576;" :code="historyCode.code" :language="historyCode.language"
        :border-color="status.color"></Highlight>
      <div v-if="historyCode.info && historyCode.result !== -2" :span="20">
        <Table stripe :loading="loading" :disabled-hover="true" :columns="historyCodeColumns"
          :data="historyCode.info.data"></Table>
      </div>
    </el-dialog>
    <el-dialog :visible="viewSampleCodeDialogVisible" :title="$t('m.View_Sample_Code')"
      :fullscreen="viewSampleCodeFullscreen" @close="viewSampleCodeDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.View_Sample_Code') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="viewSampleCodeFullscreen = !viewSampleCodeFullscreen"></el-button>
      </div>
      <div v-if="this.problem.std_code && Object.keys(this.problem.std_code).length">
        <el-tabs v-model="viewSampleCodeLanguage">
          <el-tab-pane v-for="(val, key, index) in problem.std_code" :key="index" :label="key" :name="key">
          </el-tab-pane>
        </el-tabs>
        <code-mirrors v-model="problem.std_code[viewSampleCodeLanguage]"
          :mode="viewSampleCodeLanguage.content_type"></code-mirrors>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="onCopyCode(problem.std_code[viewSampleCodeLanguage])">复制</el-button>
      </span>
    </el-dialog>
    <Modal v-model="graphVisible">
      <div id="pieChart-detail">
        <ECharts :options="largePie" :initOptions="largePieInitOpts"></ECharts>
      </div>
      <div slot="footer">
        <Button type="ghost" @click="graphVisible = false">{{
          $t("m.Close")
        }}</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { types } from "../../../../store";
import CodeMirror from "@oj/components/CodeMirror.vue";
import CodeMirrors from "@admin/components/CodeMirror.vue";
import storage from "@/utils/storage";
import Emitter from "@oj/components/mixins/emitter";
import { FormMixin } from "@oj/components/mixins";
import {
  JUDGE_STATUS,
  CONTEST_STATUS,
  buildProblemCodeKey,
} from "@/utils/constants";
import api from "@oj/api";
import { pie, largePie } from "./chartData";
import SplitPane from "@oj/components/SplitPane.vue";

import utils from "@/utils/utils";
import time from "@/utils/time";
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'
import Highlight from '@/pages/oj/components/Highlight'

// 只显示这些状态的图形占用
const filtedStatus = ["-1", "-2", "0", "1", "2", "3", "4", "8"];
import VueAffixBox from "vue-affix-box";
export default {
  name: "Problem",
  components: {
    CodeMirror,
    CodeMirrors,
    VueAffixBox,
    SplitPane,
    Splitpanes,
    Pane,
    Highlight
  },
  mixins: [FormMixin, Emitter],
  data() {
    return {
      paneLengthPercent: 30,
      statusVisible: false,
      captchaRequired: false,
      graphVisible: false,
      submissionExists: false,
      captchaCode: "",
      captchaSrc: "",
      contestID: "",
      problemID: "",
      submitting: false,
      code: "",
      language: "C++",
      theme: "solarized",
      submissionId: "",
      submitted: false,
      result: {
        result: 9,
      },
      problem: {
        title: "",
        description: "",
        hint: "",
        my_status: "",
        template: {},
        std_code: {},
        languages: [],
        created_by: {
          username: "",
        },
        tags: [],
        io_mode: { io_mode: "Standard IO" },
        time_limit: "",
        memory_limit: "",
      },
      pie: pie,
      largePie: largePie,
      // echarts 无法获取隐藏dom的大小，需手动指定
      largePieInitOpts: {
        width: "500",
        height: "480",
      },
      codeEditorBoxShow: true, // 是否显示代码编辑器
      codeEditorBoxScreenfull: false, // 是否全屏代码编辑器
      historyDialogVisible: false, // 历史记录dialog
      historyFullscreen: false, // 历史记录全屏
      historyList: [], // 历史记录
      trialRunDialogVisible: false, // 试运行dialog
      trialRunFullscreen: false, // 试运行全屏
      inputCode: '', // 试运行输入代码
      outputCode: '', // 试运行输出代码
      resultDialogVisible: false, // 运行结果dialog
      resultFullscreen: false, // 运行结果全屏
      resultCode: '', // 运行结果返回值
      historyCodeDialogVisible: false, // 历史内容dialog
      historyCodeFullscreen: false, // 历史内容全屏
      historyCode: { // 历史内容返回值
        result: '0',
        code: '',
        info: {
          data: []
        },
        statistic_info: {
          time_cost: '',
          memory_cost: ''
        }
      },
      viewSampleCodeDialogVisible: false, // 示例代码dialog
      viewSampleCodeFullscreen: false, // 示例代码全屏
      viewSampleCodeLanguage: '',
      error: '',
      loading: false,
      isConcat: false,
      columns: [
        {
          title: this.$i18n.t("m.When"),
          align: "center",
          render: (h, params) => {
            return h("span", time.utcToLocal(params.row.create_time));
          },
        },
        {
          title: this.$i18n.t("m.Status"),
          align: "center",
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: JUDGE_STATUS[params.row.result].color
              }
            }, this.$i18n.t('m.' + JUDGE_STATUS[params.row.result].name.replace(/ /g, '_')))
          }
        },
        {
          title: this.$i18n.t("m.Time"),
          align: "center",
          render: (h, params) => {
            return h(
              "span",
              utils.submissionTimeFormat(params.row.statistic_info.time_cost)
            );
          },
        },
        {
          title: this.$i18n.t("m.Memory"),
          align: "center",
          render: (h, params) => {
            return h(
              "span",
              utils.submissionMemoryFormat(
                params.row.statistic_info.memory_cost
              )
            );
          },
        },
        {
          title: this.$i18n.t("m.Language"),
          align: "center",
          key: "language",
          render: (h, params) => {
            if (params.row.show_link) {
              return h(
                "span",
                {
                  style: {
                    color: "#57a3f3",
                    cursor: "pointer",
                  },
                  on: {
                    click: () => {
                      this.getSubmission(params)
                    },
                  },
                },
                params.row.language
              );
            }
          },
        },
      ],
      historyCodeColumns: [
        {
          title: this.$i18n.t('m.ID'),
          align: 'center',
          type: 'index'
        },
        {
          title: this.$i18n.t('m.Status'),
          align: 'center',
          render: (h, params) => {
            return h('Tag', {
              props: {
                color: JUDGE_STATUS[params.row.result].color
              }
            }, this.$i18n.t('m.' + JUDGE_STATUS[params.row.result].name.replace(/ /g, '_')))
          }
        },
        {
          title: this.$i18n.t('m.Memory'),
          align: 'center',
          render: (h, params) => {
            return h('span', utils.submissionMemoryFormat(params.row.memory))
          }
        },
        {
          title: this.$i18n.t('m.Time'),
          align: 'center',
          render: (h, params) => {
            return h('span', utils.submissionTimeFormat(params.row.cpu_time))
          }
        }
      ],
    };
  },
  beforeRouteEnter(to, from, next) {
    let problemCode = storage.get(
      buildProblemCodeKey(to.params.problemID, to.params.contestID)
    );
    if (problemCode) {
      next((vm) => {
        vm.language = problemCode.language;
        vm.code = problemCode.code;
        vm.theme = problemCode.theme;
      });
    } else {
      next();
    }
  },
  mounted() {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false });
    this.init();
  },
  methods: {
    ...mapActions(["changeDomTitle"]),
    init() {
      this.$Loading.start();
      this.contestID = this.$route.params.contestID;
      this.problemID = this.$route.params.problemID;
      let func =
        this.$route.name === "problem-details"
          ? "getProblem"
          : "getContestProblem";
      api[func](this.problemID, this.contestID).then(
        (res) => {
          this.$Loading.finish();
          let problem = res.data.data;
          this.changeDomTitle({ title: problem.title });
          api.submissionExists(problem.id).then((res) => {
            this.submissionExists = res.data.data;
          });
          problem.languages = problem.languages.sort();
          if (
            problem.languages.includes("C++") &&
            problem.languages[0] != "C++"
          ) {
            problem.languages[0] = "C++";
            problem.languages[1] = "C";
          }
          this.problem = problem;
          if (problem.statistic_info) {
            this.changePie(problem);
          }
          if (this.problem.std_code && Object.keys(this.problem.std_code).length) {
            this.viewSampleCodeLanguage = Object.keys(this.problem.std_code)[0];
          }
          // 在beforeRouteEnter中修改了, 说明本地有code，无需加载template
          if (this.code !== "") {
            return;
          }
          // try to load problem template
          this.language = this.problem.languages[0];
          let template = this.problem.template;
          if (template && template[this.language]) {
            this.code = template[this.language];
          }
        },
        () => {
          this.$Loading.error();
        }
      );
    },
    goSubmission() {
      if (this.contestID) {
        if (this.$route.name === "contest-problem-details")
          this.$router.push({
            name: "contest-submission-list",
            params: {
              contestID: this.contestID,
              problemID: this.problemID,
            },
          });
        else {
          this.$router.push({
            name: "assignment-submission-list",
            params: {
              contestID: this.contestID,
              problemID: this.problemID,
            },
          });
        }
      } else {
        this.$router.push({
          name: "submission-list",
          params: {
            problemID: this.problemID,
          },
        });
      }
    },
    changePie(problemData) {
      // 只显示特定的一些状态
      for (let k in problemData.statistic_info) {
        if (filtedStatus.indexOf(k) === -1) {
          delete problemData.statistic_info[k];
        }
      }
      let acNum = problemData.accepted_number;
      let data = [
        { name: "WA", value: problemData.submission_number - acNum },
        { name: "AC", value: acNum },
      ];
      this.pie.series[0].data = data;
      // 只把大图的AC selected下，这里需要做一下deepcopy
      let data2 = JSON.parse(JSON.stringify(data));
      data2[1].selected = true;
      this.largePie.series[1].data = data2;

      // 根据结果设置legend,没有提交过的legend不显示
      let legend = Object.keys(problemData.statistic_info).map(
        (ele) => JUDGE_STATUS[ele].short
      );
      if (legend.length === 0) {
        legend.push("AC", "WA");
      }
      this.largePie.legend.data = legend;

      // 把ac的数据提取出来放在最后
      let acCount = problemData.statistic_info["0"];
      delete problemData.statistic_info["0"];

      let largePieData = [];
      Object.keys(problemData.statistic_info).forEach((ele) => {
        largePieData.push({
          name: JUDGE_STATUS[ele].short,
          value: problemData.statistic_info[ele],
        });
      });
      largePieData.push({ name: "AC", value: acCount });
      this.largePie.series[0].data = largePieData;
    },
    handleRoute(route) {
      this.$router.push(route);
    },
    onChangeLang(newLang) {
      if (this.problem.template[newLang]) {
        if (this.code.trim() === "") {
          this.code = this.problem.template[newLang];
        }
      }
      this.language = newLang;
    },
    onChangeTheme(newTheme) {
      this.theme = newTheme;
    },
    onResetToTemplate() {
      this.$Modal.confirm({
        content: this.$i18n.t("m.Are_you_sure_you_want_to_reset_your_code"),
        onOk: () => {
          let template = this.problem.template;
          if (template && template[this.language]) {
            this.code = template[this.language];
          } else {
            this.code = "";
          }
        },
      });
    },
    checkSubmissionStatus() {
      // 使用setTimeout避免一些问题
      if (this.refreshStatus) {
        // 如果之前的提交状态检查还没有停止,则停止,否则将会失去timeout的引用造成无限请求
        clearTimeout(this.refreshStatus);
      }
      const checkStatus = () => {
        let id = this.submissionId;
        api.getSubmission(id).then(
          (res) => {
            this.result = res.data.data;
            if (Object.keys(res.data.data.statistic_info).length !== 0) {
              this.submitting = false;
              this.submitted = false;
              clearTimeout(this.refreshStatus);
              this.init();
            } else {
              this.refreshStatus = setTimeout(checkStatus, 2000);
            }
          },
          (res) => {
            this.submitting = false;
            clearTimeout(this.refreshStatus);
          }
        );
      };
      this.refreshStatus = setTimeout(checkStatus, 2000);
    },
    submitCode() {
      if (this.code.trim() === "") {
        this.$error(this.$i18n.t("m.Code_can_not_be_empty"));
        return;
      }
      this.submissionId = "";
      this.result = { result: 9 };
      this.submitting = true;
      let data = {
        problem_id: this.problem.id,
        language: this.language,
        code: this.code,
        contest_id: this.contestID,
      };
      if (this.captchaRequired) {
        data.captcha = this.captchaCode;
      }
      const submitFunc = (data, detailsVisible) => {
        this.statusVisible = true;
        api.submitCode(data).then(
          (res) => {
            this.submissionId = res.data.data && res.data.data.submission_id;
            // 定时检查状态
            this.submitting = false;
            this.submissionExists = true;
            if (!detailsVisible) {
              this.$Modal.success({
                title: this.$i18n.t("m.Success"),
                content: this.$i18n.t("m.Submit_code_successfully"),
              });
              return;
            }
            this.submitted = true;
            this.checkSubmissionStatus();
          },
          (res) => {
            this.getCaptchaSrc();
            if (res.data.data.startsWith("Captcha is required")) {
              this.captchaRequired = true;
            }
            this.submitting = false;
            this.statusVisible = false;
          }
        );
      };

      if (this.contestRuleType === "OI" && !this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          this.$Modal.confirm({
            title: "",
            content:
              "<h3>" +
              this.$i18n.t(
                "m.You_have_submission_in_this_problem_sure_to_cover_it"
              ) +
              "<h3>",
            onOk: () => {
              // 暂时解决对话框与后面提示对话框冲突的问题(否则一闪而过）
              setTimeout(() => {
                submitFunc(data, false);
              }, 1000);
            },
            onCancel: () => {
              this.submitting = false;
            },
          });
        } else {
          submitFunc(data, false);
        }
      } else {
        submitFunc(data, true);
      }
    },
    onCopy(event) {
      this.$success("Code copied");
    },
    onCopyError(e) {
      this.$error("Failed to copy code");
    },
    // 获取历史记录
    historicalRecord() {
      let params = {
        myself: "1",
        result: '',
        username: '',
        page: 1,
        contest_id: this.contestID,
      };
      api.getSubmissionList(0, 20, params).then((res) => {
        let data = res.data.data;
        this.historyList = [...data.results];
      })
      this.historyDialogVisible = true
    },
    // 试运行
    trialRun() {
      this.error = ''
      this.trialRunDialogVisible = true
    },
    // 快速填入样例输入
    fillInTheSampleColumn(item) {
      this.inputCode = item.input
      this.outputCode = item.output
    },
    // 试运行提交
    getTrialRun() {
      if (this.code.trim() === "") {
        this.$error(this.$i18n.t("m.Code_can_not_be_empty"));
        return;
      } else if (!this.inputCode) {
        this.$error("请输入" + this.$i18n.t('m.Input_Instance'))
        return;
      } else if (!this.outputCode) {
        this.$error("请输入" + this.$i18n.t('m.Output_Instance'))
        return;
      } else {
        let params = {
          input: this.inputCode,
          output: this.outputCode,
          lang: this.language,
          src: this.code,
          problem_id: this.problem.id,
          contest_id: this.contestID,
        }
        api.getSelfTest(params).then((res) => {
          this.resultCode = res.data.data
          this.trialRunDialogVisible = false
          this.resultDialogVisible = true
        }).catch((res) => {
          this.error = res.data.error
        })
      }
    },
    getSubmission(params) {
      this.loading = true
      this.historyCodeDialogVisible = true
      api.getSubmission(params.row.id).then(res => {
        this.loading = false
        let data = res.data.data
        if (data.info && data.info.data && !this.isConcat) {
          if (data.info.data[0].score !== undefined) {
            this.isConcat = true
            const scoreColumn = {
              title: this.$i18n.t('m.Score'),
              align: 'center',
              key: 'score'
            }
            this.historyCodeColumns.push(scoreColumn)
          }
          if (this.$store.getters.isAdminRole) {
            this.isConcat = true
            const adminColumn = [
              {
                title: this.$i18n.t('m.Real_Time'),
                align: 'center',
                render: (h, params) => {
                  return h('span', utils.submissionTimeFormat(params.row.real_time))
                }
              },
              {
                title: this.$i18n.t('m.Signal'),
                align: 'center',
                key: 'signal'
              }
            ]
            this.historyCodeColumns = this.historyCodeColumns.concat(adminColumn)
          }
        }
        this.historyCode = data
      })
    },
    onCopyCode(text) {
      this.$copyText(text).then(e => {
        console.log('复制成功：', e);
      }, e => {
        console.log('复制失败：', e);
      })
    }
  },
  computed: {
    ...mapGetters([
      "problemSubmitDisabled",
      "contestRuleType",
      "OIContestRealTimePermission",
      "contestStatus",
    ]),
    contest() {
      return this.$store.state.contest.contest;
    },
    contestEnded() {
      return this.contestStatus === CONTEST_STATUS.ENDED;
    },
    submissionStatus() {
      return {
        text: JUDGE_STATUS[this.result.result]["name"],
        color: JUDGE_STATUS[this.result.result]["color"],
      };
    },
    submissionRoute() {
      if (this.contestID) {
        return {
          name: "contest-submission-list",
          query: { problemID: this.problemID },
        };
      } else {
        return {
          name: "submission-list",
          query: { problemID: this.problemID },
        };
      }
    },
    status() {
      return {
        type: JUDGE_STATUS[this.historyCode.result].type,
        statusName: JUDGE_STATUS[this.historyCode.result].name,
        color: JUDGE_STATUS[this.historyCode.result].color
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    // 防止切换组件后仍然不断请求
    clearInterval(this.refreshStatus);

    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: true });
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
      code: this.code,
      language: this.language,
      theme: this.theme,
    });
    next();
  },
  watch: {
    $route() {
      this.init();
    },
  },
};
</script>

<style lang="less" scoped>
.card-title {
  margin-left: 8px;
}

.flex-container {
  #problem-main {
    flex: auto;
    margin-right: 18px;
  }

  #right-column {
    flex: none;
    width: 220px;
  }
}

#problem-content {
  margin-top: -50px;

  .title {
    font-size: 20px;
    font-weight: 400;
    margin: 25px 0 8px 0;
    color: #3091f2;

    .copy {
      padding-left: 8px;
    }
  }

  p.content {
    margin-left: 25px;
    margin-right: 20px;
    font-size: 15px;
    white-space: normal;
  }

  .sample {
    align-items: stretch;

    &-input,
    &-output {
      width: 50%;
      flex: 1 1 auto;
      display: flex;
      flex-direction: column;
      margin-right: 5%;
    }

    pre {
      flex: 1 1 auto;
      align-self: stretch;
      border-style: solid;
      background: transparent;
    }
  }
}

#submit-code {
  .status {
    float: left;

    span {
      margin-right: 10px;
      margin-left: 10px;
    }
  }

  .captcha-container {
    display: inline-block;

    .captcha-code {
      width: auto;
      // margin-top: -20px;
      // margin-left: 20px;
    }
  }
}

#info {
  margin-bottom: 20px;
  margin-top: 20px;

  ul {
    list-style-type: none;

    li {
      border-bottom: 1px dotted #e9eaec;
      margin-bottom: 10px;

      p {
        display: inline-block;
      }

      p:first-child {
        width: 90px;
      }

      p:last-child {
        float: right;
      }
    }
  }
}

#pieChart {
  .echarts {
    height: 250px;
    width: 210px;
  }

  #detail {
    position: absolute;
    right: 10px;
    top: 10px;
  }
}

#pieChart-detail {
  margin-top: 20px;
  width: 500px;
  height: 480px;
}

.center_col {
  display: flex;
  justify-content: center;
  /*主轴上居中*/
  align-items: center;
  /*侧轴上居中*/
}

@media screen and (max-width: 1200px) {
  .codeEditorBox {
    height: calc(100vh - 236px);
  }

  .problemBox {
    overflow-y: auto;
    height: calc(100vh - 236px);
  }
}

@media screen and (min-width: 1200px) {
  .codeEditorBox {
    height: calc(100vh - 156px);
  }

  .problemBox {
    overflow-y: auto;
    height: calc(100vh - 156px);
  }
}

.challenge-btn {
  background-color: #00000030;
  font-size: 16px;
  padding: 8px;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}

.footer {
  position: fixed;
  display: flex;
  justify-content: flex-end;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 12px 20px 12px;
  margin: 0;
  z-index: 20;
  background: #d2ddf1;
  box-shadow: 2px -4px 8px #c7c7c7;

  .footerBtn {
    margin: 0 5px;
  }
}

.floatleft {
  float: left;
  margin-left: 10px;
}

.historyTable {
  overflow: hidden;
  overflow-y: auto;
}
</style>
<style lang="less">
.codeEditorBoxScreenfull {
  position: fixed !important;
  top: 0;
  left: 0;
  z-index: 1001;
  width: 100vw;
  height: 100vh;

  .CodeMirror-scroll {
    min-height: calc(100vh - 150px);
    max-height: calc(100vh - 150px);
  }
}

// .ivu-table-overflowX{
//   overflow-x: hidden;
// }
</style>