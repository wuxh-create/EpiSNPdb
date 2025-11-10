<template>
  <div class="header">
    <div class="content-container">
      <img src="EpiSNP-db_final.png" style="width: 1140px;height: 150px" alt="Logo" class="logo">
      <div class="nav-container">
        <el-menu
          class="el-menu-demo larger-font-menu"
          mode="horizontal"
          background-color="#9ACDFA"
          text-color="#336699"
          active-text-color="#ce1212"
        >
          <router-link to="/" exact>
            <el-menu-item index="1" :class="{ active: currentRoute === '/' }">
              Home
            </el-menu-item>
          </router-link>
          <router-link to="/EpistasisSNP">
            <el-menu-item index="2" :class="{ active: currentRoute === '/EpistasisSNP' }">
              Epistasis-SNP
            </el-menu-item>
          </router-link>
          <router-link to="/EpistasisGene">
            <el-menu-item index="9" :class="{ active: currentRoute === '/EpistasisGene' }">
              Epistasis-Gene
            </el-menu-item>
          </router-link>
          <router-link to="/EpiSNPAnnotation">
            <el-menu-item index="3" :class="{ active: currentRoute === '/EpiSNPAnnotation' }">
              EpiSNP-Annotation
            </el-menu-item>
          </router-link>
          <router-link to="/EpiSNPGWAS">
            <el-menu-item index="4" :class="{ active: currentRoute === '/EpiSNPGWAS' }">
              EpiSNP-GWAS
            </el-menu-item>
          </router-link>
          <router-link to="/EpiSNPSurvival">
            <el-menu-item index="5" :class="{ active: currentRoute === '/EpiSNPSurvival' }">
              EpiSNP-Survival
            </el-menu-item>
          </router-link>
          <router-link to="/EpistasisMutation">
            <el-menu-item index="6" :class="{ active: currentRoute === '/EpistasisMutation' }">
              Epistasis-Mutation
            </el-menu-item>
          </router-link>
          <router-link to="/Download">
            <el-menu-item index="7" :class="{ active: currentRoute === '/download' }">
              Download
            </el-menu-item>
          </router-link>
          <router-link to="/Document">
            <el-menu-item index="8" :class="{ active: currentRoute === '/Document' }">
              Document
            </el-menu-item>
          </router-link>
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
a:hover {
  text-decoration: none !important; 
}
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
  background-color: #86c6f4;
  display: flex;
  justify-content: space-around; /* 均匀分布 */
  align-items: center; /* 上下居中 */
  width: 100%;
  height: 50px; /* 确保导航栏有足够的高度 */
}

.el-menu-demo .el-menu-item {
  font-size: 16px;
  font-weight: bold;
  padding: 5px 7px;
  line-height: 1.5;
  height: auto;
}

.larger-font-menu .el-menu-item {
  font-size: 17px;
}

.el-menu-item a {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none !important;
  color: inherit; 
}
</style>
