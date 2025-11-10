<template>
  <div class="header">
    <div class="content-container">
      <img src="EpiSNP-db/SSIdb5.png" style="width: 1140px;height: 150px" alt="Logo" class="logo">
      <div class="nav-container">
        <el-menu
          class="el-menu-demo larger-font-menu"
          mode="horizontal"
          background-color="#A3BFFA"
          text-color="#fff"
          active-text-color="#ff6600"
        >
          <el-menu-item index="1" :class="{ active: currentRoute === '/' }">
            <router-link to="/" exact>Home</router-link>
          </el-menu-item>
          <el-menu-item index="2" :class="{ active: currentRoute === '/EpistasisSNP' }">
            <router-link to="/EpistasisSNP">Epistasis-SNP</router-link>
          </el-menu-item>
          <el-menu-item index="3" :class="{ active: currentRoute === '/EpiSNPAnnotation' }">
            <router-link to="/EpiSNPAnnotation">EpiSNP-Annotation</router-link>
          </el-menu-item>
          <el-menu-item index="4" :class="{ active: currentRoute === '/EpiSNPGWAS' }">
            <router-link to="/EpiSNPGWAS">EpiSNP-GWAS</router-link>
          </el-menu-item>
          <el-menu-item index="5" :class="{ active: currentRoute === '/EpiSNPSurvival' }">
            <router-link to="/EpiSNPSurvival">EpiSNP-Survival</router-link>
          </el-menu-item>
          <el-menu-item index="6" :class="{ active: currentRoute === '/EpistasisMutation' }">
            <router-link to="/EpistasisMutation">Epistasis-Mutation</router-link>
          </el-menu-item>
          <el-menu-item index="7" :class="{ active: currentRoute === '/Download' }">
            <router-link to="/Download">Download</router-link>
          </el-menu-item>
          <el-menu-item index="8" :class="{ active: currentRoute === '/Help' }">
            <router-link to="/Help">Help</router-link>
          </el-menu-item>
        </el-menu>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Header',
  computed: {
    currentRoute() {
      return this.$route.path;
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.content-container {
  width: 1140px;
  margin: 0 auto; /* 确保内容在页面中居中 */
}

.logo {
  width: 100%;
  margin-bottom: 0;
}

.nav-container {
  display: flex;
  justify-content: center;
  background-color: #A3BFFA;
}

.el-menu-demo {
  background-color: #A8DADC;
  display: flex;
  justify-content: space-around; /* 均匀分布 */
  align-items: center; /* 上下居中 */
  width: 100%;
  height: 50px; /* 确保导航栏有足够的高度 */
}

.el-menu-demo .el-menu-item {
  font-size: 16px;
  font-weight: bold;
  padding: 10px 15px;
  line-height: 1.5;
  height: auto;
}

.larger-font-menu .el-menu-item {
  font-size: 17px; /* 设置更大的字体大小 */
}
</style>
