<template>
  <Row type="flex" justify="space-around">
    <Col :span="20" id="status">
    <Alert :type="status.type" showIcon>
      <span class="title">{{ $t("m." + status.statusName.replace(/ /g, "_")) }}</span>
      <div slot="desc" class="content">
        <template>
          <span>{{ $t("m.Author") }}: {{ objectiveSubmission.username }}</span>
        </template>
      </div>
    </Alert>
    </Col>
    <Col :span="20">
    <Panel :padding="40" shadow>
      <div slot="title">{{ objectiveProblem.title }}</div>
      <div id="problem-content" class="markdown-body" v-katex>
        <p class="title">{{ $t("m.Description") }}</p>
        <p class="content" v-html="objectiveProblem.description"></p>
        <el-divider></el-divider>
        <div v-if="!objectiveProblem.is_multiple">
          <Row :gutter="16" v-if="objectiveProblem.type != 'Check'">
            <Col span="12" v-for="(item, index) in objectiveProblem.answer" :key="'item' + index" :label="index">
            <Card :padding="10" v-if="choice == index">
              <Alert :type="status.type" showIcon>
                <span class="title">{{ optionChar[index] }}.</span>
                <div slot="desc" class="content">
                  <template>
                    <span>
                      <p class="content" v-html="item.option"></p>
                    </span>
                  </template>
                </div>
              </Alert>
            </Card>
            <Card :padding="10" v-else>
              <Alert :type="'info'" :showIcon="false">
                <span class="title">{{ optionChar[index] }}.</span>
                <div slot="desc" class="content">
                  <template>
                    <span>
                      <p class="content" v-html="item.option"></p>
                    </span>
                  </template>
                </div>
              </Alert>
            </Card>
            </Col>
          </Row>
          <Row :gutter="16" v-else>
            <el-checkbox-group v-model="choice">
              <Col span="12" v-for="(item, index) in objectiveProblem.answer" :key="'item' + index" :label="index">
              <Card :padding="10" v-if="choice.indexOf(index) != -1">
                <Alert :type="!item.isAns ? status.type : 'success'" showIcon>
                  <span class="title">{{ optionChar[index] }}</span>
                  <div slot="desc" class="content">
                    <template>
                      <span>
                        <p class="content" v-html="item.option"></p>
                      </span>
                    </template>
                  </div>
                </Alert>
              </Card>
              <Card :padding="10" v-else>
                <Alert :type="item.isAns ? 'warning' : 'info'" :showIcon="item.isAns ? true : false">
                  <span class="title">{{ optionChar[index] }}.</span>
                  <div slot="desc" class="content">
                    <template>
                      <span>
                        <p class="content" v-html="item.option"></p>
                      </span>
                    </template>
                  </div>
                </Alert>
              </Card>
              </Col>
            </el-checkbox-group>
          </Row>
        </div>

        <div v-else>
          <div v-for="(answer, key) in objectiveProblem.multiple_problem" :key="'answer' + key">
            <p class="content" v-html="answer.description"></p>
            <Row :gutter="16" v-if="answer.type != 'Check'">
              <Col span="12" v-for="(item, index) in answer.answer" :key="'item' + index" :label="index">
              <Card :padding="10" v-if="multiple_choice[key] == index">
                <Alert :type="'error'" showIcon>
                  <span class="title">{{ optionChar[index] }}.</span>
                  <div slot="desc" class="content">
                    <template>
                      <span>
                        <p class="content" v-html="item.option"></p>
                      </span>
                    </template>
                  </div>
                </Alert>
              </Card>
              <Card :padding="10" v-else>
                <Alert :type="'info'" :showIcon="false">
                  <span class="title">{{ optionChar[index] }}.</span>
                  <div slot="desc" class="content">
                    <template>
                      <span>
                        <p class="content" v-html="item.option"></p>
                      </span>
                    </template>
                  </div>
                </Alert>
              </Card>
              </Col>
            </Row>
            <Row :gutter="16" v-else>
              <el-checkbox-group v-model="multiple_choice[key]">
                <Col span="12" v-for="(item, index) in answer.answer" :key="'item' + index" :label="index">
                <Card :padding="10" v-if="multiple_choice[key].indexOf(index) != -1">
                  <Alert :type="!item.isAns ? 'error' : 'success'" showIcon>
                    <span class="title">{{ optionChar[index] }}.</span>
                    <div slot="desc" class="content">
                      <template>
                        <span>
                          <p class="content" v-html="item.option"></p>
                        </span>
                      </template>
                    </div>
                  </Alert>
                </Card>
                <Card :padding="10" v-else>
                  <Alert :type="item.isAns ? 'warning' : 'info'" :showIcon="item.isAns ? true : false">
                    <span class="title">{{ optionChar[index] }}.</span>
                    <div slot="desc" class="content">
                      <template>
                        <span>
                          <p class="content" v-html="item.option"></p>
                        </span>
                      </template>
                    </div>
                  </Alert>
                </Card>
                </Col>
              </el-checkbox-group>
            </Row>
            <el-divider v-if="key != objectiveProblem.multiple_problem.length"></el-divider>
          </div>
        </div>
      </div>
    </Panel>
    </Col>
    <Col v-if="objectiveSubmission.can_unshare" :span="20">
    <div id="share-btn">
      <Button v-if="objectiveSubmission.shared" type="warning" size="large" @click="shareObjectiveSubmission(false)">
        {{ $t("m.UnShare") }}
      </Button>
      <Button v-else type="primary" size="large" @click="shareObjectiveSubmission(true)">
        {{ $t("m.Share") }}
      </Button>
    </div>
    </Col>
  </Row>
