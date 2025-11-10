<template>
    <div class="content-container">
        <el-card class="box-card">
            <el-row class="custom-row" :style="{ marginBottom: '15px' }">
                <el-col :span="24">
                    <p class="card-description" style="font-size: 20px; line-height: 1.6; font-family: 'Helvetica';">
                        This module provides the significant epiSNP associated with cancers (P-value < 0.05).
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
                    <!-- SNP input based on query type -->
                    <el-col :span="5" :offset="0" v-if="selectQueryType === 'SNP'">
                        <span class="input-label">SNP:</span>
                        <el-input v-model="queryRsid1" placeholder="SNP" class="place-input" style="width: 100%;"></el-input>
                        <span :class="{ 'text-black': !isClicked1, 'text-orange': isClicked1 }" @click="handleClickAndSetQueryRsid1" style="font-size: 16px;">e.g., rs17632542</span>
                    </el-col>
                    <!-- Chromosome Range input based on query type -->
                    <el-col :span="5" :offset="0" v-if="selectQueryType === 'Chromosome range'">
                        <span class="input-label">Chromosome range:</span>
                        <el-input v-model="queryRsid1" placeholder="Chromosome range" class="place-input" style="width: 100%;font-size: 17px;"></el-input>
                        <span :class="{ 'text-black': !isClicked2, 'text-orange': isClicked2 }" 
                        @click="handleClickAndSetQueryRsid2" style="font-size: 16px;">e.g., chr1:1003629-4063154</span>
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

        <!-- Search Results Display -->
        <!-- Table Display -->
        <el-card class="box-card">
            <div class="header-controls">
                <el-pagination :hide-on-single-page="true" :total="recordNumber" :page-size="perPage" :current-page.sync="currentPage" @current-change="currentChange" layout="prev, pager, next"></el-pagination>
                <div style="margin-bottom: 0px; text-align: right; margin-right: 20px;">
                    <el-button type="primary" :circle="true" @click="downloadCSV" style="font-size: 35px; padding: 0; background-color: white; color: blue; font-weight: bold;">
                        <i class="el-icon-download"></i>
                    </el-button>
                </div>
            </div>
            <el-table
                v-loading="loading"
                :data="SnpGwasSearchThreeWayResult"
                style="width: 100%;"
                max-height="600"
                stripe
                empty-text="No results found for your query"
            >
                <el-table-column
                    prop="N"
                    label="Sample"
                    width="80"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        <a-icon type="bar-chart" theme="outlined" @click="fetchPdf(scope.row.Cancertype, scope.row.SNP)" style="font-size: 2.2em; cursor: pointer; color: blueviolet;"/>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="Cancertype"
                    label="Cancer"
                    width="105"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        <span :style="{ color: 'red', fontSize: cancerTypes.includes(scope.row.Cancertype) ? '1.1em' : 'inherit' }">
                            {{ scope.row.Cancertype }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="SNP"
                    label="SNP"
                    width="133"
                    align="center" 
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="props">
                        {{ props.row.SNP }}
                        <a target="_blank" :href="'https://www.ncbi.nlm.nih.gov/snp/'  + props.row.SNP">
                            <i class="el-icon-zoom-in" style="color: #FF7C43;font-size: 1.2em;"></i>
                        </a>
                    </template>
                </el-table-column>
                <el-table-column
                    label="Position"
                    width="188"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        {{ scope.row.Pos }} : {{ scope.row.POS }}
                        <a target="_blank" :href="'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position='  + scope.row.Pos + ':' + scope.row.POS">
                            <i class="el-icon-zoom-in" style="color: #FF7C43;font-size: 1.2em;"></i>
                        </a>
                    </template>
                </el-table-column>
                <!-- <el-table-column
                    prop="alleles"
                    label="Alleles(A/a)"
                    width="99"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column> -->
                <el-table-column
                    prop="A1"
                    label="A1"
                    width="68"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template #header>
                        A1
                        <el-tooltip class="item" effect="dark" content="The effect allele calculated by GCTA fast-GLMM" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="A2"
                    label="A2"
                    width="68"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template #header>
                        A2
                        <el-tooltip class="item" effect="dark" content="The other allele calculated by GCTA fast-GLMM" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="AF1"
                    label="AF1"
                    width="58"
                    align="center" 
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        <span>{{ parseFloat(scope.row.AF1).toFixed(2) }}</span>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="BETA"
                    label="OR"
                    width="105"
                    sortable
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        <span>{{ parseFloat(Math.exp(scope.row.BETA)).toFixed(2) }}</span>
                    </template>
                    <template #header>
                        Beta
                        <el-tooltip class="item" effect="dark" content="Beta calculated by GCTA fast-GLMM" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="P"
                    label="P-value"
                    width="123"
                    align="center"
                    sortable
                    class="custom-column-header">
                    <template #default="scope">
                        {{ parseFloat(scope.row.P).toExponential(2) }}
                    </template>
                    <template #header>
                        P-value
                        <el-tooltip class="item" effect="dark" content="P-value calculated by GCTA fast-GLMM" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="case"
                    label="Case"
                    width="72"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                    prop="control"
                    label="Control"
                    width="80"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
            </el-table>
            <el-dialog :visible.sync="imageDialogVisible" :style="{ maxWidth: '560px', margin: '0 auto' }" width="auto" @close="handleClose" 
            :close-on-click-modal="true" :close-on-press-escape="true" :modal-append-to-body="false">
                <div style="text-align: center;" @click="imageDialogVisible = false">
                    <img :src="imageUrl" style="width: 530px; height: 500px; object-fit: contain;" alt="Image Preview">
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
import axios from 'axios'
export default {
    name: 'SNP-GWAS',
    data() {
        return {
            cancerType: [
                { id: '001', cancerName: 'All', sampleNumber: '399723' },
                {id: '002', cancerName: 'Breast', sampleNumber: '189339'},
                {id: '003', cancerName: 'Prostate', sampleNumber: '159222'},
                {id: '004', cancerName: 'Melanoma', sampleNumber: '322104'},
                {id: '005', cancerName: 'Colon', sampleNumber: '320482'},
                {id: '006', cancerName: 'Cervical', sampleNumber: '176438'},
                {id: '007', cancerName: 'Lung', sampleNumber: '318728'},
                {id: '008', cancerName: 'Bladder', sampleNumber: '317673'},
                {id: '009', cancerName: 'Rectal', sampleNumber: '316597'},
                {id: '0010', cancerName: 'Uterine', sampleNumber: '172157'},
                {id: '0011', cancerName: 'Kidney', sampleNumber: '315750'},
                {id: '0012', cancerName: 'Ovarian', sampleNumber: '171548'},
                {id: '0013', cancerName: 'Pancreatic', sampleNumber: '315056'},
                {id: '0014', cancerName: 'Esophagus', sampleNumber: '315022'},
                {id: '0015', cancerName: 'Stomach', sampleNumber: '314676'},
                {id: '0016', cancerName: 'Brain', sampleNumber: '314501'},
                {id: '0017', cancerName: 'Liver', sampleNumber: '314490'},
            ],
            queryTypes: [
                { id: '001', queryName: 'SNP' },
                { id: '002', queryName: 'Chromosome range' },
                { id: '003', queryName: 'Cancer type' }
            ],
            cancerTypes: [
                "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
                "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
                "Rectal", "Stomach", "Uterine"
            ],
            selectQueryType:'',
            SnpGwasSearchThreeWayResult: [],
            recordNumber: 0,
            currentPage: 1,
            selectCancerType: '', 
            queryRsid1: '',
            pValueThreshold: '0.05',
            isClicked1: false,
            isClicked2: false,
            loading: false,
            perPage: 8,
            defaultQueryType: 'SNP',
            defaultCancerType: 'Breast',
            defaultPValueThreshold: '0.05',
            imageUrl: '',
            downloadClicked: false,
            imageDialogVisible: false,
            initialLoad: true
        }
    },
    methods: {
        handleClickAndSetQueryRsid1() {
            this.isClicked1 = !this.isClicked1;
            this.queryRsid1 = 'rs11992171';
            this.selectCancerType = 'Prostate';
            this.pValueThreshold = '0.05';
        },

        handleClickAndSetQueryRsid2() {
            this.isClicked2 = !this.isClicked2;
            this.queryRsid1 = 'chr16:90093070-90103075';
            this.selectCancerType = 'Melanoma';
            this.pValueThreshold = '0.05';
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
        validateAndFormatInput(input) {
            input = input.replace(/\s+/g, ''); // 去除所有空格

            if (/^rs/i.test(input)) {
                return input.toLowerCase();
            } else if (/^affx/i.test(input)) {
                return input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
            } else if (/^chr\d+:\d+-\d+$/.test(input)) {
                return input.toLowerCase();
            } else if (this.selectQueryType === 'Cancer type') {
                return input; // 对于癌症类型，不需要特殊处理
            } else {
                this.$alert('Invalid input', 'Error', {
                    confirmButtonText: 'OK',
                    callback: () => {
                        this.SnpGwasSearchThreeWayResult = [];
                        this.recordNumber = 0;
                    }
                });
                return null;
            }
        },
        clearInput() {
            this.queryRsid1 = '';
            this.selectQueryType = this.defaultQueryType;
            this.selectCancerType = this.defaultCancerType;
            this.pValueThreshold = this.defaultPValueThreshold;
            this.isClicked1 = false;
            this.isClicked2 = false;
            this.SnpGwasSearchThreeWayResult = []; 
        },
        initData() {
            this.initialLoad = true;
            this.selectQueryType = 'SNP';
            this.pValueThreshold = '0.05';
            this.submitForm(); 
        },
        submitForm() {
            this.loading = true;
            let params = {};

            if (this.initialLoad) {
                params = { Type: true };
                this.initialLoad = false;
            } else {
                if (this.selectQueryType === 'SNP' || this.selectQueryType === 'Chromosome range') {
                    let formattedInput = this.validateAndFormatInput(this.queryRsid1);
                    if (formattedInput === null) {
                        this.SnpGwasSearchThreeWayResult = [];
                        this.recordNumber = 0;
                        this.loading = false;
                        return;
                    }
                    params = {
                        queryType: this.selectQueryType,
                        cancerType: this.selectCancerType || 'All',
                        pValue: this.pValueThreshold,
                        page: this.currentPage,
                        perPage: this.perPage,
                        snp: formattedInput,
                        chromosomeRange: this.selectQueryType === 'Chromosome range' ? formattedInput : undefined,
                    };
                } else if (this.selectQueryType === 'Cancer type') {
                    params = {
                        queryType: this.selectQueryType,
                        cancerType: this.selectCancerType || 'All',
                        pValue: this.pValueThreshold,
                        page: this.currentPage,
                        perPage: this.perPage,
                    };
                }
            }

            axios.post('api/SnpGwasSearchThreeWay', params)
                .then(response => {
                    this.SnpGwasSearchThreeWayResult = response.data.results;
                    this.recordNumber = response.data.total;
                })
                .catch(error => {
                    console.error('Error during search:', error);
                    this.$message.error('Search failed due to server error.');
                })
                .finally(() => {
                    this.loading = false;
                });
        },


        currentChange(newPage) {
            this.currentPage = newPage;
            this.submitForm();
        },
        downloadCSV() {
        const headers = ['Cancer', 'SNP', 'Position', 'A1', 'A2', 'AF1', 'OR', 'P-value', 'Case', 'Control', 'Sample'];
        const rows = this.SnpGwasSearchThreeWayResult.map(item => [
            item.Cancertype,
            item.SNP,
            `${item.Pos}:${item.POS}`,
            item.A1,
            item.A2,
            parseFloat(item.AF1).toFixed(2),
            parseFloat(Math.exp(item.BETA)).toFixed(2),
            parseFloat(item.P).toExponential(2),
            item.case,
            item.control,
            item.N
        ]);

        let csvContent = "data:text/csv;charset=utf-8,"
            + headers.join(",") + "\n"
            + rows.map(e => e.join(",")).join("\n");

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");

        const queryType = this.selectQueryType || '';
        const cancerType = this.selectCancerType || '';
        const snpOrChromosomeRange = this.queryRsid1 || '';
        const pValueThreshold = this.pValueThreshold || '';
        const currentPage = this.currentPage || '';

        const fileNameParts = [queryType, cancerType, snpOrChromosomeRange, pValueThreshold];
        const fileName = fileNameParts.filter(part => part !== '').join('_') + `_page${currentPage}.csv`;

        link.setAttribute("href", encodedUri);
        link.setAttribute("download", fileName);
        document.body.appendChild(link); 
        link.click();
        document.body.removeChild(link);
    },
        downloadPdf() {
            const cancertype = this.currentCancertype; 
            const snp = this.currentSNP;
            axios.get(`api/downloadPdf`, {
                params: {
                    Cancertype: encodeURIComponent(cancertype),
                    SNP: encodeURIComponent(snp)
                },
                responseType: 'blob'
            })
            .then(response => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const fileName = `${cancertype}_${snp}.pdf`;
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
        fetchPdf(Cancertype, SNP) {
            this.currentCancertype = Cancertype;
            this.currentSNP = SNP;
            axios.get(`api/getPdf`, {
                params: {
                    Cancertype: encodeURIComponent(Cancertype),
                    SNP: encodeURIComponent(SNP)
                },
                responseType: 'blob'
            })
            .then(response => {
                const imageUrl = URL.createObjectURL(response.data);
                this.imageUrl = imageUrl;
                this.imageDialogVisible = true;
            })
            .catch(error => {
                console.error('Error fetching image:', error);
            });
        },
    },
    computed: {},
    mounted() {
        this.initData();
        document.addEventListener('click', this.handleOutsideClick);   
    },
    beforeDestroy() {
        document.removeEventListener('click', this.handleOutsideClick);
    }
}
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
    margin: 0 auto; /* Ensure content is centered */
}
.text-black {
    display: block;
    color: black;
    cursor: pointer;
    margin-top: 8px;
}
::v-deep .el-table thead th {
  color: #2d4059 !important;
  font-family: 'Helvetica';
  font-weight: bold;
}
.text-orange {
    display: block;
    color: orange;
    cursor: pointer;
    margin-top: 8px;
}
body {
    font-family: 'Arial', sans-serif;
}
.box-card {
    margin: 5px 0;
    padding: 10px;
}
.custom-row {
    margin-top: -10px; /* Adjust margin for top alignment */
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
    margin-top: 5px; /* Adjust margin for spacing */
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
.custom-select-input {
    font-size: 17px; /* Desired font size */
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
.download-button .el-icon-download {
    font-size: 16px;
    font-weight: bold;
    color: blue; 
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
</style>
