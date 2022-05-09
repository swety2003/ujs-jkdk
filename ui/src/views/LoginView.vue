<template>
  <el-row type="flex" justify="center">
    <el-card style="width: 600px">
      <el-row type="flex" justify="center">
        <span style="font-size: 30px; color: #409eff"> 登陆 </span>
      </el-row>
      <el-row type="flex" justify="space-around">
        <el-form ref="form" label-width="40px" label-position="left">
          <el-form-item label="帐号">
            <el-input v-model="username"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input type="password" v-model="password" />
          </el-form-item>

          <el-button type="primary" round @click="login" style="width:250px;"> 登陆</el-button>
        </el-form>
      </el-row>
    </el-card>
  </el-row>
</template>

<script>
import axios from "axios";
import QueryString from "qs";
export default {
  data() {
    return {
      username: "admin",
      password: "",
    };
  },
  mounted() {
    this.$login = false;
  },
  methods: {
    login() {
      var form = {
        username: this.username,
        password: this.password,
      };
      axios
        .post("/auth/token", QueryString.stringify(form))
        .catch((err) => {
          this.$message.success(err.data);
        })
        .then((res) => {
          console.log(res);
          window.localStorage.setItem("token", res.data.access_token);
          this.$login = true;
          this.$message.success("登陆成功");
          this.$router.push("/");
        });
    },
  },
};
</script>

<style></style>
