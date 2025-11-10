<template>
  <div class="content-container">
    <!-- 查询模块 -->
    <el-card class="box-card">
      <!-- card -->
      <el-row class="custom-row" :style="{ marginBottom: '15px' }">
        <el-col :span="24">
          <p class="card-description" style="font-size: 18px; line-height: 1.7; font-family: 'Helvetica';">
            This module provides <span style="color: blue; font-weight: bold;">145,505</span> epistasis with a P-value less than 1e-5 across 16 cancer types.
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
          <el-col :span="5" :offset="0" v-if="selectQueryType === 'SNP'">
            <span class="input-label">SNP:</span>
            <el-input v-model="queryRsid1" placeholder="SNP" class="place-input" style="width: 100%;"></el-input>
            <span :class="{ 'text-black': !isClicked1, 'text-orange': isClicked1 }" @click="handleClickAndSetQueryRsid1" style="font-size: 16px;">e.g., rs12924101</span>
          </el-col>
          <el-col :span="5" :offset="0" v-if="selectQueryType === 'SNP epistasis'">
            <span class="input-label">SNP epistasis:</span>
            <el-input v-model="queryRsid1" placeholder="SNP epistasis" class="place-input" style="width: 100%;"></el-input>
            <span :class="{ 'text-black': !isClicked2, 'text-orange': isClicked2 }" @click="handleClickAndSetQueryRsid2" style="font-size: 16px;">e.g., rs6687430_rs17781327</span>
          </el-col>
          <!-- P-value filter select -->
          <el-col :span="5" :offset="0">
            <span class="input-label">P-value threshold:</span>
            <el-select v-model="pValueThreshold" placeholder="P-value" class="place-input p-value-select" style="width: 100%;font-size: 17px;">
              <el-option label="0.05" value="0.05"></el-option>
              <el-option label="1e-5" value="1e-5"></el-option>
              <el-option label="5e-6" value="5e-6"></el-option>
              <el-option label="5e-8" value="5e-8"></el-option>
            </el-select>
          </el-col>
        </el-row>
      </div>

      <div style="margin: 15px 0 0px;">
        <el-row type="flex" justify="center">
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
        <el-pagination :hide-on-single-page="true" :total="recordNumber" :page-size="perPage" :current-page.sync="currentPage" @current-change="currentChange" layout="prev, pager, next"></el-pagination>

        <div style="margin-bottom: 0px; text-align: right; margin-right: 20px;">
          <el-button type="primary" :circle="true" @click="downloadCSV" style="font-size: 35px; padding: 0; background-color: white; color: blue; font-weight: bold;">
            <i class="el-icon-download"></i>
          </el-button>
        </div>
      </div>

      <el-table :data="QTLData.SnpEpistasis" style="width: 100%;" empty-text="No SNP epistasis results found for your query">
        <el-table-column
            prop="Cancertype"
            label="Cancer"
            width="107"
            align="center"
            class="custom-column-header"
            show-overflow-tooltip>
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
        <el-table-column prop="SNP_epi" label="SNP epistasis" width="260" align="center" class-name="custom-column-header">
          <template slot-scope="scope">
            <span v-for="(snp, index) in scope.row.SNP_epi.split('_')" :key="index">
              {{ snp }}
              <a :href="'https://www.ncbi.nlm.nih.gov/snp/' + snp" target="_blank">
                <i class="el-icon-zoom-in" style="color: #FF7C43; font-size: 1.2em;"></i>
              </a>
              <span v-if="index === 0">_</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="ORstatus" label="Odds ratio" width="115" align="center" class-name="custom-column-header">
          <template v-slot:header>
                Odds ratio
              <el-tooltip class="item" effect="dark" content="Odds ratio for snp epistasis calculated by PLINK" placement="top">
              <i class="el-icon-question"></i>
              </el-tooltip>
          </template>
          <template v-slot="scope">
            {{ scope.row.OR_INT !== undefined ? scope.row.OR_INT.toFixed(2) : '' }}
          </template>
        </el-table-column>
        <el-table-column prop="STAT" label="STAT" width="80" align="center" class-name="custom-column-header">
          <template v-slot:header>
                  STAT
              <el-tooltip class="item" effect="dark" content="Chi-square statistic with 1 degree of freedom, calculated by PLINK" placement="top">
              <i class="el-icon-question"></i>
              </el-tooltip>
          </template>
          <template v-slot="scope">
            {{ scope.row.STAT !== undefined ? scope.row.STAT.toFixed(2) : '' }}
          </template>
        </el-table-column>
        <el-table-column prop="P" label="P-value" width="126" sortable align="center" show-overflow-tooltip class-name="custom-column-header">
          <template v-slot:header>
            P-value
            <el-tooltip class="item" effect="dark" content="Asymptotic p-value calculated by PLINK" placement="top" popper-class="tooltip-large-font">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          
          <template v-slot="scope">
            {{ scope.row.P !== undefined ? scope.row.P.toExponential(2) : '' }}
          </template>
        </el-table-column>
        <el-table-column prop="Best_snp" label="Best SNP" width="113" align="center" class-name="custom-column-header">
          <template v-slot:header>
            Best SNP
            <el-tooltip class="item" effect="dark" content="The SNP with the highest statistic obtained by testing SNP1 through PLINK." placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="saige_p" label="P-saige" width="123" sortable align="center" class-name="custom-column-header">
          <template v-slot:header>
            P-saige
            <el-tooltip class="item" effect="dark" content="Asymptotic p-value calculated by SAIGE" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
          <template v-slot="scope">
            {{ scope.row.saige_p !== undefined ? (scope.row.saige_p === 0 ? '0' : scope.row.saige_p.toExponential(2)) : '' }}
          </template>
        </el-table-column>
        <!-- <el-table-column prop="IsSPA" label="Is.SPA" width="88" align="center" class-name="custom-column-header">
          <template slot-scope="scope">
              <i :class="['custom-icon', scope.row.IsSPA ? 'el-icon-check' : 'el-icon-close']" :style="{ color: scope.row.IsSPA ? 'green' : 'red' }"></i>
          </template>
          <template v-slot:header>
              Is.SPA
              <el-tooltip class="item" effect="dark" content="Whether saddle point approximation(SPA) is converged or not" placement="top">
                  <i class="el-icon-question"></i>
              </el-tooltip>
          </template>
       </el-table-column> -->
        <el-table-column prop="alleles1" label="Sample" width="78" align="center" class-name="custom-column-header">
          <template v-slot="scope">
            <a-icon type="fund" theme="twoTone" 
            @click="fetchPdfSample(scope.row.Cancertype, scope.row.SNPepi)" 
            style="font-size: 2.0em; cursor: pointer; color: #AED4D4;" />
          </template>
        </el-table-column>
        <el-table-column prop="ORstatus" label="OR plot" width="82" align="center" class-name="custom-column-header">
          <template v-slot="scope">
            <a-icon type="bar-chart" theme="outlined"
              @click="fetchPdfOR(scope.row.Cancertype, scope.row.SNPepi, scope.row.ORstatus)" 
              :style="{ fontSize: '2.0em', cursor: 'pointer', color: scope.row.ORstatus ? 'blue' : 'grey' }"
            />
          </template>
        </el-table-column>
      </el-table>

      <el-dialog 
        :visible.sync="imageDialogVisibleSample" 
        :style="{ maxWidth: '700px', margin: '0 auto' }" 
        width="auto" 
        @close="handleCloseSample" 
        :close-on-click-modal="false" 
        :close-on-press-escape="true" 
        :modal-append-to-body="useModalAppendToBody"
      >
        <div style="display: flex; flex-direction: column; align-items: center; position: relative;" @click="handleCloseSample">
          <img 
            :src="imageUrl" 
            @click="handleCloseSample"
            style="width: 600px; height: 500px; object-fit: contain; cursor: pointer; position: relative; z-index: 2;" 
            alt="Image Preview"
          >
          <button 
            class="download-button"
            :class="{ 'clicked': downloadClickedSample }"
            @click.stop="handleDownloadSample"
            style="position: relative; z-index: 2; margin-top: 20px; font-size: 18px;"
          >
            Download
          </button>
        </div>
      </el-dialog>

      <el-dialog 
        :visible.sync="imageDialogVisibleOR" 
        :style="{ maxWidth: '700px', margin: '0 auto' }" 
        width="auto" 
        @close="handleCloseOR" 
        :close-on-click-modal="false" 
        :close-on-press-escape="true" 
        :modal-append-to-body="useModalAppendToBody"
      >
        <div style="display: flex; flex-direction: column; align-items: center; position: relative;" @click="handleCloseOR"> 
          <img 
            :src="imageUrl" 
            @click="handleCloseOR"
            style="width: 700px; height: 500px; object-fit: contain; cursor: pointer; position: relative; z-index: 2;" 
            alt="Image Preview"
          >
          <button 
            class="download-button"
            :class="{ 'clicked': downloadClickedOR }"
            @click.stop="handleDownloadOR"
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
            The epistasis associated with this SNP has not satisfied the criteria for sample filtration 
            <strong style="color: black;">sample filtration</strong> in the context of the current cancer phenotype.
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
  name: 'EpistasisSNP',
  data() {
    return {
      selectQueryType: 'SNP',
      selectCancerType:'Breast',
      pValueThreshold:'0.05',
      isBestSnpModalVisible: false,
      formattedRowDetails: [],
      queryTypes: [
        { id: '001', queryName: 'SNP' },
        { id: '002', queryName: 'SNP epistasis' },
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
          "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
          "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
          "Rectal", "Stomach", "Uterine"
      ],
      searchRecordNumber: {},
      QTLData: {
        SnpEpistasis: []
      },
      recordNumber: 0,
      showBlock: 'N',
      pValueThreshold: '',
      loading: false,
      selectCancerType: '',
      isClicked1: false,
      isClicked2: false,
      isClicked3: false,
      queryRsid1: '',
      queryRsid2: '',
      flag: 1,
      currentPage: 1,
      perPage: 8,
      rowHeight: 60,
      defaultQueryType: 'SNP',
      defaultCancerType: 'Breast',
      defaultPValueThreshold: '0.05',
      currentCancertype: '',
      currentSNP: '',
      currentSNPepi: '',
      imageDialogVisibleSample: false,
      imageDialogVisibleOR: false,
      imageUrl: '',
      downloadClickedSample: false,
      downloadClickedOR: false,
      useModalAppendToBody: false,
      showAlert: false,
      useModalAppendToBody: false,
      isFirstLoad: true 
    };
  },
  computed: {
    tableHeight() {
      return this.QTLData.SnpEpistasis.length < this.perPage
        ? this.rowHeight * this.QTLData.SnpEpistasis.length + 50
        : this.rowHeight * this.perPage + 50;
    },
  },
  methods: {
    setQueryRsid1(value) {
      this.queryRsid1 = value;
    },
    toggleClickStatus(clickIndex) {
      this['isClicked' + clickIndex] = !this['isClicked' + clickIndex];
    },
    handleClickAndSetQueryRsid1() {
      this.setQueryRsid1('rs12924101');
      this.toggleClickStatus(1);
      this.selectCancerType = 'Melanoma';
      this.pValueThreshold = '0.05';
    },
    handleClickAndSetQueryRsid2() {
      this.setQueryRsid1('rs6687430_rs17781327');
      this.toggleClickStatus(2);
      this.selectCancerType = 'Melanoma';
      this.pValueThreshold = '0.05';
    },
    handleClickAndSetQueryRsid3() {
      this.toggleClickStatus(2);
      this.selectCancerType = 'Colon';
      this.pValueThreshold = '0.05';
    },
    handleCloseSample() {
      this.imageDialogVisibleSample = false; 
      this.downloadClickedSample = false;
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl); 
        this.imageUrl = ''; 
      }
    },
    handleCloseOR() {
      this.imageDialogVisibleOR = false; 
      this.downloadClickedOR = false;
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl); 
        this.imageUrl = ''; 
      }
    },
    handleOutsideClick(event) {
      const dialogElementSample = this.$el.querySelector('.el-dialog__wrapper[aria-label="Sample"]');
      const dialogElementOR = this.$el.querySelector('.el-dialog__wrapper[aria-label="OR_plot"]');
      
      if (dialogElementSample && !dialogElementSample.contains(event.target)) {
        this.handleCloseSample();
      }
      
      if (dialogElementOR && !dialogElementOR.contains(event.target)) {
        this.handleCloseOR();
      }
    },
    handleClose() {
        this.imageDialogVisible = false; 
        this.downloadClicked = false;
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

        // Normalize the case for 'rs' and 'Affx-'
        const validPattern = /^(rs\d+|affx-\d+)(_(rs\d+|affx-\d+))?$/i;
        const trimmedValue = inputValue.trim().toLowerCase();

        if (!validPattern.test(trimmedValue)) {
            this.$message.error('Invalid input');
            return null;
        }

        if (trimmedValue.startsWith('rs')) {
            return trimmedValue;
        } else if (trimmedValue.startsWith('affx-')) {
            const parts = trimmedValue.split('_');
            const normalizedParts = parts.map(part => {
                if (part.startsWith('rs')) {
                    return part;
                } else if (part.startsWith('affx-')) {
                    return 'Affx-' + part.slice(5);
                }
                return part;
            });
            return normalizedParts.join('_');
        } else {
            return trimmedValue;
        }
    },
    normalizeAndTrimInput(input) {
      return input.replace(/\s+/g, ''); // 去除所有空格
    },
    changePage(newPage) {
      this.currentPage = newPage;
      this.submitForm();
    },
    // initData() {
    //   this.selectQueryType = this.defaultQueryType;
    //   this.selectCancerType = this.defaultCancerType;
    //   this.pValueThreshold = this.defaultPValueThreshold;
    //   this.submitForm(); // 调用submitForm方法发送请求
    // },
    initData() {
        // 自动请求一批数据
        if (this.isFirstLoad) {
            this.isFirstLoad = false;
            axios.get('api/SnpEpistasis', { params: { isFirstLoad: true, Type: true } })
                .then(response => {
                    this.QTLData.SnpEpistasis = response.data.SnpEpistasis_results;
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
      if (/^rs/i.test(trimmedValue)) {
        return 'rs' + trimmedValue.slice(2).toLowerCase();
      } else if (/^affx-/i.test(trimmedValue)) {
        return 'Affx-' + trimmedValue.slice(5);
      } else {
        return null; // 不符合格式，返回null
      }
    },
    submitForm() {
      this.showBlock = 'Y';
      this.queryRsid1 = this.normalizeAndTrimInput(this.queryRsid1);
      this.queryRsid2 = this.normalizeAndTrimInput(this.queryRsid2);
      let queryParams = {
        selectQueryType: this.selectQueryType || 'SNP',
        selectCancerType: this.selectCancerType || 'All',
        currentPage: this.currentPage,
        perPage: this.perPage,
        pValueThreshold: this.pValueThreshold,
        isFirstLoad: false
      };

      if (this.selectQueryType === 'SNP') {
        if (!this.isValidInput(this.queryRsid1) || this.normalizeInput(this.queryRsid1) === null) {
          this.$alert('Invalid input', 'Error', {
            confirmButtonText: 'OK',
            callback: () => {
              this.QTLData.SnpEpistasis = [];
              this.recordNumber = 0;
            }
          });
          return;
        }
        queryParams.queryRsid1 = this.normalizeInput(this.queryRsid1);
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.pValueThreshold = this.pValueThreshold;
      } else if (this.selectQueryType === 'SNP epistasis') {
        if (!this.isValidInput(this.queryRsid1) || this.normalizeInput(this.queryRsid1) === null) {
          this.$alert('Invalid input', 'Error', {
            confirmButtonText: 'OK',
            callback: () => {
              this.QTLData.SnpEpistasis = [];
              this.recordNumber = 0;
            }
          });
          return;
        }
        queryParams.queryRsid1 = this.normalizeInput(this.queryRsid1);
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.pValueThreshold = this.pValueThreshold;
      } else if (this.selectQueryType === 'Cancer type and P-value') {
        queryParams.selectCancerType = this.selectCancerType;
        queryParams.pValueThreshold = this.pValueThreshold;
      }

      if (queryParams.queryRsid1 === null) {
        this.QTLData.SnpEpistasis = []; 
        this.recordNumber = 0;
        this.loading = false;
        return; 
      }

      axios.get('api/SnpEpistasis', { params: queryParams })
        .then(response => {
          this.QTLData.SnpEpistasis = response.data.SnpEpistasis_results;
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
      this.queryRsid1 = '';
      this.queryRsid2 = '';
      this.pValueThreshold = '';
      this.isOrange1 = false;
    },
    currentChange(page) {
      this.currentPage = page;
      this.submitForm();
    },
//     downloadCSV() {
//     if (!Array.isArray(this.QTLData.SnpEpistasis) || this.QTLData.SnpEpistasis.length === 0) {
//         this.$message.error('No data available for download');
//         return;
//     }

//     // 定义需要导出的列
//     const headers = ['Cancer', 'SNP Epistasis', 'Odds ratio', 'STAT', 'P-value', 'Best SNP', 'P-saige'];
//     const rows = this.QTLData.SnpEpistasis.map(item => [
//         item.Cancertype,
//         item.SNP_epi,
//         item.OR_INT !== undefined ? item.OR_INT.toFixed(2) : '',
//         item.STAT !== undefined ? item.STAT.toFixed(2) : '',
//         item.P !== undefined ? item.P.toExponential(2) : '',
//         item.Best_snp,
//         item.saige_p !== undefined ? (item.saige_p === 0 ? '0' : item.saige_p.toExponential(2)) : ''
//     ]);

//     // 创建CSV内容
//     let csvContent = "data:text/csv;charset=utf-8,"
//         + headers.join(",") + "\n"
//         + rows.map(e => e.join(",")).join("\n");

//     // 创建下载链接
//     const encodedUri = encodeURI(csvContent);
//     const link = document.createElement("a");

//     // 生成文件名
//     const cancertype = this.selectCancerType || '';
//     const snpepi = this.queryRsid1 || ''; 
//     const pValueThreshold = this.pValueThreshold || '';

//     const fileNameParts = [cancertype, snpepi, pValueThreshold];
//     const fileName = fileNameParts.filter(part => part !== '').join('_') + ".csv";

//     link.setAttribute("href", encodedUri);
//     link.setAttribute("download", fileName);
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
// },
    downloadCSV() {
        if (!Array.isArray(this.QTLData.SnpEpistasis) || this.QTLData.SnpEpistasis.length === 0) {
            this.$message.error('No data available for download');
            return;
        }

        // 定义需要导出的列，排除画图模块数据
        const headers = ['Cancer', 'SNP epistasis', 'Odds ratio', 'STAT', 'P-value', 'Best SNP', 'P-saige'];
        const rows = this.QTLData.SnpEpistasis.map(item => [
            item.Cancertype,
            item.SNP_epi,
            item.OR_INT !== undefined ? item.OR_INT.toFixed(2) : '',
            item.STAT !== undefined ? item.STAT.toFixed(2) : '',
            item.P !== undefined ? item.P.toExponential(2) : '',
            item.Best_snp,
            item.saige_p !== undefined ? (item.saige_p === 0 ? '0' : item.saige_p.toExponential(2)) : ''
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
        const snpepi = this.queryRsid1 || ''; 
        const pValueThreshold = this.pValueThreshold || '';

        const fileNameParts = [cancertype, snpepi, pValueThreshold];
        const fileName = fileNameParts.filter(part => part !== '').join('_') + ".csv";

        link.setAttribute("href", encodedUri);
        link.setAttribute("download", fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
    handleDownloadOR() {
        this.downloadClickedOR = true; 
        this.ORdownloadPdf();
    },
    handleDownloadSample() {
        this.downloadClickedSample = true; 
        this.SampledownloadPdf();
    },
    fetchPdfSample(Cancertype, SNPepi) {
      this.currentCancertype = Cancertype;
      this.currentSNPepi = SNPepi;
      axios.get(`api/SnpEpistasisSamplegetPdf`, {
        params: {
          Cancertype: encodeURIComponent(Cancertype),
          SNPepi: encodeURIComponent(SNPepi)
        },
        responseType: 'blob'
      })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        this.imageUrl = imageUrl;
        this.imageDialogVisibleSample = true;
      })
      .catch(error => {
        console.error('Error fetching image:', error);
        this.$alert(
          '<strong style="color: blue;">注意：</strong> ' +
          '没有通过样本过滤', {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '确定',
          }
        ).catch(() => {}); // Ensure the alert can be closed by clicking anywhere
      });
    },
    fetchPdfOR(Cancertype, SNPepi, ORstatus) {
      console.log('fetchPdfOR called'); // 调试日志
      if (!ORstatus) {
        console.log('ORstatus is false, setting showAlert to true'); // 调试日志
        this.showAlert = true;
        console.log('showAlert is now', this.showAlert); // 确认 showAlert 值被设置
        return;
      }
      this.currentCancertype = Cancertype;
      this.currentSNPepi = SNPepi;
      axios.get(`api/SnpEpistasisORgetPdf`, {
        params: {
          Cancertype: encodeURIComponent(Cancertype),
          SNPepi: encodeURIComponent(SNPepi)
        },
        responseType: 'blob'
      })
      .then(response => {
        const imageUrl = URL.createObjectURL(response.data);
        this.imageUrl = imageUrl;
        this.imageDialogVisibleOR = true;
      })
      .catch(error => {
        console.error('Error fetching image:', error);
        this.showAlert = true;
        console.log('showAlert is now', this.showAlert); // 确认 showAlert 值被设置
      });
    },
    closeAlert() {
        console.log('closeAlert called');
        this.showAlert = false;
    },
    stopPropagation(event) {
        event.stopPropagation();
    },
    SampledownloadPdf() {
      const cancertype = this.currentCancertype;
      const snpEpi = this.currentSNPepi;
      axios.get(`api/SnpEpistasisSampledownloadPdf`, {
        params: {
          Cancertype: encodeURIComponent(cancertype),
          SNPepi: encodeURIComponent(snpEpi)
        },
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const fileName = `${cancertype}_${snpEpi}.pdf`;
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error downloading PDF:', error);
        this.downloadClickedSample = false; 
      });
    },
    ORdownloadPdf() {
      const cancertype = this.currentCancertype;
      const snpEpi = this.currentSNPepi;
      axios.get(`api/SnpEpistasisORdownloadPdf`, {
        params: {
          Cancertype: encodeURIComponent(cancertype),
          SNPepi: encodeURIComponent(snpEpi)
        },
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const fileName = `${cancertype}_${snpEpi}.pdf`;
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error downloading PDF:', error);
        this.downloadClickedOR = false;
        this.$alert('<strong style="color: blue;">注意：</strong> <strong style="color: black;">没有通过样本过滤</strong>', {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '确定',
        });
      });
    }
  },
  mounted() {
    this.initData();
    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleOutsideClick);
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
    margin: 0 auto; /* 确保内容在页面中居中 */
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
  margin-top: 10px;
  background-color: #FA8072;
  font-size: 17px;
  border-radius: 4px;
  border-color: #FA8072;
}

.submit-button:hover, 
.submit-button:focus, 
.submit-button:active {
  background-color: #FA8072;
  border-color: #FA8072;
}

.cancel-button {
  margin-top: 10px;
  background-color: #77acf1;
  font-size: 17px;
  border-radius: 4px;
  border-color: #77acf1;
  margin: 5px 0 5px 0;
}

.cancel-button:hover, 
.cancel-button:focus, 
.cancel-button:active {
  background-color: #77acf1;
  border-color: #77acf1;
}
body {
    font-family: 'Arial', sans-serif;
}
.box-card {
    margin: 5px 0;
    padding: 10px;
}
.custom-row {
    margin-top: -10px; /* 例如，这里设置为负值可以让内容更靠近顶部，根据需要调整 */
}
.card-title {
    font-size: 19px;
    font-weight: bold;
    color: #337ab7;
    margin: 0;
    padding-top: 20px; /* 如果需要进一步调整标题与顶部的距离，可以增加这里的值 */
}
.card-description {
    font-size: 15px;
    color: #333;
    margin-top: 5px; /* 根据需要调整描述文本与标题的间距 */
    font-family: 'Helvetica';
}
.text {
    padding: 10px;
    background-color: #D1C6E0;
    font-size: 17px;
    border-radius: 4px;
    margin: 5px 0 5px 0;
}
.submit-button {
    margin-top: 10px;
    background-color: #FA8072;
    font-size: 17px;
    border-radius: 4px;
    margin: 5px 0 5px 0;
}
.orange-text {
    color: orange;
}
.place-input {
    font-size: 17px;
    font-family: 'Helvetica';
}
.custom-select-input {
    font-size: 17px; /* 您希望的字体大小 */
}
::v-deep(.el-select .el-input__inner) {
    font-size: 17px; /* Adjust the font size as needed */
}

.cancer-type-select ::v-deep .el-input__inner {
    font-size: 17px; /* Adjust the font size as needed */
}

.p-value-select ::v-deep .el-input__inner {
    font-size: 17px; /* Adjust the font size as needed */
}

.query-type-select {
    z-index: 2000; 
}
/deep/ .el-select .el-input__inner::placeholder {
    font-size: 17px; 
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
.el-dialog {
  max-width: 400px;
  width: 30%;
}
.el-table {
  width: 100%;
  table-layout: fixed;
}
.el-table th, .el-table td {
  white-space: normal;
  word-wrap: break-word;
}
.row-detail {
  display: flex;
  justify-content: space-between;
}
.align-left {
  text-align: left;
  flex: 1;
}
.bold-text {
  font-weight: bold;
}
.link-text {
  color: blue;
}
.bold-text {
  font-weight: bold;
}
.link-text {
  color: blue;
}

.custom-icon {
  font-size: 20px; /* 放大图标 */
  font-weight: bold; /* 加粗图标 */
}



.row-detail {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
}

.bold-text {
    font-weight: bold;
    flex: 1;
}

.align-left {
    text-align: left;
    flex: 2;
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
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  z-index: 2000; /* 确保弹框在前面 */
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
.tooltip-large-font .el-tooltip__popper {
  font-size: 20px !important; 
}

.submit-button, 
.cancel-button, 
.text-black, 
.text-orange, 
.custom-select-input, 
.cancer-type-select ::v-deep .el-input__inner, 
.p-value-select ::v-deep .el-input__inner, 
.download-button .el-icon-download {
    font-family: 'Helvetica';
}
body {
    font-family: 'Helvetica', sans-serif;
}

.box-card, 
.custom-row, 
.card-title, 
.text, 
.orange-text, 
.el-button--primary, 
.el-tooltip__popper, 
.custom-column-header, 
.el-table, 
.el-table th, 
.el-table td, 
.row-detail, 
.bold-text, 
.link-text, 
.custom-icon {
    font-family: 'Helvetica';
}
</style>
