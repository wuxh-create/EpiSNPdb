<template>
  <div>
    <div class="content-container">
      <div class="header epistasis-background">SNP Epistasis Result for Each Cancer Type</div>
      <div class="grid">
        <div v-for="type in SnpEpistasis" :key="type" class="grid-item" @click="downloadFile('Epistasis', type)">
          <b>{{ type }}</b>
        </div>
      </div>
    </div>

    <div class="content-container">
      <div class="header gwas-background">SNP-GWAS Result for Each Cancer Type</div>
      <div class="grid">
        <div v-for="type in SnpGwas" :key="type" class="grid-item" @click="downloadFile('GWAS', type)">
          <b>{{ type }}</b>
        </div>
      </div>
    </div>

    <!-- 添加加载提示 -->
    <div v-if="downloading" class="loading-overlay">
      <div class="loading-content">
        <i class="el-icon-loading"></i>
        <p>Downloading file...</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      downloading: false, // 添加下载状态
      SnpEpistasis: [
        "Breast", "Prostate", "Melanoma", "Colon",
        "Cervical", "Lung", "Bladder", "Rectal", // 注意这里修正了"Cervica"为"Cervical"
        "Uterine", "Kidney", "Ovarian", "Pancreatic",
        "Esophagus", "Stomach", "Brain", "Liver"
      ],
      SnpGwas: [
        "Breast", "Prostate", "Melanoma", "Colon",
        "Cervical", "Lung", "Bladder", "Rectal", // 注意这里修正了"Cervica"为"Cervical"
        "Uterine", "Kidney", "Ovarian", "Pancreatic",
        "Esophagus", "Stomach", "Brain", "Liver"
      ],
    };
  },
  methods: {
    downloadFile(category, type) {
      // 防止重复点击
      if (this.downloading) {
        return;
      }

      this.downloading = true;

      let params = {
        category: category,
        cancerType: type
      };
      
      // 打印传递的参数
      console.log('Downloading file with params:', params);

      axios.post('api/DownloadFile', params, { 
        responseType: 'blob',
        timeout: 30000 // 设置30秒超时
      })
      .then(response => {
        // 检查响应状态
        if (response.status === 200) {
          // 从响应头获取文件名（如果后端设置了）
          const contentDisposition = response.headers['content-disposition'];
          let fileName = `${params.category}_${params.cancerType}.csv`;
          
          if (contentDisposition) {
            const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
            if (fileNameMatch) {
              fileName = fileNameMatch[1];
            }
          }

          // 创建下载链接
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', fileName);
          document.body.appendChild(link);
          link.click();
          
          // 清理
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
          
          // 显示成功消息
          this.$message({
            message: `File ${fileName} downloaded successfully!`,
            type: 'success',
            duration: 3000
          });
        }
      })
      .catch(error => {
        console.error('Error during file download:', error);
        
        // 处理不同类型的错误
        if (error.response && error.response.status === 404) {
          this.$message({
            message: `File not found for ${params.category} - ${params.cancerType}`,
            type: 'warning',
            duration: 3000
          });
        } else if (error.code === 'ECONNABORTED') {
          this.$message({
            message: 'Download timeout. Please try again.',
            type: 'error',
            duration: 3000
          });
        } else {
          this.$message({
            message: 'Download failed. Please try again later.',
            type: 'error',
            duration: 3000
          });
        }
      })
      .finally(() => {
        this.downloading = false;
      });
    }
  }
};
</script>

<style scoped>
.content-container {
  width: 1140px;
  margin: 20px auto 0; /* 设置上边框距离为20px */
  border: 1px solid #cddeff;
  border-radius: 8px;
  background-color: white;
}

.epistasis-background {
  background-color: #cddeff; /* 适用于SNP Epistasis */
  color: white;
  padding: 8px;
  border-radius: 8px 8px 0 0;
}

.gwas-background {
  background-color: #cddeff; /* 适用于SNP-GWAS */
  color: white;
  padding: 8px;
  border-radius: 8px 8px 0 0;
}

.header {
  font-size: 1.1em;
  margin-bottom: 5px;
  color: #29506D;
  font-weight: bold;
}

.grid {
  display: flex;
  flex-wrap: wrap;
}

.grid-item {
  flex: 1 1 calc(25% - 10px); /* 每行显示4个 */
  margin: 5px;
  padding: 10px;
  background: #F2F5ED;
  text-align: center;
  border-radius: 4px;
  transition: transform 0.3s ease, box-shadow 0.3s ease; 
  font-size: 1em;
  cursor: pointer; /* 添加鼠标指针效果 */
}

/* 添加点击效果 */
.grid-item:active {
  transform: scale(1.02); /* 点击时放大2%，实现整体扩大的效果 */
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

/* 添加禁用状态样式 */
.grid-item.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 加载覆盖层样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.loading-content i {
  font-size: 24px;
  color: #409eff;
}

.loading-content p {
  margin: 10px 0 0 0;
  color: #666;
  font-size: 14px;
}
</style>