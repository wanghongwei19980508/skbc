<template>
  <div class="flex-container">
    <div id="problem-main">
      <splitpanes class="default-theme">
        <pane min-size="30">
          <Panel :padding="40" shadow class="description">
            <div slot="title">
              {{ objectiveProblem.title }}
              <el-tooltip placement="right" :content="$t('m.Submissions')">
                <el-button type="text" @click="goSubmission()">
                  <i class="el-icon-tickets" style="font-size: 20px"></i>
                </el-button>
              </el-tooltip>
            </div>
            <div id="problem-content" class="markdown-body" v-katex>
              <Row>
                <el-tooltip placement="bottom-start" :content="$t('m.ID')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="objectiveProblem._id"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
                <el-tooltip placement="bottom-start" :content="$t('m.Created')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="objectiveProblem.created_by.username"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
                <el-tooltip placement="bottom-start" :content="$t('m.Level')">
                  <Col :span="6" class="center_col">
                  <el-tag>
                    <span v-html="objectiveProblem.difficulty"></span>
                  </el-tag>
                  </Col>
                </el-tooltip>
              </Row>
              <p class="title">{{ $t("m.Description") }}</p>
              <div v-html="objectiveProblem.description"></div>
              <div v-if="objectiveProblem.hint">
                <p class="title">{{ $t("m.Hint") }}</p>
                <Card dis-hover>
                  <div class="content" v-html="objectiveProblem.hint"></div>
                </Card>
              </div>
            </div>
          </Panel>
        </pane>
        <pane min-size="40">
          <Panel :padding="40" shadow class="description">
            <div id="problem-content" class="markdown-body" v-katex>
              <div v-if="!objectiveProblem.is_multiple">
                <Row :gutter="16" v-if="objectiveProblem.type != 'Check'" class="problemBox">
                  <Col span="11" v-for="(option, index) in objectiveProblem.options" :key="'option' + index"
                    :label="index" class="problem">
                  <Card :padding="10">
                    <el-radio v-model="radioChoice" slot="title" :label="index">{{ optionChar[index] }}.</el-radio>
                    <p class="content" v-html="option" @click="radioChoice = index"></p>
                  </Card>
                  </Col>
                </Row>
                <Row :gutter="16" v-else>
                  <el-checkbox-group v-model="choice" class="problemBox">
                    <Col span="11" v-for="(option, index) in objectiveProblem.options" :key="'option' + index"
                      :label="index" class="problem">
                    <Card :padding="10">
                      <el-checkbox slot="title" :label="index">{{ optionChar[index] }}.</el-checkbox>
                      <p class="content" v-html="option" @click="checkOption(index)"></p>
                    </Card>
                    </Col>
                  </el-checkbox-group>
                </Row>
                <el-divider></el-divider>
              </div>
              <div v-else>
                <div v-for="(item, key) in objectiveProblem.multipleProblem" :key="key">
                  <p>{{ `题目${key + 1}(${item.scorce})分 : ` }}</p><span v-html="item.description"></span>
                  <Row :gutter="16" v-if="item.type != 'Check'" class="problemBox">
                    <Col span="11" v-for="(option, index) in item.options" :key="'option' + index" :label="index"
                      class="problem">
                    <Card :padding="10">
                      <el-radio v-model="choiceList[key]" slot="title" :label="index">{{ optionChar[index] }}.</el-radio>
                      <p class="content" v-html="option" @click="checkChoiceOption(key, index)"></p>
                    </Card>
                    </Col>
                  </Row>
                  <Row :gutter="16" v-else>
                    <el-checkbox-group v-model="choiceList[key]" class="problemBox">
                      <Col span="11" v-for="(option, index) in item.options" :key="'option' + index" :label="index"
                        class="problem">
                      <Card :padding="10">
                        <el-checkbox slot="title" :label="index">{{ optionChar[index] }}.</el-checkbox>
                        <p class="content" v-html="option" @click="checkChoiceOption(choiceList[key], index)"></p>
                      </Card>
                      </Col>
                    </el-checkbox-group>
                  </Row>
                  <el-divider></el-divider>
                </div>
              </div>
              <Row>
                <Col offset="20">
                <Button type="primary" size="large" icon="edit" :loading="submitting" @click="submitChoice">{{
                  $t("m.Submit") }}
                </Button>
                </Col>
              </Row>
              <div v-if="objectiveProblem.source">
                <p class="title">{{ $t("m.Source") }}</p>
                <p class="content">{{ objectiveProblem.source }}</p>
              </div>
            </div>
          </Panel>
        </pane>
      </splitpanes>
    </div>
    <div>
    </div>
  </div>
