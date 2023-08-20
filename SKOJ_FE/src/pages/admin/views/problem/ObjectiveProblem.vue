<template>
  <div class="problem">
    <Panel :title="title">
      <el-form ref="form" :model="objectiveProblem" :rules="rules" label-position="top" label-width="70px">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item prop="_id" :label="$t('m.Display_ID')" :required="this.routeName === 'create-contest-objective-problem' ||
              this.routeName === 'edit-contest-objective-problem'
              ">
              <el-input :placeholder="$t('m.Display_ID')" v-model="objectiveProblem._id"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item prop="title" :label="$t('m.Title')" required>
              <el-input :placeholder="$t('m.Title')" v-model="objectiveProblem.title"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item prop="description" :label="$t('m.ObjectiveDescription')" required>
              <Simditor v-model="objectiveProblem.description"></Simditor>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="2">
            <el-form-item :label="$t('m.Visible')">
              <el-switch v-model="objectiveProblem.visible" active-text="" inactive-text="">
              </el-switch>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Tag')" :error="error.tags" required>
              <span class="tags">
                <el-tag v-for="tag in objectiveProblem.tags" :closable="true" :close-transition="false" :key="tag"
                  type="success" @close="closeTag(tag)">{{ tag }}</el-tag>
              </span>
              <el-autocomplete v-if="inputVisible" size="mini" class="input-new-tag" popper-class="problem-tag-poper"
                v-model="tagInput" :trigger-on-focus="false" @keyup.enter.native="addTag" @select="addTag"
                :fetch-suggestions="querySearch">
              </el-autocomplete>
              <el-button class="button-new-tag" v-else size="small" @click="inputVisible = true">+ {{ $t("m.New_Tag")
              }}</el-button>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item :label="$t('m.Difficulty')">
              <el-select class="difficulty-select" size="small" :placeholder="$t('m.Difficulty')"
                v-model="objectiveProblem.difficulty">
                <el-option :label="$t('m.Low')" value="Low"></el-option>
                <el-option :label="$t('m.Mid')" value="Mid"></el-option>
                <el-option :label="$t('m.High')" value="High"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item :label="$t('m.Source')">
              <el-input :placeholder="$t('m.Source')" v-model="objectiveProblem.source"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2">
            <el-form-item :label="$t('m.ProblemSet')">
              <el-switch v-model="objectiveProblem.is_multiple" active-text="" inactive-text="">
              </el-switch>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="!objectiveProblem.is_multiple">
          <el-col :span="4">
            <el-form-item :label="$t('m.ObjectiveProblemType')">
              <el-select class="type-select" size="small" :placeholder="$t('m.ObjectiveProblemType')"
                v-model="objectiveProblem.type" @change="typeChange">
                <el-option :label="$t('m.Radio')" value="Radio"></el-option>
                <el-option :label="$t('m.Check')" value="Check"></el-option>
                <el-option :label="$t('m.True_False')" value="True_False"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="20">
            <el-table :data="objectiveProblem.answer" style="width: 100%" :border="true">
              <el-table-column type="index" :label="$t('m.Option')" width="60">
              </el-table-column>
              <el-table-column label="选项" width="240">
                <template #default="scope">
                  <el-switch v-model="scope.row.isAns" size="" active-color="#13ce66" slot="header"
                    inactive-color="#ff4949" :active-text="$t('m.TrueOption')" :inactive-text="$t('m.FalseOption')">
                  </el-switch>
                </template>
              </el-table-column>
              <el-table-column label="内容">
                <template #default="scope">
                  <div v-html="scope.row.option" class="tableOption"></div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="280">
                <template #default="scope">
                  <el-button size="mini" @click.prevent="editOption(scope.row)">
                    {{ $t('m.Edit_Option') }}
                  </el-button>
                  <el-button v-if="objectiveProblem.type != 'True_False'" size="mini"
                    @click="addOption(objectiveProblem)">
                    {{ $t('m.Add_Option') }}
                  </el-button>
                  <el-button v-if="objectiveProblem.type != 'True_False'" size="mini"
                    @click="deleteOption(objectiveProblem, scope.$index)">
                    {{ $t('m.Delete') }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
        <el-row v-else>
          <div v-for="(item, index) in objectiveProblem.multipleProblem" :key="index"
            style="border: 1px solid #c5c3a9; padding: 10px 20px;margin: 10px 0;">
            <el-col :span="3">
              <el-form-item :label="$t('m.ObjectiveProblemType')">
                <el-select class="type-select" size="small" :placeholder="$t('m.ObjectiveProblemType')"
                  v-model="item.type" @change="((val) => { typeChange(val, item) })">
                  <el-option :label="$t('m.Radio')" value="Radio"></el-option>
                  <el-option :label="$t('m.Check')" value="Check"></el-option>
                  <el-option :label="$t('m.True_False')" value="True_False"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item :label="$t('m.Scorce')">
                <el-input-number size="small" :controls="false" v-model="item.scorce"></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="18">
              <el-form-item :label="$t('m.Question_Title')">
                <!-- <el-input type="textarea" :placeholder="$t('m.Question_Title')" v-model="item.description"
                  :autosize="{ minRows: 3, maxRows: 3 }"></el-input> -->
                <div style="height: 180px;overflow: auto;">
                  <Simditor v-model="item.description"></Simditor>
                </div>
              </el-form-item>
            </el-col>
            <el-col :span="3">
              <el-form-item :label="$t('m.Delete')" style="padding: 0 20px;">
                <el-button type="warning" icon="el-icon-delete" size="mini" @click="deleteMultipleProblem(index)">
                  {{ $t('m.Delete') }}
                </el-button>
              </el-form-item>
            </el-col>
            <el-table :data="item.answer" style="width: 100%" :border="true">
              <el-table-column type="index" :label="$t('m.Option')" width="60">
              </el-table-column>
              <el-table-column label="选项" width="240">
                <template #default="scope">
                  <el-switch v-model="scope.row.isAns" size="" active-color="#13ce66" slot="header"
                    inactive-color="#ff4949" :active-text="$t('m.TrueOption')" :inactive-text="$t('m.FalseOption')">
                  </el-switch>
                </template>
              </el-table-column>
              <el-table-column label="内容">
                <template #default="scope">
                  <div v-html="scope.row.option" class="tableOption"></div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="280">
                <template #default="scope">
                  <el-button size="mini" @click.prevent="editOption(scope.row)">
                    {{ $t('m.Edit_Option') }}
                  </el-button>
                  <el-button v-if="item.type != 'True_False'" size="mini" @click="addOption(item)">
                    {{ $t('m.Add_Option') }}
                  </el-button>
                  <el-button v-if="item.type != 'True_False'" size="mini" @click="deleteOption(item, scope.$index)">
                    {{ $t('m.Delete') }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <div class="add-option-btn">
            <button type="button" class="add-option" @click="addMultipleProblem()">
              <i class="el-icon-plus"></i>{{ $t("m.Add_ProblemSet") }}
            </button>
          </div>
        </el-row>
        <el-form-item style="margin-top: 20px" :label="$t('m.Hint')">
          <Simditor v-model="objectiveProblem.hint" placeholder=""></Simditor>
        </el-form-item>

        <!-- <el-button>预览</el-button> -->
        <save @click.native="submit()">Save</save>
      </el-form>
    </Panel>
    <el-dialog :visible="editDialogVisible" :title="$t('m.Edit_Option')" :fullscreen="editFullscreen"
      @close="editDialogVisible = false">
      <div slot="title">
        <h2>{{ $t('m.Edit_Option') }}</h2>
        <el-button style="position: absolute;right: 50px;top: 18px;" size="mini" icon="el-icon-full-screen"
          @click="editFullscreen = !editFullscreen"></el-button>
      </div>
      <div>
        <Simditor v-model="OptionContent.option" :placeholder="$t('m.OptionContent')"></Simditor>
      </div>
    </el-dialog>
  </div>
</template>
  
<script>
import Simditor from "../../components/Simditor";
import Accordion from "../../components/Accordion";
import CodeMirror from "../../components/CodeMirror";
import api from "../../api";

export default {
  name: "ObjectiveProblem",
  components: {
    Simditor,
    Accordion,
    CodeMirror,
  },
  data() {
    return {
      editDialogVisible: false,
      editFullscreen: false,
      OptionContent: {},
      rules: {
        _id: {
          required: true,
          message: "Display ID is required",
          trigger: "blur",
        },
        title: {
          required: true,
          message: "Title is required",
          trigger: "blur",
        },
      },
      loadingCompile: false,
      mode: "",
      contest: {},
      lastType: "Radio",
      ops: {
        Radio: [
          { option: "", isAns: true },
          { option: "", isAns: false },
          { option: "", isAns: false },
          { option: "", isAns: false },
        ],
        Check: [
          { option: "", isAns: true },
          { option: "", isAns: false },
          { option: "", isAns: false },
          { option: "", isAns: false },
        ],
        True_False: [
          { option: "<p>" + this.$i18n.t("m.True") + "</p>", isAns: true },
          { option: "<p>" + this.$i18n.t("m.False") + "</p>", isAns: false },
        ],
      },
      objectiveProblem: {},
      reObjectiveProblem: {},
      tagInput: "",
      inputVisible: false,
      title: "",
      disableRuleType: false,
      routeName: "",
      error: {
        tags: "",
      },
    };
  },
  mounted() {
    this.routeName = this.$route.name;
    if (
      this.routeName === "edit-objective-problem" ||
      this.routeName === "edit-contest-objective-problem"
    ) {
      this.mode = "edit";
    } else {
      this.mode = "add";
    }
    this.objectiveProblem = this.reObjectiveProblem = {
      _id: "",
      title: "",
      description: "",
      difficulty: "Low",
      type: "Radio",
      visible: true,
      is_multiple: false,
      tags: [],
      options: [],
      hint: "<p>" + this.$i18n.t("m.Nothing") + "</p>",
      source: "",
      answer: [
        { option: "", isAns: true },
        { option: "", isAns: false },
        { option: "", isAns: false },
        { option: "", isAns: false },
      ],
      multipleProblem: [
        { type: "Radio", description: '', answer: [{ option: "", isAns: true }, { option: "", isAns: false }, { option: "", isAns: false }, { option: "", isAns: false }], scorce: 1 },
        { type: "Radio", description: '', answer: [{ option: "", isAns: true }, { option: "", isAns: false }, { option: "", isAns: false }, { option: "", isAns: false }], scorce: 1 },
      ]
    };
    let contestID = this.$route.params.contestId;
    if (contestID) {
      this.objectiveProblem.contest_id = this.reObjectiveProblem.contest_id =
        contestID;
      this.disableRuleType = true;
      api.getContest(contestID).then((res) => {
        this.contest = res.data.data;
        console.log(this.contest);
      });
    }
    // get problem after getting languages list to avoid find undefined value in `watch problem.languages`
    if (this.mode === "edit") {
      this.title = this.$i18n.t("m.Edit_Problem");
      let funcName = {
        "edit-objective-problem": "getObjectiveProblem",
        "edit-contest-objective-problem": "getContestObjectiveProblem",
      }[this.routeName];
      api[funcName](this.$route.params.objectiveProblemId).then((problemRes) => {
        let data = problemRes.data.data;
        if (data.is_multiple) {
          data.multipleProblem = data.multiple_problem
        } else {
          data.is_multiple = false
          data.multipleProblem = [
            {
              type: "Radio", description: '', answer: [{ option: "", isAns: true }, { option: "", isAns: false }, { option: "", isAns: false }, { option: "", isAns: false },], scorce: 1
            },
          ]
        }
        this.objectiveProblem = data;
        this.ops[this.objectiveProblem.type] = this.objectiveProblem.answer;
      });
    } else {
      this.title = this.$i18n.t("m.Add_Problem");
    }
  },
  watch: {
    $route() {
      this.$refs.form.resetFields();
      this.objectiveProblem = this.reObjectiveProblem;
      this.ops = this.objectiveProblem.answer;
    },
  },
  methods: {
    typeChange(event, item) {
      if (item) {
        item.answer = JSON.parse(JSON.stringify(this.ops[event]))
      } else {
        this.ops[this.lastType] = this.objectiveProblem.answer;
        this.objectiveProblem.answer = this.ops[this.objectiveProblem.type];
        this.lastType = this.objectiveProblem.type;
      }
    },
    querySearch(queryString, cb) {
      api.getObjectiveProblemTagList({ keyword: queryString }).then((res) => {
        let tagList = [];
        for (let tag of res.data.data) {
          tagList.push({ value: tag.name });
        }
        cb(tagList);
      }).catch(() => { });
    },
    addTag() {
      let inputValue = this.tagInput;
      if (inputValue) {
        this.objectiveProblem.tags.push(inputValue);
      }
      this.inputVisible = false;
      this.tagInput = "";
    },
    closeTag(tag) {
      this.objectiveProblem.tags.splice(this.objectiveProblem.tags.indexOf(tag), 1);
    },
    addOption(row) {
      row.answer.push({ option: "", isAns: false })
    },
    deleteOption(item, index) {
      if (item.answer.length > 1) {
        item.answer.splice(index, 1);
      }
    },
    addMultipleProblem() {
      this.objectiveProblem.multipleProblem.push({
        type: "Radio", description: '', answer: [{ option: "", isAns: true }, { option: "", isAns: false }, { option: "", isAns: false }, { option: "", isAns: false },], scorce: 1
      })
    },
    deleteMultipleProblem(index) {
      if (this.objectiveProblem.multipleProblem.length > 1) {
        this.objectiveProblem.multipleProblem.splice(index, 1)
      }
    },
    editOption(row) {
      this.OptionContent = row
      this.editDialogVisible = true
    },
    submit() {
      if (!this.objectiveProblem.tags.length) {
        this.$error(this.$i18n.t('m.Please_Add_At_Least_One_Tag'));
        return;
      }
      let e, multiple_answer = [], multiple_problem = []
      if (this.objectiveProblem.is_multiple) {
        try {
          this.objectiveProblem.multipleProblem.forEach((item, index) => {
            e = this.depthCheck(item.answer, item.type)
            if (!item.scorce) {
              e.haveTrue = false
              this.$error(this.$i18n.t('m.Please_Enter_The_Score_Value'))
            } else if (!item.description) {
              e.haveTrue = false
              this.$error(this.$i18n.t('m.Please_Enter_The_Question_Content'))
            }
            if (!e.haveTrue) {
              throw new Error(e.haveTrue)
            }
            item.options = e.options
            multiple_answer.push(item.answer)
            multiple_problem.push(item)
          })
        } catch (e) { }
      } else {
        e = this.depthCheck(this.objectiveProblem.answer, this.objectiveProblem.type)
        this.objectiveProblem.options = e.options
      }
      if (!e.haveTrue) return
      this.objectiveProblem.multiple_answer = multiple_answer
      this.objectiveProblem.multiple_problem = multiple_problem
      let funcName = {
        "create-objective-problem": "createObjectiveProblem",
        "edit-objective-problem": "editObjectiveProblem",
        "create-contest-objective-problem": "createContestObjectiveProblem",
        "edit-contest-objective-problem": "editContestObjectiveProblem",
      }[this.routeName];
      // edit contest problem 时, contest_id会被后来的请求覆盖掉
      if (funcName === "editContestObjectiveProblem") {
        this.objectiveProblem.contest_id = this.contest.id;
      }
      api[funcName](this.objectiveProblem).then((res) => {
        if (
          this.routeName === "create-contest-objective-problem" ||
          this.routeName === "edit-contest-objective-problem"
        ) {
          this.$router.push({
            name: "contest-public-topic-list",
            params: { contestId: this.$route.params.contestId },
          });
        } else {
          this.$router.push({ name: "objective-problem-list" });
        }
      }).catch(() => { });
    },
    depthCheck(row, type) {
      let haveTrue = false
      let correctChoice = 0;
      let options = []
      for (let option of row) {
        if (options.indexOf(option.option) != -1) {
          this.$error(this.$i18n.t('m.Duplicate_Options_Are_Not_Allowed'))
          return { haveTrue, options }
        }
        options.push(option.option);
        if (!option.option) {
          this.$error(this.$i18n.t('m.Option_Content_Is_Required'))
          return { haveTrue, options }
        }
        if (option.isAns) {
          correctChoice++
        }
      }
      if (correctChoice !== 1 && type !== 'Check') {
        correctChoice > 1 ? this.$error(this.$i18n.t('m.You_Can_Only_Have_One_Correct_Choice')) : this.$error(this.$i18n.t('m.Please_Set_A_Correct_Option'))
      } else if (type === 'Check' && correctChoice === 0) {
        this.$error(this.$i18n.t('m.Please_Set_A_Correct_Option'))
      } else {
        haveTrue = true
      }
      return { haveTrue, options }
    }
  },
};
</script>
  
<style lang="less" scoped>
.problem {

  .difficulty-select,
  .type-select {
    width: 120px;
  }

  .spj-radio {
    margin-left: 10px;

    &:last-child {
      margin-right: 20px;
    }
  }

  .input-new-tag {
    width: 78px;
  }

  .button-new-tag {
    height: 24px;
    line-height: 22px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .tags {
    .el-tag {
      margin-right: 10px;
    }
  }

  .accordion {
    margin-bottom: 10px;
  }

  .add-option {
    width: 100%;
    background-color: #fff;
    border: 1px dashed #aaa;
    outline: none;
    cursor: pointer;
    color: #666;
    height: 35px;
    font-size: 14px;

    &:hover {
      background-color: #f9fafc;
    }

    i {
      margin-right: 10px;
    }
  }

  .tableOption {
    max-height: 100px;
    overflow: auto;
  }

  .add-option-btn {
    margin: 20px 0 10px;
  }
}
</style>
  
<style>
.problem-tag-poper {
  width: 200px !important;
}

.dialog-compile-error {
  width: auto;
  max-width: 80%;
  overflow-x: scroll;
}
</style>
  
  