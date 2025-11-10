<template>
    <div class="content-container">
        <el-card class="box-card">
            <el-row class="custom-row" :style="{ marginBottom: '15px' }">
                <el-col :span="24">
                    <p class="card-description" style="font-size: 18px; line-height: 1.7;font-family: 'Helvetica';">
                        The development of cancer is thought to derive from the accumulation of somatic mutations. These mutations do not occur randomly; functionally antagonistic mutations are likely to be selected exclusively (mutual exclusivity) of each other, whereas synergistic alterations are frequently co-selected and observed together (co-occurrence) in certain tumor subtypes. Followed the method previously described by <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8690927/" style="color:#B285D3;">Wang et al.</a>, we identified a set of <span style="color: blue; font-weight: bold;">98</span> significant mutation epistasis pairs with a P-value < 0.05 across 18 cancer types in TCGA.
                    </p>
                </el-col>
            </el-row>
            <div>
                <el-row :gutter="40" type="flex" justify="center"> <!-- 修改gutter属性以增加搜索框之间的距离 -->
                    <!-- Query type select -->
                    <el-col :span="5" :offset="0">
                        <span class="input-label">Query type:</span>
                        <el-select v-model="selectQueryType" placeholder="Query type" class="place-input query-type-select" style="width: 100%; font-size: 17px;z-index: 1000;">
                            <el-option v-for="query in queryTypes" :key="query.id" :value="query.queryName">
                                <span style="float: left">{{ query.queryName }}</span>
                            </el-option>
                        </el-select>
                    </el-col>
                    <!-- Cancer type select -->
                    <el-col :span="5" :offset="0" v-if="selectQueryType === 'Cancer type'">
                        <span class="input-label">Cancer type:</span>
                        <el-select v-model="selectCancerType" placeholder="Cancer type" class="place-input cancer-type-select" style="width: 100%;font-size: 17px;">
                            <el-option v-for="cancer in cancerType" :key="cancer.id" :value="cancer.cancerName">
                                <span style="float: left">{{ cancer.cancerName }}</span>
                                <span style="float: right">(N={{ cancer.sampleNumber }})</span>
                            </el-option>
                        </el-select>
                    </el-col>
                    <!-- Gene input based on query type -->
                    <el-col :span="5" :offset="0" v-if="selectQueryType === 'Gene'">
                        <span class="input-label">Gene:</span>
                        <el-input v-model="queryGene" placeholder="Gene" class="place-input" style="width: 100%;font-size: 17px;"></el-input>
                        <span :class="{ 'text-black': !isHoveredGene, 'text-orange': isHoveredGene }" @mouseover="handleHoverAndSetQueryGene" @mouseleave="handleMouseLeave" style="font-size: 16px;">e.g., DOCK3</span>
                    </el-col>
                </el-row>
            </div>

            <div style="margin: 15px 0;">
                <el-row type="flex" justify="center" :gutter="5"> <!-- 修改gutter属性以缩小按钮之间的距离 -->
                    <el-col :span="4" class="text-center">
                        <el-button type="primary" class="submit-button" @click="submitForm">Submit</el-button>
                    </el-col>
                    <el-col :span="2" class="text-center">
                        <el-button type="danger" class="cancel-button" @click="clearInput">Cancel</el-button>
                    </el-col>
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
                :data="MutationResult"
                style="width: 100%;"
                max-height="600"
                stripe
                empty-text="No results found for your query"
            >
                <el-table-column prop="Pvalue" label="Sample" width="85" align="center" class="custom-column-header">
                    <template v-slot="scope">
                        <a-icon type="bar-chart" theme="outlined"
                        @click="fetchPdf(scope.row.Cancertype, scope.row.Mutation_X, scope.row.Mutation_Y)" 
                        style="font-size: 2.2em; cursor: pointer; color: #E5446D;" />
                    </template>
                </el-table-column>
                <el-table-column
                    prop="Cancertype"
                    label="Cancer"
                    width="80"
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
                    prop="Mutation_X"
                    label="Mutation_X"
                    width="145"
                    align="center" 
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                    prop="Gene_X"
                    label="Gene_X"
                    width="90"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                    prop="Mutation_Y"
                    label="Mutation_Y"
                    width="145"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                    prop="Gene_Y"
                    label="Gene_Y"
                    width="90"
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                    prop="Cor_Type"
                    label="Cor_Type"
                    width="163"
                    align="center" 
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template #header>
                        Cor_Type
                        <el-tooltip class="item" effect="dark" content="Types of mutation epistasis" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="OR"
                    label="Odds Ratio"
                    width="150"
                    sortable
                    align="center"
                    class="custom-column-header"
                    show-overflow-tooltip>
                    <template v-slot="scope">
                        {{ scope.row.OR !== undefined ? (scope.row.OR < 0.05 ? scope.row.OR.toExponential(2) : scope.row.OR.toFixed(2)) : '' }}
                    </template>
                    <template #header>
                        Odds Ratio
                        <el-tooltip class="item" effect="dark" content="Odds ratio for mutation epistasis calculated by Fisher's exact test" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="Pvalue"
                    label="P-value"
                    width="129"
                    align="center"
                    sortable
                    class="custom-column-header">
                    <template #default="scope">
                        {{ parseFloat(scope.row.Pvalue).toExponential(2) }}
                    </template>
                    <template #header>
                        P-value
                        <el-tooltip class="item" effect="dark" content="P-value calculated by Fisher's exact test" placement="top">
                            <i class="el-icon-question"></i>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog :visible.sync="imageDialogVisible" :style="{ maxWidth: '1240px', margin: '0 auto' }" width="auto" @close="handleClose" 
            :close-on-click-modal="true" :close-on-press-escape="true" :modal-append-to-body="false">
                <div style="text-align: center;" @click="imageDialogVisible = false">
                    <img :src="imageUrl" style="width: 1140px; height: 230px; object-fit: contain;" alt="Image Preview">
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
    name: 'EpistasisMutation',
    data() {
        return {
            cancerType: [
                {"id": "01", "cancerName": "All", "sampleNumber": "6685"},
                {"id": "02", "cancerName": "BLCA", "sampleNumber": "411"},
                {"id": "03", "cancerName": "BRCA", "sampleNumber": "791"},
                {"id": "04", "cancerName": "COAD", "sampleNumber": "288"},
                {"id": "05", "cancerName": "LGG", "sampleNumber": "510"},
                {"id": "06", "cancerName": "LUAD", "sampleNumber": "513"},               
                {"id": "07", "cancerName": "PAAD", "sampleNumber": "177"},
                {"id": "08", "cancerName": "READ", "sampleNumber": "89"},
                {"id": "09", "cancerName": "STAD", "sampleNumber": "439"},
                {"id": "10", "cancerName": "UCEC", "sampleNumber": "447"}
            ],
            queryTypes: [
                { id: '001', queryName: 'Cancer type' },
                { id: '002', queryName: 'Gene' }
            ],
            cancerTypes: [
                "BLCA","BRCA","COAD","LGG","LUAD","PAAD","READ","STAD","UCEC"
            ],
            selectQueryType: 'Cancer type',
            selectCancerType: 'All',
            queryGene: '',
            isClickedGene: false,
            loading: false,
            MutationResult: [],
            recordNumber: 0,
            currentPage: 1,
            perPage: 8,
            imageUrl: '',
            downloadClicked: false,
            imageDialogVisible: false,
        }
    },
    methods: {
        handleHoverAndSetQueryGene() {
            this.queryGene = 'DOCK3';
            this.isHoveredGene = true;
        },
        handleMouseLeave() {
            this.isHoveredGene = false;
        },
        clearInput() {
            this.selectQueryType = 'Gene';
            this.selectCancerType = '';
            this.queryGene = '';
            this.isHoveredGene = false;
        },
        submitForm() {
            this.queryGene = this.queryGene.replace(/\s+/g, '');
            const isValidInput = /^[a-zA-Z0-9]*$/.test(this.queryGene);
            if (!isValidInput) {
                this.$alert('Invalid input', 'Error', {
                    confirmButtonText: 'OK',
                    callback: () => {
                        this.MutationResult = [];
                        this.recordNumber = 0;
                    }
                });
                return;
            }
            this.loading = true;
            let params = {
                queryType: this.selectQueryType,
                page: this.currentPage,
                perPage: this.perPage
            };
            if (this.selectQueryType === 'Cancer type') {
                params.cancerType = this.selectCancerType;
            } else if (this.selectQueryType === 'Gene') {
                params.gene = this.queryGene;
            }
            axios.post('api/mutationRequest', params)
                .then(response => {
                    this.MutationResult = response.data.results;
                    this.recordNumber = response.data.total;
                })
                .catch(error => {
                    console.error('Error during search:', error);
                    this.$alert('Search failed due to server error.', 'Error', {
                        confirmButtonText: 'OK'
                    });
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
        const headers = ['Cancer', 'Mutation_X', 'Gene_X', 'Mutation_Y', 'Gene_Y', 'Cor_Type', 'Odds Ratio', 'P-value'];
        const rows = this.MutationResult.map(item => [
            item.Cancertype,
            item.Mutation_X,
            item.Gene_X,
            item.Mutation_Y,
            item.Gene_Y,
            item.Cor_Type,
            item.OR !== undefined ? parseFloat(item.OR).toFixed(2) : '',
            parseFloat(item.Pvalue).toExponential(2)
        ]);

        let csvContent = "data:text/csv;charset=utf-8,"
            + headers.join(",") + "\n"
            + rows.map(e => e.join(",")).join("\n");

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");

        const queryType = this.selectQueryType || '';
        const cancerType = this.selectCancerType || '';
        const queryGene = this.queryGene || '';
        const currentPage = this.currentPage || '';

        const fileNameParts = [queryType, cancerType, queryGene];
        const fileName = fileNameParts.filter(part => part !== '').join('_') + `_page${currentPage}.csv`;

        link.setAttribute("href", encodedUri);
        link.setAttribute("download", fileName);
        document.body.appendChild(link); 
        link.click();
        document.body.removeChild(link);
    },
        handleClose() {
            this.imageDialogVisible = false;
        },
        fetchPdf(Cancertype, Mutation_X, Mutation_Y) {
            this.currentCancertype = Cancertype;
            this.currentMutation_X = Mutation_X;
            this.currentMutation_Y = Mutation_Y;

            axios.get('api/mutationPng', {
                params: {
                    Cancertype: encodeURIComponent(Cancertype),
                    Mutation_X: encodeURIComponent(Mutation_X),
                    Mutation_Y: encodeURIComponent(Mutation_Y)
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
        handleDownload() {
            const cancertype = this.currentCancertype; 
            const mutation_x = this.currentMutation_X;
            const mutation_y = this.currentMutation_Y;
            axios.get('api/mutationPdf', {
                params: {
                    Cancertype: cancertype,
                    Mutation_X: mutation_x,
                    Mutation_Y: mutation_y
                },
                responseType: 'blob'
            })
            .then(response => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const fileName = `${cancertype}_${mutation_x}_${mutation_y}.pdf`;
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
    },
    mounted() {
        this.clearInput();
        this.selectQueryType = 'Cancer type'; // 设置初次进入页面时的默认Query Type
        this.selectCancerType = 'All'; // 设置默认的Cancer Type为All
        this.submitForm(); // 自动请求数据用于展示
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
    font-family: 'Helvetica', sans-serif;
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
    font-family: 'Helvetica';
}

</style>
