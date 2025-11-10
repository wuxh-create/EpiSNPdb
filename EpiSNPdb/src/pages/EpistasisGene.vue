<template>
  <div class="content-container">
    <!-- 查询模块 -->
    <el-card class="box-card">
      <!-- card -->
      <el-row class="custom-row" :style="{ marginBottom: '15px' }">
        <el-col :span="24">
          <p class="card-description" style="font-size: 18px; line-height: 1.7; font-family: 'Helvetica';">
            This module provides gene expression correlation analysis across 16 cancer types, showing correlation relationships between gene pairs.
            
            This module provides <span style="color: blue; font-weight: bold;">gene correlation</span> analysis with statistical significance across 16 cancer types.
          </p>
        </el-col>
      </el-row>

      <!-- search methods -->
      <div>
        <el-row :gutter="20" type="flex" justify="center">
          <!-- Query type select -->
          <el-col :span="5" :offset="0">
            <span class="input-label">Query type:</span>
            <el-select v-model="selectQueryType" placeholder="Query type" class="place-input query-type-select" style="width: 100%; z-index: 1000;">
              <el-option v-for="query in queryTypes" :key="query.id" :value="query.queryName">
                <span style="float: left">{{ query.queryName }}</span>
              </el-option>
            </el-select>
          </el-col>
          <!-- Cancer type select -->
          <el-col :span="5" :offset="0">
            <span class="input-label">Cancer type:</span>
            <el-select v-model="selectCancerType" placeholder="Cancer type" class="place-input cancer-type-select" style="width: 100%;font-size: 17px;">
              <el-option v-for="cancer in cancerType" :key="cancer.id" :value="cancer.cancerName">
                <span style="float: left">{{ cancer.cancerName }}</span>
                <span style="float: right">(N={{ cancer.sampleNumber }})</span>
              </el-option>
            </el-select>
          </el-col>
          <!-- Gene input -->
          <el-col :span="5" :offset="0" v-if="selectQueryType === 'Gene'">
            <span class="input-label">Gene:</span>
            <el-input v-model="queryGene1" placeholder="Gene" class="place-input" style="width: 100%;"></el-input>
            <span :class="{ 'text-black': !isClicked1, 'text-orange': isClicked1 }" @click="handleClickAndSetQueryGene1" style="font-size: 16px;">e.g., TP53</span>
          </el-col>
          <!-- Gene epistasis input -->
          <el-col :span="5" :offset="0" v-if="selectQueryType === 'Gene epistasis'">
            <span class="input-label">Gene epistasis:</span>
            <el-input v-model="queryGene1" placeholder="Gene epistasis" class="place-input" style="width: 100%;"></el-input>
            <span :class="{ 'text-black': !isClicked2, 'text-orange': isClicked2 }" @click="handleClickAndSetQueryGene2" style="font-size: 16px;">e.g., TP53_BRCA1</span>
          </el-col>
          <!-- Correlation threshold select -->
          <el-col :span="5" :offset="0">
            <span class="input-label">Correlation threshold:</span>
            <el-select v-model="correlationThreshold" placeholder="Correlation" class="place-input correlation-select" style="width: 100%;font-size: 17px;">
              <el-option label="0.1" value="0.1"></el-option>
              <el-option label="0.3" value="0.3"></el-option>
              <el-option label="0.5" value="0.5"></el-option>
              <el-option label="0.7" value="0.7"></el-option>
            </el-select>
          </el-col>
        </el-row>
      </div>

      <div style="margin: 15px 0 0px;">
        <el-row type="flex" justify="center" align="middle">
            <el-col :span="4"></el-col>
            <el-col :span="4" class="text-center">
            <el-button type="primary" class="submit-button" @click="submitForm">Submit</el-button>
            </el-col>
            <el-col :span="4" class="text-center">
            <el-button type="danger" class="cancel-button" @click="clearInput">Cancel</el-button>
            </el-col>
            <el-col :span="4"></el-col>
        </el-row>
      </div>

    </el-card>

    <!-- 结果展示模块 -->
    <el-card class="box-card">
      <div class="header-controls">
          <el-pagination
            :hide-on-single-page="true"
            :total="recordNumber"
            :page-size="perPage"
            :current-page.sync="currentPage"
            @current-change="currentChange"
            layout="prev, pager, next"
          ></el-pagination>

          <div style="margin-bottom: 0px; text-align: right; margin-right: 20px;">
            <el-button
              type="primary"
              :circle="true"
              @click="downloadCSV"
              style="font-size: 35px; padding: 0; background-color: white; color: blue; font-weight: bold;"
            >
              <i class="el-icon-download"></i>
            </el-button>
          </div>
        </div>

      <el-table :data="QTLData.GeneCorrelation" style="width: 100%;" empty-text="No gene correlation results found for your query">
        <!-- Correlation plot column -->
        <el-table-column prop="plotStatus" label="Plot" width="60" align="center" class="custom-column-header">
          <template v-slot="scope">
            <a-icon 
              type="dot-chart" 
              theme="outlined"
              @click="fetchPdf(scope.row.Cancertype, scope.row.Gene1, scope.row.Gene2)"
              style="font-size: 2.1em; cursor: pointer; color: #2196f3;"
            />
          </template>
        </el-table-column>
        <!-- Cancer type column -->
        <el-table-column
          prop="Cancertype"
          label="Cancer"
          width="107"
          align="center"
          class="custom-column-header"
          show-overflow-tooltip
        >
          <template v-slot="scope">
            <span
              :style="{
                color: 'red',
                fontSize: cancerTypes.includes(scope.row.Cancertype) ? '1.1em' : 'inherit'
              }"
            >
              {{ scope.row.Cancertype }}
            </span>
          </template>
        </el-table-column>
        <!-- Gene1 column -->
        <el-table-column prop="Gene1" label="Gene1" width="100" align="center" class="custom-column-header">
          <template slot-scope="scope">
            <span>{{ scope.row.Gene1 }}</span>
          </template>
        </el-table-column>
        <!-- Gene2 column -->
        <el-table-column prop="Gene2" label="Gene2" width="100" align="center" class="custom-column-header">
          <template slot-scope="scope">
            <span>{{ scope.row.Gene2 }}</span>
          </template>
        </el-table-column>
        <!-- Correlation column -->
        <el-table-column prop="correlation" label="Correlation" width="144" align="center" show-overflow-tooltip class="custom-column-header">
          <template v-slot:header>
            Correlation
            <el-tooltip content="Spearman correlation coefficient" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          <template v-slot="scope">
            {{ formatCorrelationValue(scope.row.correlation) }}
          </template>
        </el-table-column>
        <!-- P-value column -->
        <el-table-column prop="P_value" label="P-value" width="117" sortable align="center" show-overflow-tooltip class="custom-column-header">
          <template v-slot:header>
            P-value
            <el-tooltip content="Statistical significance of correlation" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          <template v-slot="scope">
            {{ formatPValue(scope.row.P_value) }}
          </template>
        </el-table-column>
        <el-table-column prop="coexpression" label="coexpression" width="140" align="center" class="custom-column-header" show-overflow-tooltip>
          <template slot-scope="scope">
              <span v-if="scope.row.coexpression === 'NA' || !scope.row.coexpression">
                  <i class="el-icon-minus" style="color: #FA8072; font-weight: bold;"></i>
              </span>
              <span v-else>
                  {{ scope.row.coexpression }}
              </span>
          </template>
          <template v-slot:header>
              Coexpression
              <el-tooltip class="item" effect="dark" content="Whether the gene pair shows coexpression" placement="top">
                  <i class="el-icon-question"></i>
              </el-tooltip>
          </template>
       </el-table-column>
        <!-- Text mining transferred column -->
        <el-table-column prop="textmining_transferred" label="Text mining transferred" width="210" align="center" class="custom-column-header" show-overflow-tooltip>
          <template v-slot:header>
            Text mining transferred
            <el-tooltip content="Text mining transferred score from STRING database" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          <template slot-scope="scope">
              <span v-if="scope.row.textmining_transferred === 'NA' || !scope.row.textmining_transferred">
                  <i class="el-icon-minus" style="color: #FA8072; font-weight: bold;"></i>
              </span>
              <span v-else>
                  {{ scope.row.textmining_transferred }}
              </span>
          </template>
        </el-table-column>
        <!-- Combined score column -->
        <el-table-column prop="combined_score" label="Combined score" width="160" align="center" class="custom-column-header" show-overflow-tooltip>
          <template v-slot:header>
            Combined score
            <el-tooltip content="Combined score from STRING database" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          <template slot-scope="scope">
              <span v-if="scope.row.combined_score === 'NA' || !scope.row.combined_score">
                  <i class="el-icon-minus" style="color: #FA8072; font-weight: bold;"></i>
              </span>
              <span v-else>
                  {{ scope.row.combined_score }}
              </span>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog 
        :visible.sync="imageDialogVisiblePlot" 
        :style="{ maxWidth: '700px', margin: '0 auto' }" 
        width="auto" 
        @close="handleClosePlot" 
        :close-on-click-modal="false" 
        :close-on-press-escape="true" 
        :modal-append-to-body="useModalAppendToBody"
      >
        <div style="display: flex; flex-direction: column; align-items: center; position: relative;" @click="handleClosePlot">
          <img 
            :src="imageUrl" 
            @click="handleClosePlot"
            style="width: 600px; height: 500px; object-fit: contain; cursor: pointer; position: relative; z-index: 2;" 
            alt="Correlation Plot"
          >
          <button 
            class="download-button"
            :class="{ 'clicked': downloadClickedPlot }"
            @click.stop="handleDownloadPlot"
            style="position: relative; z-index: 2; margin-top: 20px; font-size: 18px;"
          >
            Download
          </button>
        </div>
      </el-dialog>

      <div v-if="showAlert" class="custom-alert" @click="closeAlert">
        <div class="custom-alert-content" @click="stopPropagation">
          <div style="font-size: 20px; line-height: 1.5em; text-align: center;">
            <strong style="color: blue;">Please note: </strong>
            The correlation plot for this gene pair is not available or 
            <strong style="color: black;">correlation is not significant</strong> in the context of the current cancer phenotype.
          </div>
          <el-button @click="closeAlert" style="margin-top: 20px;">OK</el-button>
        </div>
      </div>

    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GeneCorrelation',
  data() {
    return {
      selectQueryType: '',
      selectCancerType:'',
      correlationThreshold:'',
      queryTypes: [
        { id: '001', queryName: 'Gene' },
        { id: '002', queryName: 'Gene epistasis' },
        { id: '003', queryName: 'Cancer type' }
      ],
      cancerType: [
        { id: '001', cancerName: 'All', sampleNumber: '399723' },
        { id: '002', cancerName: 'Breast', sampleNumber: '189339' },
        { id: '003', cancerName: 'Prostate', sampleNumber: '159222' },
        { id: '004', cancerName: 'Melanoma', sampleNumber: '322104' },
        { id: '005', cancerName: 'Colon', sampleNumber: '320482' },
        { id: '006', cancerName: 'Cervical', sampleNumber: '176438' },
        { id: '007', cancerName: 'Lung', sampleNumber: '318728' },
        { id: '008', cancerName: 'Bladder', sampleNumber: '317673' },
        { id: '009', cancerName: 'Rectal', sampleNumber: '316597' },
        { id: '0010', cancerName: 'Uterine', sampleNumber: '172157' },
        { id: '0011', cancerName: 'Kidney', sampleNumber: '315750' },
        { id: '0012', cancerName: 'Ovarian', sampleNumber: '171548' },
        { id: '0013', cancerName: 'Pancreatic', sampleNumber: '315056' },
        { id: '0014', cancerName: 'Esophagus', sampleNumber: '315022' },
        { id: '0015', cancerName: 'Stomach', sampleNumber: '314676' },
        { id: '0016', cancerName: 'Brain', sampleNumber: '314501' },
        { id: '0017', cancerName: 'Liver', sampleNumber: '314490' }
      ],
      cancerTypes: [
          "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus","Kidney", "Liver", "Lung", "Melanoma", 
          "Ovarian", "Pancreatic", "Prostate","Rectal", "Stomach", "Uterine"
      ],
      QTLData: {
        GeneCorrelation: []
      },
      recordNumber: 0,
      showBlock: 'N',
      correlationThreshold: '',
      loading: false,
      selectCancerType: '',
      isClicked1: false,
      isClicked2: false,
      queryGene1: 'TP53_BRCA1',
      flag: 1,
      currentPage: 1,
      perPage: 8,
      rowHeight: 60,
      defaultQueryType: 'Gene epistasis',
      defaultCancerType: 'Breast',
      defaultCorrelationThreshold: '0.3',
      currentCancertype: '',
      currentGene1: '',
      currentGene2: '',
      imageDialogVisiblePlot: false,
      imageUrl: '',
      downloadClickedPlot: false,
      useModalAppendToBody: false,
      showAlert: false,
      isFirstLoad: true 
    };
  },
  computed: {
    tableHeight() {
      return this.QTLData.GeneCorrelation.length < this.perPage
        ? this.rowHeight * this.QTLData.GeneCorrelation.length + 50
        : this.rowHeight * this.perPage + 50;
    },
  },
  methods: {
    // 格式化相关性数值，保留两位有效数字
    formatCorrelationValue(value) {
      if (value === undefined || value === null || value === 'NA') {
        return 'NA';
      }
      if (typeof value === 'number') {
        return value.toPrecision(2);
      }
      return value;
    },
    // 格式化数值字段，处理NA值
    formatNumericValue(value, decimals = 3) {
      if (value === undefined || value === null || value === 'NA') {
        return 'NA';
      }
      if (typeof value === 'number') {
        return value.toFixed(decimals);
      }
      return value;
    },
    // 格式化P值
    formatPValue(value) {
      if (value === undefined || value === null || value === 'NA') {
        return 'NA';
      }
      if (typeof value === 'number' && value !== 100) {
        return value.toExponential(2);
      }
      return '-';
    },
    setQueryGene1(value) {
      this.queryGene1 = value;
    },
    toggleClickStatus(clickIndex) {
      this['isClicked' + clickIndex] = !this['isClicked' + clickIndex];
    },
    handleClickAndSetQueryGene1() {
      this.setQueryGene1('TP53');
      this.toggleClickStatus(1);
      this.selectCancerType = 'Breast';
      this.correlationThreshold = '0.3';
    },
    handleClickAndSetQueryGene2() {
      this.setQueryGene1('TP53_BRCA1');
      this.toggleClickStatus(2);
      this.selectCancerType = 'Breast';
      this.correlationThreshold = '0.3';
    },
    handleClosePlot() {
      this.imageDialogVisiblePlot = false; 
      this.downloadClickedPlot = false;
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl); 
        this.imageUrl = ''; 
      }
    },
    valueCheck(inputValue) {
        // Check for invalid characters
        if (/[@#\$%\^&\*]+/g.test(inputValue)) {
            this.$message.error('Invalid input');
            return null;
        }

        // Basic gene name pattern validation
        const validPattern = /^[A-Za-z0-9_-]+$/;
        const trimmedValue = inputValue.trim();

        if (!validPattern.test(trimmedValue)) {
            this.$message.error('Invalid gene name');
            return null;
        }

        return trimmedValue.toUpperCase();
    },
    normalizeAndTrimInput(input) {
      return input.replace(/\s+/g, ''); // 去除所有空格
    },
    changePage(newPage) {
      this.currentPage = newPage;
      this.submitForm();
    },
    initData() {
        // 自动请求一批数据
        if (this.isFirstLoad) {
            this.isFirstLoad = false;
            axios.get('api/GeneCorrelation', { params: { isFirstLoad: true, Type: true } })
                .then(response => {
                    this.QTLData.GeneCorrelation = response.data.GeneCorrelation_results;
                    this.recordNumber = response.data.total_count;
                    this.loading = false;
                }).catch(error => {
                    this.loading = false;
                });
        }
    },
    isValidInput(inputValue) {
      const validPattern = /^[a-zA-Z0-9-_]+$/;
      return validPattern.test(inputValue);
    },
    normalizeInput(inputValue) {
      const trimmedValue = inputValue.trim();
      return trimmedValue.toUpperCase();
    },
    submitForm() {
      this.showBlock = 'Y';
      this.queryGene1 = this.normalizeAndTrimInput(this.queryGene1);
      
      let queryParams = {
        selectQueryType: this.selectQueryType || 'Gene',
        selectCancerType: this.selectCancerType || 'All',
        currentPage: this.currentPage,
        perPage: this.perPage,
        correlationThreshold: this.correlationThreshold,
        isFirstLoad: false
      };

      if (this.selectQueryType === 'Gene') {
        if (!this.isValidInput(this.queryGene1)) {
          this.$alert('Invalid gene name input', 'Error', {
            confirmButtonText: 'OK',
            callback: () => {
              this.QTLData.GeneCorrelation = [];
              this.recordNumber = 0;
            }
          });
          return;
        }
        queryParams.queryGene1 = this.normalizeInput(this.queryGene1);
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.correlationThreshold = this.correlationThreshold;
      } else if (this.selectQueryType === 'Gene epistasis') {
        if (!this.isValidInput(this.queryGene1)) {
          this.$alert('Invalid gene epistasis input', 'Error', {
            confirmButtonText: 'OK',
            callback: () => {
              this.QTLData.GeneCorrelation = [];
              this.recordNumber = 0;
            }
          });
          return;
        }
        queryParams.queryGene1 = this.normalizeInput(this.queryGene1);
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.correlationThreshold = this.correlationThreshold;
      } else if (this.selectQueryType === 'Cancer type') {
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.correlationThreshold = this.correlationThreshold;
      }

      axios.get('api/GeneCorrelation', { params: queryParams })
        .then(response => {
          this.QTLData.GeneCorrelation = response.data.GeneCorrelation_results;
          this.recordNumber = response.data.total_count;
          this.loading = false;
        }).catch(error => {
          this.loading = false;
        });

      if (this.flag === 1) {
        this.loading = true;
      } else {
        this.loading = false;
      }
    },
    clearInput() {
      this.selectQueryType = '';
      this.selectCancerType = '';
      this.queryGene1 = '';
      this.correlationThreshold = '';
      this.isClicked1 = false;
      this.isClicked2 = false;
    },
    currentChange(page) {
      this.currentPage = page;
      this.submitForm();
    },
    downloadCSV() {
        if (!Array.isArray(this.QTLData.GeneCorrelation) || this.QTLData.GeneCorrelation.length === 0) {
            this.$message.error('No data available for download');
            return;
        }

        // 定义需要导出的列
        const headers = ['Cancertype', 'Gene1', 'Gene2', 'Correlation', 'P-value', 'Coexpression', 'Text mining transferred', 'Combined score'];
        const rows = this.QTLData.GeneCorrelation.map(item => [
            item.Cancertype,
            item.Gene1,
            item.Gene2,
            this.formatCorrelationValue(item.correlation),
            this.formatPValue(item.P_value),
            (item.coexpression === 'NA' || !item.coexpression) ? '-' : item.coexpression,
            (item.textmining_transferred === 'NA' || !item.textmining_transferred) ? '-' : item.textmining_transferred,
            (item.combined_score === 'NA' || !item.combined_score) ? '-' : item.combined_score
        ]);

        // 创建CSV内容
        let csvContent = "data:text/csv;charset=utf-8,"
            + headers.join(",") + "\n"
            + rows.map(e => e.join(",")).join("\n");

        // 创建下载链接
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");

        // 生成文件名
        const cancertype = this.selectCancerType || '';
        const gene = this.queryGene1 || ''; 
        const correlationThreshold = this.correlationThreshold || '';

        const fileNameParts = [cancertype, gene, correlationThreshold];
        const fileName = fileNameParts.filter(part => part !== '').join('_') + ".csv";

        link.setAttribute("href", encodedUri);
        link.setAttribute("download", fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
    handleDownloadPlot() {
        this.downloadClickedPlot = true; 
        this.PlotdownloadPdf();
    },
    fetchPdf(Cancertype, Gene1, Gene2) {
      this.currentCancertype = Cancertype;
      this.currentGene1 = Gene1;
      this.currentGene2 = Gene2;
      
      axios.get(`api/GeneCorrelationPlot`, {
        params: {
          Cancertype: encodeURIComponent(Cancertype),
          Gene1: encodeURIComponent(Gene1),
          Gene2: encodeURIComponent(Gene2)
        },
        responseType: 'blob'
      })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        this.imageUrl = imageUrl;
        this.imageDialogVisiblePlot = true;
      })
      .catch(error => {
        console.error('Error fetching correlation plot:', error);
        this.showAlert = true;
      });
    },
    fetchCorrelationPlot(Cancertype, Gene1, Gene2) {
      this.currentCancertype = Cancertype;
      this.currentGene1 = Gene1;
      this.currentGene2 = Gene2;
      
      axios.get(`api/GeneCorrelationPlot`, {
        params: {
          Cancertype: encodeURIComponent(Cancertype),
          Gene1: encodeURIComponent(Gene1),
          Gene2: encodeURIComponent(Gene2)
        },
        responseType: 'blob'
      })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        this.imageUrl = imageUrl;
        this.imageDialogVisiblePlot = true;
      })
      .catch(error => {
        console.error('Error fetching correlation plot:', error);
        this.showAlert = true;
      });
    },
    closeAlert() {
        this.showAlert = false;
    },
    stopPropagation(event) {
        event.stopPropagation();
    },
    PlotdownloadPdf() {
      const cancertype = this.currentCancertype;
      const gene1 = this.currentGene1;
      const gene2 = this.currentGene2;
      
      axios.get(`api/GeneCorrelationPlotDownload`, {
        params: {
          Cancertype: encodeURIComponent(cancertype),
          Gene1: encodeURIComponent(gene1),
          Gene2: encodeURIComponent(gene2)
        },
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const fileName = `${cancertype}_${gene1}_${gene2}_correlation.pdf`;
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error downloading correlation plot:', error);
        this.downloadClickedPlot = false;
        this.$alert('<strong style="color: blue;">注意：</strong> <strong style="color: black;">相关性图表下载失败</strong>', {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '确定',
        });
      });
    }
  },
  mounted() {
    this.initData();
    this.selectQueryType = this.defaultQueryType;
    this.selectCancerType = this.defaultCancerType;
    this.correlationThreshold = this.defaultCorrelationThreshold;
  }
};
</script>

