<template>
  <div style="margin: 0px 0px 15px 0px">
    <Row type="flex" justify="space-between" class="header">
      <Col :span="16">
        <div :style="{ '--fontPreSize': fontPreSize }">
          <span>{{ $t("m.Language") }}:</span>
          <Select :value="language" @on-change="onLangChange" class="adjust">
            <Option v-for="item in languages" :key="item" :value="item"
              >{{ item }}
            </Option>
          </Select>

          <Tooltip
            :content="this.$i18n.t('m.Reset_to_default_code_definition')"
            placement="bottom"
            style="margin-left: 10px"
          >
            <Button icon="refresh" @click="onResetClick"></Button>
          </Tooltip>

          <Tooltip
            :content="this.$i18n.t('m.Upload_file')"
            placement="bottom"
            style="margin-left: 10px"
          >
            <Button icon="upload" @click="onUploadFile"></Button>
          </Tooltip>
          <Tooltip v-if="screenfull"
          :content="screenfullBtn ? this.$i18n.t('m.Cancel_Full_Screen') : this.$i18n.t('m.Screen_Full')"
          placement="bottom"
          style="margin-left: 10px"
          >
            <Button icon="qr-scanner" @click="justLookAtTheProblem"></Button>
          </Tooltip>

          <input
            type="file"
            id="file-uploader"
            style="display: none"
            @change="onUploadFileDone"
          />
        </div>
      </Col>
      <Col :span="8">
        <div class="fl-right">
          <span>{{ $t("m.Theme") }}:</span>
          <Select :value="theme" @on-change="onThemeChange" class="adjust">
            <Option v-for="item in themes" :key="item.label" :value="item.value"
              >{{ item.label }}
            </Option>
          </Select>
        </div>
      </Col>
    </Row>
    <codemirror
      :value="value"
      :options="options"
      @change="onEditorCodeChange"
      ref="myEditor"
    >
    </codemirror>
  </div>
</template>
<script>
import utils from "@/utils/utils";
import { codemirror } from "vue-codemirror-lite";
import "../../../../static/css/myself_codemirror.css";
// theme
import "codemirror/theme/monokai.css";
import "codemirror/theme/solarized.css";
import "codemirror/theme/material.css";
import "codemirror/theme/night.css";
import "codemirror/theme/idea.css";
import "codemirror/theme/icecoder.css";

// mode
import "codemirror/mode/clike/clike.js";
import "codemirror/mode/python/python.js";
import "codemirror/mode/go/go.js";
import "codemirror/mode/javascript/javascript.js";

// active-line.js
import "codemirror/addon/selection/active-line.js";
import "codemirror/addon/edit/matchbrackets.js";
import "codemirror/addon/edit/closebrackets.js";

// foldGutter
import "codemirror/addon/fold/foldgutter.css";
import "codemirror/addon/fold/foldgutter.js";
import "codemirror/addon/fold/brace-fold.js";
import "codemirror/addon/fold/indent-fold.js";

//代码补全提示
import "codemirror/addon/hint/anyword-hint.js";
import "codemirror/addon/hint/css-hint.js";
import "codemirror/addon/hint/html-hint.js";
import "codemirror/addon/hint/javascript-hint.js";
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/show-hint.js";
import "codemirror/addon/hint/sql-hint.js";
import "codemirror/addon/hint/xml-hint.js";

import "codemirror/addon/edit/closebrackets.js";

export default {
  name: "CodeMirror",
  components: {
    codemirror,
  },
  props: {
    value: {
      type: String,
      default: "",
    },
    languages: {
      type: Array,
      default: () => {
        return ["C++", "C", "Java", "Python2"];
      },
    },
    language: {
      type: String,
      default: "C++",
    },
    theme: {
      type: String,
      default: "solarized",
    },
    fontPreSize: {
      type: String,
      default: "200%",
    },
    // 是否显示全屏按钮
    screenfull: {
      type: Boolean,
      default: false,
    },
    // 是否全屏
    screenfullBtn: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      options: {
        // codemirror options
        tabSize: 2,
        mode: "text/x-csrc",
        theme: "solarized",
        lineNumbers: true,
        line: true,
        // 代码折叠
        foldGutter: true,
        autoCloseBrackets: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        // 选中文本自动高亮，及高亮方式
        styleSelectedText: true,
        lineWrapping: true,
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true },
        extraKeys: { Ctrl: "autocomplete" },
        autoCloseBrackets: true, // 自动闭合符号
        matchBrackets: true, // 在光标点击紧挨{、]括号左、右侧时，自动突出显示匹配的括号 }、]
      },
      mode: {
        "C++": "text/x-csrc",
      },
      themes: [
        { label: this.$i18n.t("m.Solarized_Light"), value: "solarized" },
        { label: this.$i18n.t("m.Monokai"), value: "monokai" },
        { label: this.$i18n.t("m.Material"), value: "material" },
        { label: this.$i18n.t("m.Night"), value: "night" },
        { label: this.$i18n.t("m.Idea"), value: "idea" },
        { label: this.$i18n.t("m.Icecoder"), value: "icecoder" },
      ],
    };
  },
  mounted() {
    utils.getLanguages().then((languages) => {
      let mode = {};
      languages.forEach((lang) => {
        mode[lang.name] = lang.content_type;
      });
      this.mode = mode;
      this.editor.setOption("mode", this.mode[this.language]);
    });
    this.editor.focus();
  },
  methods: {
    onEditorCodeChange(newCode) {
      this.$emit("update:value", newCode);
    },
    onLangChange(newVal) {
      this.editor.setOption("mode", this.mode[newVal]);
      this.$emit("changeLang", newVal);
    },
    onThemeChange(newTheme) {
      this.editor.setOption("theme", newTheme);
      this.$emit("changeTheme", newTheme);
    },
    onResetClick() {
      this.$emit("resetCode");
    },
    onUploadFile() {
      document.getElementById("file-uploader").click();
    },
    onUploadFileDone() {
      let f = document.getElementById("file-uploader").files[0];
      let fileReader = new window.FileReader();
      let self = this;
      fileReader.onload = function (e) {
        var text = e.target.result;
        self.editor.setValue(text);
        document.getElementById("file-uploader").value = "";
      };
      fileReader.readAsText(f, "UTF-8");
    },
    // 切换全屏的回调函数
    justLookAtTheProblem() {
      this.$emit("changescreenfull");
    },
  },
  computed: {
    editor() {
      // get current editor object
      return this.$refs.myEditor.editor;
    },
  },
  watch: {
    theme(newVal, oldVal) {
      this.editor.setOption("theme", newVal);
    },
  },
};
</script>

<style lang="less" scoped>
.header {
  margin: 5px 5px 15px 5px;
  .adjust {
    width: 100px;
    margin-left: 5px;
  }
  .fl-right {
    float: right;
  }
}
</style>