</template>
  
<script>
import api from "@oj/api";
import { OBJECTIVE_PROBLEM_STATUS } from "@/utils/constants";

export default {
  name: "objectiveSubmissionDetails",
  data() {
    return {
      columns: [
        {
          title: this.$i18n.t("m.ID"),
          align: "center",
          type: "index",
        },
        {
          title: this.$i18n.t("m.Status"),
          align: "center",
          render: (h, params) => {
            return h(
              "Tag",
              { props: { color: OBJECTIVE_PROBLEM_STATUS[params.row.result].color, }, },
              this.$i18n.t("m." + OBJECTIVE_PROBLEM_STATUS[params.row.result].name.replace(/ /g, "_"))
            );
          },
        },
      ],
      objectiveSubmission: {
        result: "0",
      },
      optionChar: "",
      radioChoice: "",
      choice: [],
      multiple_choice: [],
      objectiveProblem: {},
      loading: false,
    };
  },
  mounted() {
    this.getObjectiveSubmission();
  },
  methods: {
    getObjectiveSubmission() {
      this.optionChar = "ABCDEFGHIJKLMN";
      this.loading = true;
      api.getObjectiveSubmission(this.$route.params.id).then((res) => {
        let data = res.data.data;
        this.objectiveSubmission = data;
        api.getObjectiveProblemById(this.objectiveSubmission.objective_problem).then((res) => {
          this.loading = false;
          let data = res.data.data;
          this.objectiveProblem = data;
          if (!this.objectiveProblem.is_multiple) {
            if (this.objectiveProblem.type != "Check")
              this.choice = this.objectiveSubmission.choice[0];
            else {
              this.choice = this.objectiveSubmission.choice;
            }
          } else {
            this.multiple_choice = this.objectiveSubmission.multiple_choice
          }
        }, () => {
          this.loading = false;
        });
      }, () => {
        this.loading = false;
      });
    },
    shareObjectiveSubmission(shared) {
      let data = { id: this.objectiveSubmission.id, shared: shared };
      api.updateObjectiveSubmission(data).then((res) => {
        this.getObjectiveSubmission();
        this.$success(this.$i18n.t("m.Succeeded"));
      }, () => { });
    },
  },
  computed: {
    status() {
      return {
        type: OBJECTIVE_PROBLEM_STATUS[this.objectiveSubmission.result].type,
        statusName: OBJECTIVE_PROBLEM_STATUS[this.objectiveSubmission.result].name,
        color: OBJECTIVE_PROBLEM_STATUS[this.objectiveSubmission.result].color,
      };
    },
    isCE() {
      return this.objectiveSubmission.result === -2;
    },
    isAdminRole() {
      return this.$store.getters.isAdminRole;
    },
  },
};
</script>
  
<style scoped lang="less">
#status {
  .title {
    font-size: 20px;
  }

  .content {
    margin-top: 10px;
    font-size: 14px;

    span {
      margin-right: 10px;
    }

    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
      word-break: break-all;
    }
  }
}

.admin-info {
  margin: 5px 0;

  &-content {
    font-size: 16px;
    padding: 10px;
  }
}

#share-btn {
  float: right;
  margin-top: 5px;
  margin-right: 10px;
}

pre {
  border: none;
  background: none;
}

/deep/ .ivu-alert-info {
  border: 1px solid #cdcbcb;
  background-color: #ffffff;
}
</style>
  