</template>
  
<script>
import { mapGetters, mapActions } from "vuex";
import { types } from "../../../../store";
import storage from "@/utils/storage";
import { FormMixin } from "@oj/components/mixins";
import {
  OBJECTIVE_PROBLEM_STATUS,
  CONTEST_STATUS,
  buildObjectiveProblemCodeKey,
} from "@/utils/constants";
import api from "@oj/api";
import { pie } from "./chartData";
import Save from "../../../admin/components/btn/Save.vue";
import VueAffixBox from "vue-affix-box";

import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'
const synth = window.speechSynthesis;
const msg = new SpeechSynthesisUtterance();
export default {
  name: "objectiveProblem",
  components: { VueAffixBox, Save, Splitpanes, Pane },
  mixins: [FormMixin],
  data() {
    return {
      statusVisible: false,
      captchaRequired: false,
      submissionExists: false,
      captchaCode: "",
      captchaSrc: "",
      choice: [],
      radioChoice: undefined,
      contestID: "",
      objectiveProblemID: "",
      submitting: false,
      submissionId: "",
      result: {
        result: 2,
      },
      optionChar: "",
      objectiveProblem: {
        title: "",
        description: "",
        hint: "",
        my_status: "",
        template: {},
        languages: [],
        created_by: {
          username: "",
        },
        tags: [],
      },
      pie: pie,
      choiceList: []
    };
  },
  beforeRouteEnter(to, from, next) {
    let problemCode = storage.get(
      buildObjectiveProblemCodeKey(
        to.params.objectiveProblemID,
        to.params.contestID
      )
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
      this.optionChar = "ABCDEFGHIJKLMN";
      this.$Loading.start();
      this.contestID = this.$route.params.contestID;
      this.objectiveProblemID = this.$route.params.objectiveProblemID;
      let func =
        this.$route.name === "objective-problem-details"
          ? "getObjectiveProblem"
          : "getContestObjectiveProblem";
      api[func](this.objectiveProblemID, this.contestID).then(
        (res) => {
          this.$Loading.finish();
          if (res.data.data.is_multiple) {
            res.data.data.multipleProblem = res.data.data.multiple_problem
            this.choiceList = res.data.data.multipleProblem.map((item) => {
              if (item.type !== 'Check') {
                return null
              } else {
                return []
              }
            })
          }
          let objectiveProblem = res.data.data;
          this.changeDomTitle({ title: objectiveProblem.title });
          api.objectiveSubmissionExists(objectiveProblem.id).then((res) => {
            this.submissionExists = res.data.data;
          });
          this.changePie(objectiveProblem);
          this.objectiveProblem = objectiveProblem;
          // this.handleSpeak(objectiveProblem.description)
        },
        () => {
          this.$Loading.error();
        }
      );
    },
    goSubmission() {
      if (this.contestID) {
        if (this.$route.name === "contest-objective-problem-details")
          this.$router.push({
            name: "contest-objective-submission-list",
            params: {
              contestID: this.contestID,
              objectiveProblemID: this.objectiveProblemID,
            },
          });
        else {
          this.$router.push({
            name: "assignment-objective-submission-list",
            params: {
              contestID: this.contestID,
              objectiveProblemID: this.objectiveProblemID,
            },
          });
        }
      } else {
        this.$router.push({
          name: "objective-submission-list",
          params: {
            objectiveProblemID: this.objectiveProblemID,
          },
        });
      }
    },
    checkOption(index) {
      if (this.choice.indexOf(index) != -1) {
        this.choice.splice(this.choice.indexOf(index), 1);
      } else {
        this.choice.push(index);
      }
    },
    checkChoiceOption(row, index) {
      if (row instanceof Array) {
        if (row.indexOf(index) != -1) {
          row.splice(row.indexOf(index), 1);
        } else {
          row.push(index);
        }
      } else {
        this.$set(this.choiceList, row, index)
      }
    },
    changePie(problemData) {
      // 只显示特定的一些状态
      let acNum = problemData.accepted_number;
      let data = [
        { name: "WA", value: problemData.submission_number - acNum },
        { name: "AC", value: acNum },
      ];
      this.pie.series[0].data = data;
    },
    handleRoute(route) {
      this.$router.push(route);
    },
    checkSubmissionStatus() {
      // 使用setTimeout避免一些问题
      if (this.refreshStatus) {
        // 如果之前的提交状态检查还没有停止,则停止,否则将会失去timeout的引用造成无限请求
        clearTimeout(this.refreshStatus);
      }
      const checkStatus = () => {
        let id = this.submissionId;
        api.getObjectiveSubmission(id).then(
          (res) => {
            this.result = res.data.data;
            // if (Object.keys(res.data.data.statistic_info).length !== 0) {
            this.submitting = false;
            clearTimeout(this.refreshStatus);
            this.init();
            // } else {
            //   this.refreshStatus = setTimeout(checkStatus, 2000);
            // }
          },
          (res) => {
            this.submitting = false;
            clearTimeout(this.refreshStatus);
          }
        );
      };
      this.refreshStatus = setTimeout(checkStatus, 2000);
    },
    submitChoice() {
      let data = {
        objective_problem_id: this.objectiveProblem.id,
        contest_id: this.contestID,
      };
      if (this.objectiveProblem.is_multiple) {
        let noChoose = 0
        this.choiceList.forEach((item) => {
          if (item == null || item.length == 0) {
            noChoose++
          }
        })
        if (noChoose) {
          this.$error(this.$i18n.t("m.Choice_can_not_be_empty"));
          return
        }
        data.choiceList = this.choiceList
      } else {
        if (this.objectiveProblem.type == "Radio" || this.objectiveProblem.type == "True_False") {
          if (this.radioChoice == undefined) {
            this.$error(this.$i18n.t("m.Choice_can_not_be_empty"));
            return;
          }
          this.choice = [this.radioChoice];
        } else if (this.choice.length == 0) {
          this.$error(this.$i18n.t("m.Choice_can_not_be_empty"));
          return;
        }
        data.choice = this.choice
      }
      this.submissionId = "";
      this.result = { result: 2 };
      this.submitting = true;
      if (this.captchaRequired) {
        data.captcha = this.captchaCode;
      }
      const submitFunc = (data, detailsVisible) => {
        this.statusVisible = true;
        api.submitChoice(data).then(
          (res) => {
            this.submissionId = res.data.data && res.data.data.submission_id;
            this.$router.push("/objective-status/" + this.submissionId);
            // 定时检查状态
            // this.submitting = false;
            // this.submissionExists = true;
            // if (!detailsVisible) {
            //   this.$Modal.success({
            //     title: this.$i18n.t("m.Success"),
            //     content: this.$i18n.t("m.Submit_code_successfully"),
            //   });
            //   return;
            // }
            // this.checkSubmissionStatus();
          }
          // (res) => {
          // this.getCaptchaSrc();
          // if (res.data.data.startsWith("Captcha is required")) {
          //   this.captchaRequired = true;
          // }
          // this.submitting = false;
          // this.statusVisible = false;
          // }
        );
      };
      submitFunc(data, true);
    },
    handleSpeak(text) {
      msg.text = text;
      msg.lang = 'zh-CN';
      msg.volume = '1';
      msg.rate = 1;
      msg.pitch = 1;
      synth.speak(msg);
    },
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
        text: OBJECTIVE_PROBLEM_STATUS[this.result.result]["name"],
        color: OBJECTIVE_PROBLEM_STATUS[this.result.result]["color"],
      };
    },
    submissionRoute() {
      if (this.contestID) {
        return {
          name: "contest-submission-list",
          query: { objectiveProblemID: this.objectiveProblemID },
        };
      } else {
        return {
          name: "objective-submission-list",
          query: { objectiveProblemID: this.objectiveProblemID },
        };
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    // 防止切换组件后仍然不断请求
    clearInterval(this.refreshStatus);
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: true });
    storage.set(
      buildObjectiveProblemCodeKey(
        this.objectiveProblem._id,
        from.params.contestID
      ),
      {
        choice: this.choice,
        theme: this.theme,
      }
    );
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
    justify-content: normal;

  }

  #right-column {
    flex: none;
    width: 220px;
  }
}

.description {
  height: calc(100vh - 100px);
  overflow: hidden;
  overflow-y: auto;
}

#problem-content {
  margin-top: -50px;

  .problemBox {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;

    .problem {
      margin: 10px 5px;
    }
  }

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

.fl-right {
  float: right;
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
</style>
  
  