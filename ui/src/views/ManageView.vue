<template>
  <div>
    <el-button @click="handleAdd">添加同伴</el-button>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column label="学号" width="180">
        <template slot-scope="scope">
          <i class="el-icon-user"></i>
          <span style="margin-left: 10px">{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="密码" width="180">
        <template>
          <i class="el-icon-lock"></i>
          <span style="margin-left: 10px">**********</span>
        </template>
      </el-table-column>
      <el-table-column label="邮件" width="180">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.recv }}</span>
        </template>
      </el-table-column>
      <el-table-column label="启用" width="100">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.enabled" disabled />
        </template>
      </el-table-column>
      <el-table-column label="备注" width="180">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.extrainfo }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)"
            >删除</el-button
          >
          <el-button size="mini" type="warn" @click="test(scope.row)"> 测试</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="信息编辑" :visible.sync="EditdialogVisible" width="60%">
      <el-form
        ref="form"
        :model="editedUserData"
        label-width="120px"
        label-position="right"
      >
        <el-form-item label="学号">
          <el-input v-if="!isEdit" v-model="editedUserData.id"></el-input>
          <el-input v-else v-model="editedUserData.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="综合门户密码">
          <el-input type="password" v-model="editedUserData.pwd" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editedUserData.recv" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="editedUserData.enabled"></el-switch>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="text" v-model="editedUserData.extrainfo" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addUser">确认</el-button>
          <el-button @click="EditdialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      tableData: [],
      editedUserData: {
        id: null,
        pwd: "",
        recv: "",
        enabled: false,
        extrainfo: "无备注",
      },
      EditdialogVisible: false,
      isEdit: false,
    };
  },
  mounted() {
    this.refresh();
  },
  methods: {
    refresh() {
      this.$axios
        .get("/users")
        .then((resp) => {
          console.log(resp.data);
          this.tableData = resp.data.data;
        })
        .catch();
    },
    handleEdit(data) {
      this.editedUserData = data;
      this.EditdialogVisible = true;
      this.isEdit = true;
    },
    handleDelete(data) {
      this.$confirm("确认删除学号为" + data.id + "的信息？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$axios
            .delete("/users?id=" + data.id)
            .then((resp) => {
              this.refresh();
              this.$message({
                type: "success",
                message: "删除" + resp + "成功!",
              });
            })
            .catch();
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    handleAdd() {
      this.editedUserData = {
        id: null,
        pwd: "",
        recv: "",
        enabled: false,
        extrainfo: "无备注",
      };
      this.isEdit = false;
      this.EditdialogVisible = true;
    },
    addUser() {
      if (this.isEdit) {
        this.$axios
          .put("/users", this.editedUserData)
          .then(() => {
            this.$message({
              type: "success",
              message: "更改成功!",
            });
            this.refresh();
          })
          .catch((ex) => {
            this.$message({
              type: "success",
              message: ex,
            });
          });
        this.EditdialogVisible = false;
      } else {
        this.$axios
          .post("/users", this.editedUserData)
          .then(() => {
            this.$message({
              type: "success",
              message: "添加成功!",
            });
            this.refresh();
          })
          .catch((ex) => {
            this.$message({
              type: "success",
              message: ex,
            });
          });
        this.EditdialogVisible = false;
      }
    },
    test(data) {
      axios.post("/start", { id: data.id });
    },
  },
};
</script>
