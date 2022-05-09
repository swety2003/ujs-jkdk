<template>
  <div>
    <el-row>
      <el-card style="width: 100%" header="看板" shadow="hover">
        <el-row>
          <span> 运行状态: </span>
          <el-tag :type="stateBar">{{
            state.state ? "运行中" : "未开启"
          }}</el-tag>
          <el-tag>{{ state.targetTime }}</el-tag>
        </el-row>
        <el-row>
          <span> 详细 :</span>
          <span>{{ state.finished }}(已完成)/{{ state.max }}(总共)</span>
        </el-row>
      </el-card>
    </el-row>

    <el-row>
      <el-card style="width: 100%" header="配置" shadow="hover">
        <el-row>
          <span> (每日)执行时间: </span>
          <el-time-select
            v-model="targetTime"
            :picker-options="{
              start: '05:30',
              step: '00:30',
              end: '15:30',
            }"
            placeholder="选择时间"
          >
          </el-time-select>
        </el-row>

        <el-row>
          <el-collapse>
            <el-collapse-item title="更多配置" name="1">
              <el-form
                ref="form"
                :model="editedCFG"
                label-width="160px"
                label-position="right"
              >
                <el-form-item label="发件地址">
                  <el-input v-model="editedCFG.senderaddress"></el-input>
                </el-form-item>
                <el-form-item label="邮箱 key">
                  <el-input type="password" v-model="editedCFG.mailkey" />
                </el-form-item>
                <el-form-item label="OCR APPID">
                  <el-input v-model="editedCFG.appid" />
                </el-form-item>
                <el-form-item label="OCR APIKEY">
                  <el-input type="password" v-model="editedCFG.apikey" />
                </el-form-item>
                <el-form-item label="OCR SECRETKEY">
                  <el-input type="password" v-model="editedCFG.secretkey" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="setCFG">确认</el-button>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>
        </el-row>

        <div class="bottom clearfix">
          <el-button type="success" class="button" @click="start"
            >保存并开启</el-button
          >
          <el-button type="danger" class="button" @click="stop">停止</el-button>
          <el-button @click="refresh"> 从服务器加载配置</el-button>

          <!-- <el-button class="button">重置</el-button> -->
        </div>
      </el-card>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      targetTime: "",
      editedCFG: {
        senderaddress: "",
        mailkey: "",
        appid: "",
        apikey: "",
        secretkey: "",
      },
      state: {
        state: false,
        max: 0,
        finished: 0,
        targetTime: "07:00",
      },
      timer: null,
    };
  },
  mounted() {
    this.refresh();
    this.getState();
    if (this.timer) {
      clearInterval(this.timer);
    } else {
      this.timer = setInterval(() => {
        this.getState();
      }, 10000);
    }
  },
  methods: {
    refresh() {
      this.$axios
        .get("/cfg")
        .then((res) => {
          this.editedCFG = res.data;
        })
        .catch();
    },
    setCFG() {
      this.$axios
        .post("/cfg", this.editedCFG)
        .then((res) => {
          console.log(res);
          this.refresh();
        })
        .catch();
    },
    start() {
      console.log(this.targetTime)
      if (this.targetTime == "") {
        this.$message({
          message: '请设定时间！！',
          type: 'warning'
        });
        return;
      }
      var data = {
        targetTime: this.targetTime,
      };
      this.$axios.post("/start", data).then(() => {
        this.getState();

        this.$message("开启成功！");
      });
    },
    stop() {
      this.$axios.get("/stop").then(() => {
        this.getState();
        this.$message("已停止");
      });
    },
    getState() {
      this.$axios
        .get("state")
        .then((res) => {
          this.state = res.data;
        })
        .catch();
    },
  },
  computed: {
    stateBar() {
      return this.state.state ? "success" : "danger";
    },
  },
};
</script>
<style>
.el-row {
  margin-bottom: 20px;
}
</style>
