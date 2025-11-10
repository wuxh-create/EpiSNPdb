<template>
    <div class="content-container">
        <!-- 查询模块 -->
        <el-card class="box-card">
            <el-row class="custom-row" :style="{ marginBottom: '15px' }">
                <el-col :span="24">
                    <p class="card-description" style="font-size: 18px; line-height: 1.7;font-family: 'Helvetica';">
                      This page provides the <span style="color: red; font-weight: bold;">annotation</span> of epiSNPs, such as SNP position, genomic function,  amino acidchange from ANNOVAR; coexpression, textmining_transferred, combined_score from STRING.
                    </p>
                </el-col>
            </el-row>
  
            <!-- search methods -->
            <div>
                <el-row :gutter="20" type="flex" justify="center">
                    <!-- Query type select -->
                    <el-col :span="5">
                        <span class="input-label">Query type:</span>
                        <el-select v-model="selectQueryType" placeholder="Query type" class="place-input query-type-select" style="width: 100%; z-index: 1000;">
                            <el-option v-for="query in queryTypes" :key="query.id" :value="query.queryName">
                                <span style="float: left">{{ query.queryName }}</span>
                            </el-option>
                        </el-select>
                    </el-col>
                    <!-- Cancer type select -->
                    <el-col :span="5">
                        <span class="input-label">Cancer type:</span>
                        <el-select v-model="selectCancerType" placeholder="Cancer type" class="place-input cancer-type-select" style="width: 100%;">
                            <el-option v-for="cancer in cancerType" :key="cancer.id" :value="cancer.cancerName">
                                <span style="float: left">{{ cancer.cancerName }}</span>
                                <span style="float: right">(N={{ cancer.sampleNumber }})</span>
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="5" v-if="selectQueryType === 'Cancer type'">
                        <span class="input-label">Select Loci:</span>
                        <el-select v-model="selectLociType" placeholder="Select type" class="place-input loci-type-select" style="width: 100%;font-size: 17px;">
                            <el-option label="SNP" value="SNP"></el-option>
                            <el-option label="SNP epistasis" value="SNP epistasis"></el-option>
                        </el-select>
                        <span :class="{ 'text-black': !isClickedDefault, 'text-orange': isClickedDefault }" @click="handleClickAndSetDefaultLociType" style="font-size: 16px;">e.g., SNP epistasis</span>
                    </el-col>
                    <!-- SNP or SNP Epistasis input based on query type -->
                    <el-col :span="5" v-if="selectQueryType === 'SNP'">
                        <span class="input-label">SNP:</span>
                        <el-input v-model="queryRsid1" placeholder="SNP" class="place-input" style="width: 100%;"></el-input>
                        <span :class="{ 'text-black': !isClicked1, 'text-orange': isClicked1 }" @click="handleClickAndSetQueryRsid1" style="font-size: 16px;">e.g., rs2274911</span>
                    </el-col>
                    <el-col :span="5" v-if="selectQueryType === 'SNP epistasis'">
                        <span class="input-label">SNP epistasis:</span>
                        <el-input v-model="queryRsid1" placeholder="SNP epistasis" class="place-input" style="width: 100%;"></el-input>
                        <span :class="{ 'text-black': !isClicked2, 'text-orange': isClicked2 }" @click="handleClickAndSetQueryRsid2" style="font-size: 16px;">e.g., rs6500437_rs7195066</span>
                    </el-col>
                    <!-- P-value filter select -->
                    <el-col :span="5">
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
  
            <!-- button -->
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
  
            <el-table :data="QTLData.SnpEpistasis" style="width: 100%;" empty-text="No results found for your query">
                  <el-table-column
                      prop="Cancertype"
                      label="Cancer"
                      width="115"
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
  
                  <template v-for="column in tableColumns">
                      <el-table-column 
                          v-if="column.prop === 'SNP' || column.prop === 'SNP_epi'" 
                          :key="column.prop" 
                          :prop="column.prop" 
                          :label="column.label" 
                          :width="column.width" 
                          align="center" 
                          class="custom-column-header"
                          show-overflow-tooltip>
                          <template slot-scope="scope">
                              <span v-if="column.prop === 'SNP'">
                                  {{ scope.row[column.prop] }}
                                  <a :href="'https://www.ncbi.nlm.nih.gov/snp/' + scope.row[column.prop]" target="_blank">
                                      <i class="el-icon-zoom-in" style="color: #FF7C43; font-size: 1.2em;"></i>
                                  </a>
                              </span>
                              <span v-else-if="column.prop === 'SNP_epi'">
                                  <template v-for="(snp, index) in scope.row[column.prop].split('_')">
                                      <span :key="index">
                                          {{ snp }}
                                          <a :href="'https://www.ncbi.nlm.nih.gov/snp/' + snp" target="_blank">
                                              <i class="el-icon-zoom-in" style="color: #FF7C43; font-size: 1.2em;"></i>
                                          </a>
                                          <span v-if="index === 0">_</span>
                                      </span>
                                  </template>
                              </span>
                          </template>
                      </el-table-column>
                      
                      <el-table-column 
                          v-else
                          :key="column.prop" 
                          :prop="column.prop" 
                          :label="column.label" 
                          :width="column.width" 
                          align="center" 
                          class="custom-column-header"
                          show-overflow-tooltip>
                          <template slot-scope="scope">
                              <span v-if="['FuncrefGene', 'GenerefGene', 'ExonicFuncrefGene', 'AAChangerefGene', 'FuncrefGene1', 'GenerefGene1', 'ExonicFuncrefGene1', 'AAChangerefGene1', 'FuncrefGene2', 'GenerefGene2', 'ExonicFuncrefGene2', 'AAChangerefGene2'].includes(column.prop)">
                                  <span v-html="scope.row[column.prop] === 'NA' || scope.row[column.prop] === null || scope.row[column.prop] === undefined ? '&#8203;<i class=\'el-icon-minus\' style=\'color: #FA8072;\'></i>' : scope.row[column.prop]"></span>
                              </span>
                              <span v-else-if="column.prop === 'coexpression' || column.prop === 'textmining_transferred' || column.prop === 'combined_score'">
                                  <span v-if="scope.row[column.prop] === 'NA' || scope.row[column.prop] === null || scope.row[column.prop] === undefined">
                                      <i class="el-icon-minus" style="color: #FA8072; font-weight: bold;"></i>
                                  </span>
                                  <span v-else>
                                      {{ scope.row[column.prop] }}
                                  </span>
                              </span>
                              <span v-else>
                                  {{ scope.row[column.prop] }}
                              </span>
                          </template>
                      </el-table-column>
                  </template>
              </el-table>
  
        </el-card>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default {
  name: 'EpiSNPAnnotation',
  data() {
    return {
      selectQueryType: '',
      isBestSnpModalVisible: false,
      formattedRowDetails: [],
      queryTypes: [
        { id: '001', queryName: 'SNP' },
        { id: '002', queryName: 'SNP epistasis' },
        { id: '003', queryName: 'Cancer type' }
      ],
      cancerTypes: [
          "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
          "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
          "Rectal", "Stomach", "Uterine"
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
        { id: '010', cancerName: 'Uterine', sampleNumber: '172157' },
        { id: '011', cancerName: 'Kidney', sampleNumber: '315750' },
        { id: '012', cancerName: 'Ovarian', sampleNumber: '171548' },
        { id: '013', cancerName: 'Pancreatic', sampleNumber: '315056' },
        { id: '014', cancerName: 'Esophagus', sampleNumber: '315022' },
        { id: '015', cancerName: 'Stomach', sampleNumber: '314676' },
        { id: '016', cancerName: 'Brain', sampleNumber: '314501' },
        { id: '017', cancerName: 'Liver', sampleNumber: '314490' }
      ],
      QTLData: {
        SnpEpistasis: []
      },
      recordNumber: 0,
      pValueThreshold: '',
      selectLociType:'',
      loading: false,
      selectCancerType: '',
      isClicked1: false,
      isClicked2: false,
      isClickedDefault: false,
      queryRsid1: '',
      currentPage: 1,
      perPage: 7,
      defaultQueryType: 'Cancer type',
      defaultCancerType: 'Breast',
      defaultPValueThreshold: '0.05',
      defaultselectLociType:'SNP epistasis',
      tableColumns: [],
      allData: []
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
      this.setQueryRsid1('rs2274911');
      this.toggleClickStatus(1);
      this.selectCancerType = 'Prostate';
      this.pValueThreshold = '0.05';
    },
    handleClickAndSetQueryRsid2() {
      this.setQueryRsid1('rs6500437_rs7195066');
      this.toggleClickStatus(2);
      this.selectCancerType = 'Melanoma';
      this.pValueThreshold = '0.05';
    },
    handleClickAndSetDefaultLociType() {
      this.selectLociType = 'SNP epistasis';
      this.selectCancerType = 'Esophagus';
      this.pValueThreshold = '0.05';
      this.isClickedDefault = !this.isClickedDefault;
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
    initData() {
      this.selectQueryType = this.defaultQueryType;
      this.selectCancerType = this.defaultCancerType;
      this.selectLociType = this.defaultselectLociType;
      this.pValueThreshold = this.defaultPValueThreshold;
      this.submitForm();
    },
    // 修复displayDataBasedOnModel方法 - 确保prop名称与数据库字段名称匹配
    displayDataBasedOnModel() {
        if (this.selectQueryType === 'SNP') {
            const displayColumns = [
                { prop: "SNP", label: "SNP", width: 140 },
                { prop: "alleles", label: "Alleles(A/a)", width: 115 },
                { prop: "FuncrefGene", label: "Func.refGene", width: 125 },
                { prop: "GenerefGene", label: "Gene.refGene", width: 125 },
                { prop: "ExonicFuncrefGene", label: "ExonicFunc.refGene", width: 170 },
                { prop: "AAChangerefGene", label: "AAChange.refGene", width: 210 }
            ];
            this.tableColumns = displayColumns;
        } else if (this.selectQueryType === 'SNP epistasis') {
            const displayColumns = [
                { prop: "SNP_epi", label: "SNP_epi", width: 245 },
                { prop: "FuncrefGene1", label: "Func.refGene1", width: 150 },
                { prop: "GenerefGene1", label: "Gene.refGene1", width: 150 },
                { prop: "ExonicFuncrefGene1", label: "ExonicFunc.refGene1", width: 175 },
                { prop: "AAChangerefGene1", label: "AAChange.refGene1", width: 168 },
                { prop: "FuncrefGene2", label: "Func.refGene2", width: 150 },
                { prop: "GenerefGene2", label: "Gene.refGene2", width: 150 },
                { prop: "ExonicFuncrefGene2", label: "ExonicFunc.refGene2", width: 175 },
                { prop: "AAChangerefGene2", label: "AAChange.refGene2", width: 170 },
                { prop: "coexpression", label: "coexpression", width: 150 },
                { prop: "textmining_transferred", label: "textmining_transferred", width: 190 },
                { prop: "combined_score", label: "combined_score", width: 150 }
            ];
            this.tableColumns = displayColumns;
        } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
            const displayColumns = [
                { prop: "SNP", label: "SNP", width: 140 },
                { prop: "alleles", label: "Alleles(A/a)", width: 115 },
                { prop: "FuncrefGene", label: "Func.refGene", width: 130 },
                { prop: "GenerefGene", label: "Gene.refGene", width: 130 },
                { prop: "ExonicFuncrefGene", label: "ExonicFunc.refGene", width: 170 },
                { prop: "AAChangerefGene", label: "AAChange.refGene", width: 210 }
            ];
            this.tableColumns = displayColumns;
        } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
            const displayColumns = [
                { prop: "SNP_epi", label: "SNP epistasis", width: 245 },
                { prop: "FuncrefGene1", label: "Func.refGene1", width: 150 },
                { prop: "GenerefGene1", label: "Gene.refGene1", width: 150 },
                { prop: "ExonicFuncrefGene1", label: "ExonicFunc.refGene1", width: 175 },
                { prop: "AAChangerefGene1", label: "AAChange.refGene1", width: 168 },
                { prop: "FuncrefGene2", label: "Func.refGene2", width: 150 },
                { prop: "GenerefGene2", label: "Gene.refGene2", width: 150 },
                { prop: "ExonicFuncrefGene2", label: "ExonicFunc.refGene2", width: 175 },
                { prop: "AAChangerefGene2", label: "AAChange.refGene2", width: 170 },
                { prop: "coexpression", label: "coexpression", width: 150 },
                { prop: "textmining_transferred", label: "textmining_transferred", width: 185 },
                { prop: "combined_score", label: "combined_score", width: 150 }
            ];
            this.tableColumns = displayColumns;
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
        this.loading = true;
        this.queryRsid1 = this.normalizeAndTrimInput(this.queryRsid1);
        let queryParams = {
            selectQueryType: this.selectQueryType || 'SNP',
            selectCancerType: this.selectCancerType || 'All',
            currentPage: this.currentPage,
            perPage: this.perPage,
            pValueThreshold: this.pValueThreshold
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
            queryParams.pValueThreshold = this.pValueThreshold;
        } else if (this.selectQueryType === 'Cancer type') {
            queryParams.selectCancerType = this.selectCancerType;
            queryParams.selectLociType = this.selectLociType;
            queryParams.pValueThreshold = this.pValueThreshold;
        }

        if (queryParams.queryRsid1 === null) {
            this.QTLData.SnpEpistasis = [];
            this.recordNumber = 0;
            this.loading = false;
            return;
        }

        let apiUrl = '';

        if (this.selectQueryType === 'SNP') {
            apiUrl = 'api/SnpAnnovar';
        } else if (this.selectQueryType === 'SNP epistasis') {
            apiUrl = 'api/SnpEpistasisAnnovar';
        } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
            apiUrl = 'api/SnpCancerTypeAnnovar';
        } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
            apiUrl = 'api/SnpEpistasisCancerTypeAnnovar';
        }

        axios.post(apiUrl, queryParams)
        .then(response => {
            if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
                this.QTLData.SnpEpistasis = response.data.SnpCancerTypeAnnovarResult;
            } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
                this.QTLData.SnpEpistasis = response.data.SnpEpistasisCancerTypeAnnovarResult;
            } else {
                this.QTLData.SnpEpistasis = response.data.SnpEpistasisAnnovarResult || response.data.SnpAnnovarResult;
            }
            this.allData = this.QTLData.SnpEpistasis; // 存储当前页面的所有数据
            this.recordNumber = response.data.total;
            this.displayDataBasedOnModel();
            this.loading = false;
        })
        .catch(error => {
            if (error.response) {
                this.errorMessage = `Request failed: ${error.response.data}, Status code: ${error.response.status}, Response headers: ${JSON.stringify(error.response.headers)}`;
            } else if (error.request) {
                this.errorMessage = "No response received";
            } else {
                this.errorMessage = `Error: ${error.message}`;
            }
            this.loading = false;
        });
        },
    clearInput() {
      this.selectQueryType = '';
      this.selectCancerType = '';
      this.queryRsid1 = '';
      this.pValueThreshold = '';
      this.selectLociType = '';
    },
    currentChange(page) {
      this.currentPage = page;
      this.submitForm();
    },
    downloadCSV() {
        if (!Array.isArray(this.allData) || !this.allData.length) {
        this.$alert('No data to download', 'Warning', {
            confirmButtonText: 'OK'
        });
        return;
        }

        const columns = this.tableColumns.map(col => col.label);
        const rows = this.allData.map(row => 
        this.tableColumns.map(col => row[col.prop] !== undefined ? row[col.prop] : '')
        );

        const csvContent = [columns, ...rows].map(e => e.join(",")).join("\n");

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const filename = `${this.selectQueryType}_${this.selectCancerType}_${this.queryRsid1}_${this.pValueThreshold}.csv`;

        if (window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
        } else {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        }
    }
  },
  mounted() {
    this.initData();
    console.log(this.QTLData.SnpEpistasis);
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
  }
  .content-container {
  width: 1140px;
  margin: 0 auto;
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
  .box-card {
  margin: 5px 0;
  padding: 10px;
  }
  .custom-row {
  margin-top: -10px;
  }
  .card-title {
  font-size: 19px;
  font-weight: bold;
  color: #337ab7;
  margin: 0;
  padding-top: 20px;
  }
  ::v-deep .el-table thead th {
  color: #2d4059 !important;
  font-family: 'Helvetica';
  font-weight: bold;
}
  .card-description {
  font-size: 15px;
  color: #333;
  margin-top: 5px;
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
  }
  
  .cancel-button:hover, 
  .cancel-button:focus, 
  .cancel-button:active {
    background-color: #77acf1;
    border-color: #77acf1;
  }
  .place-input {
  font-size: 17px;
  font-family: 'Helvetica';
  }
  .query-type-select {
    font-size: 17px;
    font-family: 'Helvetica';
    z-index: 2000;
  }
  .download-button .el-icon-download {
    font-size: 16px; 
    font-weight: bold; 
    color: blue; 
  }
  .query-type-select {
  z-index: 2000;
  }
  .download-button .el-icon-download {
    font-size: 16px; /* Increase icon size */
    font-weight: bold; /* Bold icon */
    color: blue; /* Set icon color */
  }
  .el-button--primary {
    border-color: transparent; /* 移除按钮边框 */
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
  .custom-icon {
  font-size: 20px;
  font-weight: bold;
  }
  
  .content-container, 
  .card-description, 
  .input-label, 
  .place-input, 
  .submit-button, 
  .cancel-button, 
  .text-black, 
  .text-orange, 
  .custom-select-input, 
  .cancer-type-select ::v-deep .el-input__inner, 
  .p-value-select ::v-deep .el-input__inner, 
  .download-button .el-icon-download, 
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
  .query-type-select ::v-deep .el-input__inner {
    font-size: 17px; 
    font-family: 'Helvetica';
}

  .cancer-type-select ::v-deep .el-input__inner {
        font-size: 17px; 
        font-family: 'Helvetica';
    }
.loci-type-select ::v-deep .el-input__inner {
    font-size: 17px; 
    font-family: 'Helvetica';
}
    .p-value-select ::v-deep .el-input__inner {
        font-size: 17px; 
        font-family: 'Helvetica';
    }

    /deep/ .el-select .el-input__inner::placeholder {
        font-size: 17px;
        font-family: 'Helvetica';
    }
  .el-table .el-table__cell {
      white-space: nowrap;       /* 防止换行 */
      overflow: hidden;          /* 隐藏超出部分 */
      text-overflow: ellipsis;   /* 显示省略号 */
      cursor: pointer;           /* 鼠标悬停时显示指针 */
  }
  
  .el-tooltip__popper {
      white-space: normal;       /* 使工具提示中的文本自动换行 */
      max-width: 300px;          /* 设置工具提示的最大宽度 */
  }
  
  
  </style>