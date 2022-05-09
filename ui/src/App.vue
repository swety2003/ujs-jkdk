<template>
  <el-container style="height: 100%">
    <el-header style="padding: 0" height="80px">
      <el-card shadow="never" style="width: 100%; height: 100%">
        <el-row type="flex" justify="space-between">
          <span style="font-size: 20px; margin: 10px"> FUCK打卡 </span>
          <el-button @click="logout" type="danger" v-if="isHide">
            登出
          </el-button>
        </el-row>
      </el-card>
    </el-header>
    <el-container>
      <el-aside width="250px" v-if="isHide">
        <el-menu
          style="height: 100%"
          router
          @open="handleOpen"
          @close="handleClose"
        >
          <el-menu-item index="/">
            <i class="el-icon-menu"></i>
            <span slot="title">看板</span>
          </el-menu-item>
          <el-menu-item index="/manage">
            <i class="el-icon-document"></i>
            <span slot="title">管理</span>
          </el-menu-item>
          <el-menu-item index="/about">
            <i class="el-icon-info"></i>
            <span slot="title">关于</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "app",
  components: {},
  mounted() {
    if (!this.$login && this.$route.path != "/login") {
      console.log("Go to login!");
      this.$router.push("/login");
    }
  },
  computed: {
    isHide() {
      return this.$route.path != "/login";
      // return false
    },
  },
  methods: {
    logout() {
      this.$$login = false;
      this.$router.push("/login");
    },
  },
};
</script>

<style>
body,
html,
#app .el-container {
  margin: 0px;
  width: 100%;
  height: 100%;
}
</style>
