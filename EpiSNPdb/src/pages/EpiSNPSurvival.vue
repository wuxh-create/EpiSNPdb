<template>
  <div class="content-container">
    <!-- 查询模块 -->
    <el-card class="box-card">
      <el-row class="custom-row" :style="{ marginBottom: '15px' }">
        <el-col :span="24">
            <p class="card-description" style="font-size: 18px; line-height: 1.7; font-family: 'Helvetica';">
              This module provides survival results of epiSNPs. We have conducted KM analysis to identify survival related epiSNPs using additive, dominant, and recessive models, respectively. And <span style="color: blue; font-weight: bold;">15,034</span> significant SNP epistases with a P-value < 1e-5 have been found.
            </p>
        </el-col>
      </el-row>

      <div>
        <el-row :gutter="20" type="flex" justify="center">
          <!-- Query type select -->
          <el-col :span="5">
            <span class="input-label">Query type:</span>
            <el-select v-model="selectQueryType" placeholder="Query Type" class="place-input query-type-select" style="width: 100%; font-size: 17px; z-index: 1000;">
              <el-option v-for="query in queryTypes" :key="query.id" :value="query.queryName">
                <span style="float: left">{{ query.queryName }}</span>
              </el-option>
            </el-select>
          </el-col>
          <!-- Cancer type select -->
          <el-col :span="5">
            <span class="input-label">Cancer type:</span>
            <el-select v-model="selectCancerType" placeholder="Cancer type" class="place-input cancer-type-select" style="width: 100%; font-size: 17px;">
              <el-option v-for="cancer in cancerType" :key="cancer.id" :value="cancer.cancerName">
                <span style="float: left">{{ cancer.cancerName }}</span>
                <span style="float: right">(N={{ cancer.sampleNumber }})</span>
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="5" v-if="selectQueryType === 'Cancer type'">
            <span class="input-label">Select type:</span>
            <el-select v-model="selectLociType" placeholder="Select type" class="place-input loci-type-select" style="width: 100%; font-size: 17px;">
              <el-option label="SNP" value="SNP"></el-option>
              <el-option label="SNP epistasis" value="SNP epistasis"></el-option>
            </el-select>
            <span :class="{ 'text-black': !isClickedDefault, 'text-orange': isClickedDefault }" @click="handleClickAndSetDefaultLociType" style="font-size: 16px;">e.g., SNP epistasis</span>
          </el-col>
          <!-- SNP or SNP Epistasis input based on query type -->
          <el-col :span="5" v-if="selectQueryType === 'SNP'">
            <span class="input-label">SNP:</span>
            <el-input v-model="queryRsid1" placeholder="SNP" class="place-input" style="width: 100%; font-size: 17px;"></el-input>
            <span :class="{ 'text-black': !isClicked1, 'text-orange': isClicked1 }" @click="handleClickAndSetQueryRsid1" style="font-size: 16px;">e.g., rs944857</span>
          </el-col>
          <el-col :span="5" v-if="selectQueryType === 'SNP epistasis'">
            <span class="input-label">SNP epistasis:</span>
            <el-input v-model="queryRsid1" placeholder="SNP epistasis" class="place-input" style="width: 100%; font-size: 17px;"></el-input>
            <span :class="{ 'text-black': !isClicked2, 'text-orange': isClicked2 }" @click="handleClickAndSetQueryRsid2" style="font-size: 15px;">e.g., rs12407887_rs118047432</span>
          </el-col>
          <!-- Model select -->
          <el-col :span="5">
            <span class="input-label">Model select:</span>
            <el-select v-model="ModelSelect" placeholder="Model" class="place-input p-value-select" style="width: 100%; font-size: 17px;">
              <el-option label="Dominant" value="Dominant"></el-option>
              <el-option label="Additive" value="Additive"></el-option>
              <el-option label="Recessive" value="Recessive"></el-option>
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
        <!-- <el-pagination :hide-on-single-page="true" :total="recordNumber" :page-size="perPage" :current-page.sync="currentPage" @current-change="currentChange" layout="prev, pager, next"></el-pagination> -->
        <div style="margin-bottom: 0px; text-align: right; margin-right: 20px;">
          <el-button type="primary" :circle="true" @click="downloadCSV" style="font-size: 35px; padding: 0; background-color: white; color: blue; font-weight: bold;">
            <i class="el-icon-download"></i>
          </el-button>
        </div>
      </div>

      <el-table :data="QTLData.SnpEpistasis" style="width: 100%;" empty-text="No results found for your query">
        <el-table-column
          prop="alleles1"
          label="Plot"
          width="60"
          align="center"
          class="custom-column-header"
        >
          <template v-slot="scope">
            <a-icon 
              type="line-chart" 
              theme="outlined"
              @click="fetchPdf(scope.row.Cancertype, scope.row.Model, scope.row.SNP_epi || scope.row.SNP)"
              style="font-size: 2.1em; cursor: pointer; color: blue;"
            />
          </template>
        </el-table-column>

        <el-table-column
          v-for="column in tableColumns"
          :key="column.prop"
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          align="center"
          class="custom-column-header"
        >
          <template v-slot="scope">
            <span v-if="column.prop === 'Cancertype'" :style="{ color: 'red',fontSize: '1.1em' }">
              {{ scope.row.Cancertype }}
            </span>
            <span v-else-if="column.prop === 'Model'" :style="{ color: 'orange',fontSize: '1.1em' }">
              {{ scope.row.Model }}
            </span>
            <span v-else-if="column.prop === 'SNP'">
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
            <span v-else-if="column.prop === 'P_Value'">
              {{ formatPValue(scope.row[column.prop]) }}
            </span>
            <span v-else-if="column.format === 'decimal'">
              {{ parseFloat(scope.row[column.prop]).toFixed(2) }}
            </span>
            <span v-else-if="column.format === 'scientific'">
              {{ parseFloat(scope.row[column.prop]).toExponential(2) }}
            </span>
            <span v-else>
              {{ scope.row[column.prop] }}
            </span>
          </template>
        </el-table-column>
      </el-table>


      <el-dialog :visible.sync="imageDialogVisible" :style="{ maxWidth: '560px', margin: '0 auto' }" width="auto" @close="handleClose" 
        :close-on-click-modal="false" :close-on-press-escape="true" :modal-append-to-body="false">
        <div style="text-align: center;" @click.stop>
          <img :src="imageUrl" @click="handleClose" style="max-width: 530px; max-height: 500px; object-fit: contain;cursor: pointer;" alt="Image Preview" >
          <button class="download-button"
                  :class="{ 'clicked': downloadClicked }"
                  @click.stop="handleDownload">
              Download
          </button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>