<style scoped>
.input-label {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
  color: #FA8072;
  font-weight: bold;
  font-family: 'Helvetica';
}
.content-container {
    width: 1140px;
    margin: 0 auto;
    font-family: 'Helvetica';
} 
.text-black {
    display: block;
    color: black;
    cursor: pointer;
    margin-top: 8px;
}
.text-orange {
    display: block;
    color: orange;
    cursor: pointer;
    margin-top: 8px;
}
::v-deep .el-table thead th {
  color: #2d4059 !important;
  font-family: 'Helvetica';
  font-weight: bold;
}
.submit-button {
  background-color: #FA8072;
  font-size: 17px;
  border-radius: 4px;
  border-color: #FA8072;
  margin: 0;
}

.submit-button:hover, 
.submit-button:focus, 
.submit-button:active {
  background-color: #FA8072;
  border-color: #FA8072;
}

.cancel-button {
  background-color: #77acf1;
  font-size: 17px;
  border-radius: 4px;
  border-color: #77acf1;
  margin: 0;
}

.cancel-button:hover, 
.cancel-button:focus, 
.cancel-button:active {
  background-color: #77acf1;
  border-color: #77acf1;
}
.box-card {
    margin: 5px 0;
    padding: 10px;
}
.custom-row {
    margin-top: -10px;
}
.card-description {
    font-size: 15px;
    color: #333;
    margin-top: 5px;
    font-family: 'Helvetica';
}
.place-input {
    font-size: 17px;
    font-family: 'Helvetica';
}
::v-deep(.el-select .el-input__inner) {
    font-size: 17px;
}

.cancer-type-select ::v-deep .el-input__inner {
    font-size: 17px;
}

.correlation-select ::v-deep .el-input__inner {
    font-size: 17px;
}

.query-type-select {
    z-index: 2000; 
}
.header-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0px;
}
.custom-column-header {
  background-color: #f5f5f5;
  font-weight: bold;
  text-align: center;
}
.el-icon-zoom-in {
  color: #FF7C43;
  font-size: 1.2em;
}
.custom-icon {
  font-size: 20px;
  font-weight: bold;
}
.custom-alert {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2000;
}

.custom-alert-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  width: 100%;
}
/* download style */    
.el-button--primary {
    border-color: transparent; /* 移除按钮边框 */
}
.download-button .el-icon-download {
    font-size: 16px; /* 增大图标 */
    font-weight: bold; /* 加粗图标 */
    color: blue; /* 设置图标颜色 */
}
</style>