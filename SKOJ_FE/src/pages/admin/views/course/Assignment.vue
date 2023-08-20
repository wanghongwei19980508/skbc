<template>
  <div class="view">
    <Panel>
      <div slot="title">
        <el-page-header @back="goBack" :content="$t('m.' + title)" style="margin-top: 5px">
        </el-page-header>
      </div>
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item :label="$t('m.Assignment_Title')" required>
              <el-input v-model="assignment.title" :placeholder="$t('m.Assignment_Title')"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.Assignment_Description')" required>
              <Simditor v-model="assignment.description"></Simditor>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Assignment_Start_Time')" required>
              <el-date-picker v-model="assignment.start_time" type="datetime"
                :placeholder="$t('m.Assignment_Start_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Assignment_End_Time')" required>
              <el-date-picker v-model="assignment.end_time" type="datetime" :placeholder="$t('m.Assignment_End_Time')">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Assignment_Password')">
              <el-input v-model="assignment.password" :placeholder="$t('m.Assignment_Password')"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Assignment_Rule_Type')">
              <el-radio class="radio" v-model="assignment.rule_type" label="ACM"
                :disabled="disableRuleType">ACM</el-radio>
              <el-radio class="radio" v-model="assignment.rule_type" label="OI" :disabled="disableRuleType">OI</el-radio>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Real_Time_Rank')">
              <el-switch v-model="assignment.real_time_rank" active-color="#13ce66" inactive-color="#ff4949">
              </el-switch>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Assignment_Status')">
              <el-switch v-model="assignment.visible" active-text="" inactive-text="">
              </el-switch>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <save @click.native="saveAssignment"></save>
    </Panel>
  </div>
</template>
  
<script>
import api from "../../api.js";
import Simditor from "../../components/Simditor.vue";

export default {
  name: "CreateAssignment",
  components: {
    Simditor,
  },
  data() {
    return {
      title: "Create_Assignment",
      disableRuleType: false,
      assignment: {
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        rule_type: "ACM",
        password: "",
        real_time_rank: true,
        visible: true,
        lesson_id: "",
        allowed_ip_ranges: [
          {
            value: "",
          },
        ],
      },
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    saveAssignment() {
      let funcName =
        this.$route.name === "edit-assignment"
          ? "editAssignment"
          : "createAssignment";
      let data = Object.assign({}, this.assignment);
      let ranges = [];
      for (let v of data.allowed_ip_ranges) {
        if (v.value !== "") {
          ranges.push(v.value);
        }
      }
      data.allowed_ip_ranges = ranges;
      api[funcName](data)
        .then((res) => {
          this.$router.push({
            name: "lesson-assignment-list",
            query: { refresh: "true" },
          });
        })
        .catch(() => { });
    },
    addIPRange() {
      this.assignment.allowed_ip_ranges.push({ value: "" });
    },
    removeIPRange(range) {
      let index = this.assignment.allowed_ip_ranges.indexOf(range);
      if (index !== -1) {
        this.assignment.allowed_ip_ranges.splice(index, 1);
      }
    },
  },
  mounted() {
    this.assignment.lesson_id = this.$route.params.lessonId;
    if (this.$route.name === "edit-assignment") {
      this.title = "Edit Assignment";
      this.disableRuleType = true;
      api
        .getAssignment(this.$route.params.assignmentId)
        .then((res) => {
          let data = res.data.data;
          let ranges = [];
          for (let v of data.allowed_ip_ranges) {
            ranges.push({ value: v });
          }
          if (ranges.length === 0) {
            ranges.push({ value: "" });
          }
          data.allowed_ip_ranges = ranges;
          this.assignment = data;
        })
        .catch(() => { });
    }
  },
};
</script>
  