<script>
import axios from 'axios';

export default {
name: 'EpiSNPSurvival',
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
    ModelSelect: '',
    selectLociType:'',
    loading: false,
    selectCancerType: '',
    isClicked1: false,
    isClicked2: false,
    isClickedDefault: false,
    queryRsid1: '',
    currentPage: 1,
    perPage: 8,
    defaultQueryType: 'SNP',
    defaultCancerType: 'Breast',
    defaultModelSelect: 'Additive',
    defaultselectLociType:'',
    tableColumns: [],
    imageUrl: '',
    downloadClicked: false,
    imageDialogVisible: false,
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
  formatPValue(value) {
    if (parseFloat(value) === 0) {
      return '0';
    } else {
      return parseFloat(value).toExponential(2);
    }
  },
  setQueryRsid1(value) {
    this.queryRsid1 = value;
  },
  toggleClickStatus(clickIndex) {
    this['isClicked' + clickIndex] = !this['isClicked' + clickIndex];
  },
  handleClickAndSetQueryRsid1() {
    this.setQueryRsid1('rs944857');
    this.toggleClickStatus(1);
    this.selectCancerType = 'Melanoma';
    this.ModelSelect = 'Additive';
  },
  handleClickAndSetQueryRsid2() {
    this.setQueryRsid1('rs12407887_rs118047432');
    this.toggleClickStatus(2);
    this.selectCancerType = 'Kidney';
    this.ModelSelect = 'Dominant';
  },
  handleClickAndSetDefaultLociType() {
    this.selectLociType = 'SNP epistasis';
    this.selectCancerType = 'Breast';
    this.ModelSelect = 'Additive';
    this.isClickedDefault = !this.isClickedDefault;
  },
  valueCheck(inputValue) {
    const validPattern = /^[a-zA-Z0-9-_]+$/;
    if (!validPattern.test(inputValue)) {
      this.$alert('Invalid input', 'Error', {
        confirmButtonText: 'OK',
        callback: () => {
          this.QTLData.SnpEpistasis = [];
          this.recordNumber = 0;
        }
      });
      return null;
    } else {
      return inputValue.trim();
    }
  },
  changePage(newPage) {
    this.currentPage = newPage;
    this.submitForm();
  },
  initData() {
    this.selectQueryType = this.defaultQueryType;
    this.selectCancerType = this.defaultCancerType;
    this.selectLociType = this.defaultselectLociType;
    this.ModelSelect = this.defaultModelSelect;
    this.fetchInitialData(); 
  },
  displayDataBasedOnModel() {
      if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
          if (this.ModelSelect === 'Dominant') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 99 },
              { prop: "Model", label: "Model", width: 95 },
              { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
              { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
              { prop: "N", label: "N", width: 100 },
              { prop: "OS_Median_AABB", label: "OS_Median_AABB", width: 158,format: 'decimal' },
              { prop: "OS_Median_AABb_and_AAbb", label: "OS_Median_AABb_and_AAbb", width: 250,format: 'decimal' },
              { prop: "OS_Median_AaBB_and_aaBB", label: "OS_Median_AaBB_and_aaBB", width: 250,format: 'decimal' },
              { prop: "OS_Median_AaBb_Aabb_aaBb_and_aabb", label: "OS_Median_AaBb_Aabb_aaBb_and_aabb", width: 300,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          } else if (this.ModelSelect === 'Additive') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 99 },
              { prop: "Model", label: "Model", width: 90 },
              { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
              { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
              { prop: "N", label: "N", width: 100},
              { prop: "OS_Median_AABB", label: "OS_Median_AABB", width: 158,format: 'decimal' },
              { prop: "OS_Median_AABb", label: "OS_Median_AABb", width: 158,format: 'decimal' },
              { prop: "OS_Median_AAbb", label: "OS_Median_AAbb", width: 158,format: 'decimal' },
              { prop: "OS_Median_AaBB", label: "OS_Median_AaBB", width: 158,format: 'decimal' },
              { prop: "OS_Median_AaBb", label: "OS_Median_AaBb", width: 150,format: 'decimal' },
              { prop: "OS_Median_Aabb", label: "OS_Median_Aabb", width: 150,format: 'decimal' },
              { prop: "OS_Median_aaBB", label: "OS_Median_aaBB", width: 150,format: 'decimal' },
              { prop: "OS_Median_aaBb", label: "OS_Median_aaBb", width: 150,format: 'decimal' },
              { prop: "OS_Median_aabb", label: "OS_Median_aabb", width: 150,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          } else if (this.ModelSelect === 'Recessive') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 99 },
              { prop: "Model", label: "Model", width: 95 },
              { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
              { prop: "P_Value", label: "P-value", width: 120,format: 'scientific'},
              { prop: "N", label: "N", width: 100 },
              { prop: "OS_Median_aabb", label: "OS_Median_aabb", width: 150,format: 'decimal'},
              { prop: "OS_Median_aaBB_and_aaBb", label: "OS_Median_aaBB_and_aaBb", width: 250,format: 'decimal' },
              { prop: "OS_Median_AAbb_and_Aabb", label: "OS_Median_AAbb_and_Aabb", width: 250,format: 'decimal'},
              { prop: "OS_Median_AABB_AABb_AaBB_and_AaBb", label: "OS_Median_AABB_AABb_AaBB_and_AaBb", width: 300,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          }
      } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
          if (this.ModelSelect === 'Dominant') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 100 },
              { prop: "Model", label: "Model", width: 90 },
              { prop: "SNP", label: "SNP", width: 160 },
              { prop: "P_Value", label: "P-value", width: 110,format: 'scientific'},
              { prop: "Sample_Size", label: "N", width: 90 },
              { prop: "OS_Median_AA", label: "OS_Median_AA", width: 165,format: 'decimal' },
              { prop: "OS_Median_Aa_aa", label: "OS_Median_Aa_aa", width: 155,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          } else if (this.ModelSelect === 'Additive') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 100 },
              { prop: "Model", label: "Model", width: 90 },
              { prop: "SNP", label: "SNP", width: 160 },
              { prop: "P_Value", label: "P-value", width: 110,format: 'scientific' },
              { prop: "Sample_Size", label: "N", width: 90 },
              { prop: "OS_Median_AA", label: "OS_Median_AA", width: 140,format: 'decimal' },
              { prop: "OS_Median_Aa", label: "OS_Median_Aa", width: 130,format: 'decimal' },
              { prop: "OS_Median_aa", label: "OS_Median_aa", width: 130,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          } else if (this.ModelSelect === 'Recessive') {
          const displayColumns = [
              { prop: "Cancertype", label: "Cancer", width: 100 },
              { prop: "Model", label: "Model", width: 80 },
              { prop: "SNP", label: "SNP", width: 160 },
              { prop: "P_Value", label: "P-value", width: 110,format: 'scientific' },
              { prop: "Sample_Size", label: "N", width: 100},
              { prop: "OS_Median_aa", label: "OS_Median_aa", width: 150,format: 'decimal' },
              { prop: "OS_Median_AA_Aa", label: "OS_Median_AA_Aa", width: 165,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
          }
      } else if (this.selectQueryType === 'SNP' && this.ModelSelect === 'Dominant') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 100 },
          { prop: "Model", label: "Model", width: 80 },
          { prop: "SNP", label: "SNP", width: 160 },
          { prop: "P_Value", label: "P-value", width: 110,format: 'scientific' },
          { prop: "Sample_Size", label: "N", width: 100 },
          { prop: "OS_Median_AA", label: "OS_Median_AA", width: 165,format: 'decimal' },
          { prop: "OS_Median_Aa_aa", label: "OS_Median_Aa_aa", width: 155,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
      } else if (this.selectQueryType === 'SNP' && this.ModelSelect === 'Additive') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 100 },
          { prop: "Model", label: "Model", width: 80 },
          { prop: "SNP", label: "SNP", width: 160 },
          { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
          { prop: "Sample_Size", label: "N", width: 100 },
          { prop: "OS_Median_AA", label: "OS_Median_AA", width: 165,format: 'decimal' },
          { prop: "OS_Median_Aa", label: "OS_Median_Aa", width: 150,format: 'decimal' },
          { prop: "OS_Median_aa", label: "OS_Median_aa", width: 150,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
      } else if (this.selectQueryType === 'SNP' && this.ModelSelect === 'Recessive') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 100 },
          { prop: "Model", label: "Model", width: 80 },
          { prop: "SNP", label: "SNP", width: 160 },
          { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
          { prop: "Sample_Size", label: "N", width: 100 },
          { prop: "OS_Median_aa", label: "OS_Median_aa", width: 150,format: 'decimal' },
          { prop: "OS_Median_AA_Aa", label: "OS_Median_AA_Aa", width: 160,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
      } else if (this.selectQueryType === 'SNP epistasis' && this.ModelSelect === 'Dominant') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 99 },
          { prop: "Model", label: "Model", width: 95 },
          { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
          { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
          { prop: "N", label: "N", width: 100 },
          { prop: "OS_Median_AABB", label: "OS_Median_AABB", width: 158,format: 'decimal' },
          { prop: "OS_Median_AABb_and_AAbb", label: "OS_Median_AABb_and_AAbb", width: 250,format: 'decimal' },
          { prop: "OS_Median_AaBB_and_aaBB", label: "OS_Median_AaBB_and_aaBB", width: 250,format: 'decimal' },
          { prop: "OS_Median_AaBb_Aabb_aaBb_and_aabb", label: "OS_Median_AaBb_Aabb_aaBb_and_aabb", width: 300,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
      } else if (this.selectQueryType === 'SNP epistasis' && this.ModelSelect === 'Additive') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 99 },
          { prop: "Model", label: "Model", width: 95 },
          { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
          { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
          { prop: "N", label: "N", width: 100 },
          { prop: "OS_Median_AABB", label: "OS_Median_AABB", width: 158,format: 'decimal' },
          { prop: "OS_Median_AABb", label: "OS_Median_AABb", width: 158,format: 'decimal' },
          { prop: "OS_Median_AAbb", label: "OS_Median_AAbb", width: 158,format: 'decimal' },
          { prop: "OS_Median_AaBB", label: "OS_Median_AaBB", width: 158,format: 'decimal' },
          { prop: "OS_Median_AaBb", label: "OS_Median_AaBb", width: 150,format: 'decimal' },
          { prop: "OS_Median_Aabb", label: "OS_Median_Aabb", width: 150,format: 'decimal' },
          { prop: "OS_Median_aaBB", label: "OS_Median_aaBB", width: 150,format: 'decimal' },
          { prop: "OS_Median_aaBb", label: "OS_Median_aaBb", width: 150,format: 'decimal' },
          { prop: "OS_Median_aabb", label: "OS_Median_aabb", width: 150,format: 'decimal' }
          ];
          this.tableColumns = displayColumns;
      } else if (this.selectQueryType === 'SNP epistasis' && this.ModelSelect === 'Recessive') {
          const displayColumns = [
          { prop: "Cancertype", label: "Cancer", width: 99 },
          { prop: "Model", label: "Model", width: 95 },
          { prop: "SNP_epi", label: "SNP epistasis", width: 250 },
          { prop: "P_Value", label: "P-value", width: 120,format: 'scientific' },
          { prop: "N", label: "N", width: 100 },
          { prop: "OS_Median_aabb", label: "OS_Median_aabb", width: 150,format: 'decimal' },
          { prop: "OS_Median_aaBB_and_aaBb", label: "OS_Median_aaBB_and_aaBb", width: 250,format: 'decimal'},
          { prop: "OS_Median_AAbb_and_Aabb", label: "OS_Median_AAbb_and_Aabb", width: 250,format: 'decimal'},
          { prop: "OS_Median_AABB_AABb_AaBB_and_AaBb", label: "OS_Median_AABB_AABb_AaBB_and_AaBb", width: 300,format: 'decimal'}
          ];
          this.tableColumns = displayColumns;
      }
  },
  fetchInitialData() {
    const initialParam = { Type: true }; // 初始化参数

    axios.post('api/SnpSurvival', initialParam)
      .then(response => {
        this.QTLData.SnpEpistasis = response.data.collection_SingleAdditiveSurvivalResult;
        this.recordNumber = response.data.total;
        this.displayDataBasedOnModel();
        this.loading = false;
      })
      .catch(error => {
        if (error.response) {
          console.log("请求失败", error.response.data);
          console.log("状态码:", error.response.status);
          console.log("响应头:", error.response.headers);
        } else if (error.request) {
          console.log("请求未收到响应:", error.request);
        } else {
          console.log('错误', error.message);
        }
        this.loading = false;
      });
  },
  submitForm() {
      this.loading = true;
      let sanitizedQueryRsid1 = this.queryRsid1.trim().replace(/\s+/g, '');

      const validSNPPattern = /^(rs|RS|Affx-|AFFX-)[0-9]+$/;
      const validEpistasisPattern = /^(rs|RS|Affx-|AFFX-)[0-9]+_(rs|RS|Affx-|AFFX-)[0-9]+$/;

      let queryParams = {
          queryType: this.selectQueryType,
          cancerType: this.selectCancerType,
          model: this.ModelSelect,
          page: this.currentPage,
          pageSize: this.perPage
      };

      let apiUrl = '';

      if (this.selectQueryType === 'SNP') {
          if (!validSNPPattern.test(sanitizedQueryRsid1)) {
              this.$alert('Invalid SNP input', 'Error', {
                  confirmButtonText: 'OK',
                  callback: () => {
                      this.QTLData.SnpEpistasis = [];
                      this.recordNumber = 0;
                  }
              });
              this.loading = false;
              return;
          }
          sanitizedQueryRsid1 = sanitizedQueryRsid1.toLowerCase().replace('rs', 'rs').replace('affx-', 'Affx-');
          queryParams.snp = sanitizedQueryRsid1;
          apiUrl = 'api/SnpSurvival';
      } else if (this.selectQueryType === 'SNP epistasis') {
          if (!validEpistasisPattern.test(sanitizedQueryRsid1)) {
              this.$alert('Invalid SNP epistasis input', 'Error', {
                  confirmButtonText: 'OK',
                  callback: () => {
                      this.QTLData.SnpEpistasis = [];
                      this.recordNumber = 0;
                  }
              });
              this.loading = false;
              return;
          }
          sanitizedQueryRsid1 = sanitizedQueryRsid1.toLowerCase().replace(/(rs|RS)/g, 'rs').replace(/(affx-|AFFX-)/g, 'Affx-');
          queryParams.snp = sanitizedQueryRsid1;
          apiUrl = 'api/SnpEpistasisSurvival';
      } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
          apiUrl = 'api/SnpCancerTypeSurvival';
      } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
          apiUrl = 'api/SnpEpistasisCancerTypeSurvival';
      }

      axios.post(apiUrl, queryParams)
          .then(response => {
              if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP') {
                  this.QTLData.SnpEpistasis = response.data.SnpCancerTypeSurvivalResult;
              } else if (this.selectQueryType === 'Cancer type' && this.selectLociType === 'SNP epistasis') {
                  this.QTLData.SnpEpistasis = response.data.SnpEpistasisCancerTypeSurvivalResult;
              } else if (this.selectQueryType === 'SNP') {
                  this.QTLData.SnpEpistasis = response.data.SnpSurvivalResult;
              } else if (this.selectQueryType === 'SNP epistasis') {
                  this.QTLData.SnpEpistasis = response.data.SnpEpistasisSurvivalResult;
              }
              this.recordNumber = response.data.total;
              this.displayDataBasedOnModel();
              this.loading = false;
          })
          .catch(error => {
              if (error.response) {
                  console.log("请求失败", error.response.data);
                  console.log("状态码:", error.response.status);
                  console.log("响应头:", error.response.headers);
              } else if (error.request) {
                  console.log("请求未收到响应:", error.request);
              } else {
                  console.log('错误', error.message);
              }
              this.loading = false;
          });
  },
  handleDownload() {
      this.downloadClicked = true; 
      this.downloadPdf();
  },
  handleClose() {
      this.imageDialogVisible = false; 
      this.downloadClicked = false;
      if (this.imageUrl) {
          URL.revokeObjectURL(this.imageUrl); 
          this.imageUrl = ''; 
      }
  },
  handleOutsideClick(event) {
      const dialogElement = event.target.closest('.el-dialog');
      if (!dialogElement) {
          this.handleClose();
      }
  },
  clearInput() {
    this.selectQueryType = '';
    this.selectCancerType = '';
    this.queryRsid1 = '';
    this.ModelSelect = '';
    this.selectLociType = '';
  },
  currentChange(page) {
    this.currentPage = page;
    this.submitForm();
  },
  // downloadCSV() {
  //     const headers = {
  //         'SNP': ['Cancertype', 'Model', 'SNP', 'P_Value'],
  //         'SNP Epistasis': ['Cancertype', 'Model', 'SNP epistasis', 'P_Value'],
  //         'CancerType SNP': ['Cancertype', 'Model', 'SNP', 'P_Value'],
  //         'CancerType SNP Epistasis': ['Cancertype', 'Model', 'SNP epistasis', 'P_Value']
  //     };

  //     let columnsToExport = [];
  //     if (this.selectQueryType === 'SNP') {
  //         columnsToExport = headers['SNP'];
  //     } else if (this.selectQueryType === 'SNP Epistasis') {
  //         columnsToExport = headers['SNP Epistasis'];
  //     } else if (this.selectQueryType === 'Cancer Type' && this.selectLociType === 'SNP') {
  //         columnsToExport = headers['CancerType SNP'];
  //     } else if (this.selectQueryType === 'Cancer Type' && this.selectLociType === 'SNP Epistasis') {
  //         columnsToExport = headers['CancerType SNP Epistasis'];
  //     }

  //     // 表头
  //     let csvContent = columnsToExport.join(",") + "\n";

  //     // 数据行
  //     this.QTLData.SnpEpistasis.forEach(row => {
  //         let rowContent = columnsToExport.map(col => {
  //             if (col === 'P_Value' && row[col] !== undefined) {
  //                 return parseFloat(row[col]).toExponential(2);
  //             } else if (col === 'SNP' || col === 'SNP_epi') {
  //                 return row[col];
  //             } else if (col.startsWith('OS_Median') && row[col] !== undefined) {
  //                 return parseFloat(row[col]).toFixed(2);
  //             } else {
  //                 return row[col] !== undefined ? row[col] : '';
  //             }
  //         }).join(",");
  //         csvContent += rowContent + "\n";
  //     });

  //     const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  //     const filename = `${this.selectQueryType}_${this.selectCancerType}_${this.queryRsid1}_${this.ModelSelect}.csv`;

  //     if (window.navigator.msSaveOrOpenBlob) {
  //         window.navigator.msSaveBlob(blob, filename);
  //     } else {
  //         const link = document.createElement('a');
  //         link.href = URL.createObjectURL(blob);
  //         link.download = filename;
  //         document.body.appendChild(link);
  //         link.click();
  //         document.body.removeChild(link);
  //     }
  // },
  downloadCSV() {
    // Extracting column names and headers
    const headers = [];
    const columnsToExport = [];

    this.tableColumns.forEach(column => {
      if (column.prop !== 'Plot') {
        columnsToExport.push(column.prop);
        headers.push(column.label);
      }
    });

    // Generate CSV header row
    let csvContent = headers.join(",") + "\n";

    // Generate CSV data rows
    this.QTLData.SnpEpistasis.forEach(row => {
      let rowContent = columnsToExport.map(col => {
        if (col === 'P_Value' && row[col] !== undefined) {
          return parseFloat(row[col]).toExponential(2);
        } else if (col === 'SNP' || col === 'SNP_epi') {
          return row[col];
        } else if (col.startsWith('OS_Median') && row[col] !== undefined) {
          return parseFloat(row[col]).toFixed(2);
        } else {
          return row[col] !== undefined ? row[col] : '';
        }
      }).join(",");
      csvContent += rowContent + "\n";
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const filename = `${this.selectQueryType}_${this.selectCancerType}_${this.queryRsid1}_${this.ModelSelect}.csv`;

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
  },
  downloadPdf() {
      const cancertype = this.currentCancertype;
      const model = this.currentModel;
      const snp = this.currentSNP;
      axios.get(`api/SurvivaldownloadPdf`, {
          params: {
              Cancertype: encodeURIComponent(cancertype),
              Model: encodeURIComponent(model),
              SNP: encodeURIComponent(snp)
          },
          responseType: 'blob'
      })
      .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const fileName = `${cancertype}_${model}_${snp}.pdf`;
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
          this.downloadClicked = false; 
      });
  },
  fetchPdf(Cancertype, Model, SNP) {
      this.currentCancertype = Cancertype;
      this.currentModel = Model;
      this.currentSNP = SNP;
      axios.get(`api/SurvivalgetPdf`, {
          params: {
              Cancertype: encodeURIComponent(Cancertype),
              Model: encodeURIComponent(Model),
              SNP: encodeURIComponent(SNP)
          },
          responseType: 'blob'
      })
      .then(response => {
          const imageUrl = URL.createObjectURL(new Blob([response.data], { type: 'image/png' }));
          this.imageUrl = imageUrl;
          this.imageDialogVisible = true;
      })
      .catch(error => {
          console.error('Error fetching image:', error);
      });
  },

      
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
}
.query-type-select {
z-index: 2000;
}
.download-button .el-icon-download {
  font-size: 16px; 
  font-weight: bold; 
  color: blue; 
}
.el-button--primary {
  border-color: transparent; 
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
color: black;
font-family: 'Helvetica';
}

::v-deep .el-table thead th {
  color: #2d4059 !important;
  font-family: 'Helvetica';
  font-weight: bold;
}
/* .el-icon-zoom-in {
color: #FF7C43;
font-size: 1.2em;
} */
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
.query-type-select ::v-deep .el-input__inner,
.cancer-type-select ::v-deep .el-input__inner,
.p-value-select ::v-deep .el-input__inner,
.download-button .el-icon-download,
.box-card,
.custom-row,
.card-title,
.header-controls,
.custom-column-header,
.el-dialog,
.el-table,
.el-table th,
.el-table td,
.custom-icon {
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
.header-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.el-pagination {
  flex-grow: 1;
}

.el-button {
  margin-left: auto;
}

</style>
