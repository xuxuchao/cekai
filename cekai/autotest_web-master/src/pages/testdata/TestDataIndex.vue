<template>
    <el-tabs style="padding-top: 10px; margin-left: 10px;" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="资料管理" name="first">
        <TestData v-if="tabs.first">

        </TestData>
    </el-tab-pane>
    <!-- <el-tab-pane label="文件数据核对" name="second">
        <DataContrast v-if="tabs.second">

        </DataContrast>
    </el-tab-pane> -->

  </el-tabs>
</template>
<script>
import TestData from '../testdata/TestData'
import DataContrast from '../testdata/DataContrast'
  export default {
    components: {
           TestData,
           DataContrast           

        },
    data() {
      return {
       activeName: "first",
      tabs: {
        first: true,
        second: false,
      },

      };
    },
    methods: {
      handleClick(tab) {
      this.activeName = tab.name;
      switch (this.activeName) {
        case "first":
          this.switchTab("first");
          break;
        case "second":
          this.switchTab("second");
          break;
      }
 
    },
switchTab(tab) {
      for (let key in this.tabs) {
        if (key === tab) {
         this.tabs[key] = true;
        } else {
          this.tabs[key] = false;
        }
      }
    },

    }
  };
</script>