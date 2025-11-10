<template>
    <div>
        <!-- 动态效果的容器 -->
        <div id="container"></div>

        <el-card class="box-card" style="margin-top: 20px; width: 1140px;">
            <el-row style="background-color: #ACD1E9; height: 50px; text-align: left; line-height: 50px; border: 1px solid #ACD1E9; 
            border-radius: 5px 5px 0px 0px; margin-top: 1px;margin-bottom: 0px;">
                <el-col :span="21">
                    <span style="padding: 0px 20px; font-weight: bold; color: #29506D;font-size:21px">Epistasis results</span>
                </el-col>
            </el-row>
            
            <el-row style="border-radius: 0px 0px 5px 5px; border: 1px solid #D6EADF;margin-bottom: 0px;">
                <el-table
                    v-loading="loading"
                    border
                    :data="snpEpiTableData"
                    style="width: 100%;font-size: 15px;"
                    max-height="500"
                    stripe
                    empty-text="No SNP epistasis results found for your query">
                    
                    <!-- Sample 列 -->
                    <el-table-column prop="alleles1" label="Sample" width="78" align="center" class="custom-column-header">
                        <template v-slot="scope">
                            <a-icon type="fund" theme="twoTone" 
                            @click="fetchPdfSample(scope.row.Cancertype, scope.row.SNPepi)" 
                            style="font-size: 2.0em; cursor: pointer; color: #AED4D4;" />
                        </template>
                    </el-table-column>

                    <!-- OR plot 列 -->
                    <el-table-column prop="ORstatus" label="OR plot" width="82" align="center" class="custom-column-header">
                        <template v-slot="scope">
                            <a-icon type="bar-chart" theme="outlined"
                                @click="fetchPdfOR(scope.row.Cancertype, scope.row.SNPepi, scope.row.ORstatus)" 
                                :style="{ fontSize: '2.0em', cursor: 'pointer', color: scope.row.ORstatus !== false ? 'blue' : 'grey' }"
                            />
                        </template>
                    </el-table-column>

                    <!-- Reliability 列 -->
                    <el-table-column label="Reliability" width="92" align="center" class="custom-column-header">
                        <template v-slot="scope">
                            <div class="stars-container">
                                <el-tooltip content="epistasis" placement="top">
                                    <i class="el-icon-star-on" :class="{ 'star-yellow': scope.row.Isepistasis, 'star-gray': !scope.row.Isepistasis }" style="font-size: 24px;"></i>
                                </el-tooltip>
                                <el-tooltip content="joint" placement="top">
                                    <i class="el-icon-star-on" :class="{ 'star-yellow': scope.row.Isjoint, 'star-gray': !scope.row.Isjoint }" style="font-size: 24px;"></i>
                                </el-tooltip>
                                <el-tooltip content="boost" placement="top">
                                    <i class="el-icon-star-on" :class="{ 'star-yellow': scope.row.Isboost, 'star-gray': !scope.row.Isboost }" style="font-size: 24px;"></i>
                                </el-tooltip>
                            </div>
                        </template>
                    </el-table-column>

                    <!-- Cancer 列 -->
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

                    <!-- SNP epistasis 列 -->
                    <el-table-column prop="SNPepi" label="SNP epistasis" width="260" align="center" class="custom-column-header">
                        <template slot-scope="scope">
                            <span v-for="(snp, index) in scope.row.SNPepi.split('_')" :key="index">
                                {{ snp }}
                                <a :href="'https://www.ncbi.nlm.nih.gov/snp/' + snp" target="_blank">
                                    <i class="el-icon-zoom-in" style="color: #FF7C43; font-size: 1.2em;"></i>
                                </a>
                                <span v-if="index === 0">_</span>
                            </span>
                        </template>
                    </el-table-column>

                    <!-- Odds ratio 列 -->
                    <el-table-column label="Odds ratio" width="116" align="center" class="custom-column-header">
                        <template v-slot:header>
                            Odds ratio
                            <el-tooltip content="Odds ratio for snp epistasis calculated by PLINK" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.OR_INT !== undefined ? scope.row.OR_INT.toFixed(2) : (scope.row.OR !== undefined ? scope.row.OR.toFixed(2) : '') }}
                        </template>
                    </el-table-column>

                    <!-- P_epistasis 列 -->
                    <el-table-column prop="P_epistasis" label="P_epistasis" width="147" sortable align="center" show-overflow-tooltip class="custom-column-header">
                        <template v-slot:header>
                            P_epistasis
                            <el-tooltip content="Asymptotic p-value calculated by PLINK" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.P_epistasis !== undefined && scope.row.P_epistasis != 100 ? scope.row.P_epistasis.toExponential(2) : (scope.row.P !== undefined ? scope.row.P.toExponential(2) : '-') }}
                        </template>
                    </el-table-column>

                    <!-- Best SNP 列 -->
                    <el-table-column prop="Best_snp" label="Best SNP" width="113" align="center" class="custom-column-header">
                        <template v-slot:header>
                            Best SNP
                            <el-tooltip class="item" effect="dark" content="The SNP with the highest statistic obtained by testing SNP1 through PLINK." placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                    </el-table-column>

                    <!-- P-joint 列 -->
                    <el-table-column label="P-joint" width="111" sortable align="center" class="custom-column-header">
                        <template v-slot:header>
                            P-joint
                            <el-tooltip content="Joint p-value" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            <span v-html="scope.row.P_joint !== undefined && scope.row.P_joint != 100 ? scope.row.P_joint.toExponential(2) : '<i class=\'el-icon-minus\' style=\'color: #FA8072;\'></i>'"></span>
                        </template>
                    </el-table-column>

                    <!-- P-boost 列 -->
                    <el-table-column label="P-boost" width="120" sortable align="center" class="custom-column-header">
                        <template v-slot:header>
                            P-boost
                            <el-tooltip content="Boost p-value" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            <span v-html="scope.row.P_boost !== undefined && scope.row.P_boost != 100 ? scope.row.P_boost.toExponential(2) : '<i class=\'el-icon-minus\' style=\'color: #FA8072;\'></i>'"></span>
                        </template>
                    </el-table-column>

                    <!-- P-saige 列 -->
                    <el-table-column label="P-saige" width="118" sortable align="center" class="custom-column-header">
                        <template v-slot:header>
                            P-saige
                            <el-tooltip class="item" effect="dark" content="Asymptotic p-value calculated by SAIGE" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.P_saige !== undefined ? (scope.row.P_saige === 0 ? '0' : scope.row.P_saige.toExponential(2)) : (scope.row.saige_p !== undefined ? scope.row.saige_p.toExponential(2) : '') }}
                        </template>
                    </el-table-column>

                    <!-- Is.SPA 列 -->
                    <el-table-column prop="IsSPA" label="Is.SPA" width="88" align="center" class="custom-column-header">
                        <template slot-scope="scope">
                            <i :class="['custom-icon', scope.row.IsSPA ? 'el-icon-check' : 'el-icon-close']" :style="{ color: scope.row.IsSPA ? 'green' : 'red' }"></i>
                        </template>
                        <template v-slot:header>
                            Is.SPA
                            <el-tooltip class="item" effect="dark" content="Whether saddle point approximation(SPA) is converged or not" placement="top">
                                <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                    </el-table-column>
                </el-table>

                <el-pagination
                    :hide-on-single-page="true"
                    :total="epiRecordNumber"
                    :page-size="20"
                    :current-page="currentEpiPage"
                    @current-change="currentEpiChange"
                    layout="prev, pager, next">
                </el-pagination>

                <!-- Sample图对话框 -->
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

                <!-- OR图对话框 -->
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

                <!-- 自定义alert弹框 -->
                <div v-if="showAlert" class="custom-alert" @click="closeAlert">
                    <div class="custom-alert-content" @click="stopPropagation">
                        <div style="font-size: 20px; line-height: 1.5em; text-align: center;">
                            <strong style="color: blue;">Please note: </strong>
                            The epistasis associated with this SNP has not satisfied the criteria for 
                            <strong style="color: black;">sample filteration</strong> in the context of the current cancer phenotype.
                        </div>
                        <el-button @click="closeAlert" style="margin-top: 20px;">OK</el-button>
                    </div>
                </div>
            </el-row>
        </el-card>

        <el-card class="box-card" style="margin-top: 20px; width: 1140px;">
            <el-row style="background-color: #ACD1E9; height: 50px; text-align: left; line-height: 50px; border: 1px solid #ACD1E9; 
            border-radius: 5px 5px 0px 0px; margin-top: 1px;margin-bottom: 0px;">
                <el-col :span="21">
                    <span style="padding: 0px 20px; font-weight: bold; color: #29506D;font-size:21px">GWAS results</span>
                </el-col>
            </el-row>
            
            <el-row style="border-radius: 0px 0px 5px 5px; border: 1px solid #D6EADF;margin-bottom: 0px;">
                <el-table
                    v-loading="loading"
                    border
                    :data="snpGWASData"
                    style="width: 100%;font-size: 15px;"
                    max-height="500"
                    stripe>
                    <el-table-column
                        prop="Cancertype"
                        label="Cancer"
                        width="100"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                        <template v-slot="scope">
                            <span :style="{ color: 'red', fontSize: cancerTypes.includes(scope.row.Cancertype) ? '1em' : 'inherit' }">
                                {{ scope.row.Cancertype }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column
                        prop="SNP"
                        label="SNP"
                        width="140"
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
                        width="160"
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
                    <el-table-column
                        prop="alleles"
                        label="Alleles(A/a)"
                        width="110"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column
                        prop="A1"
                        label="A1"
                        width="48"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column
                        prop="A2"
                        label="A2"
                        width="48"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column
                        prop="AF1"
                        label="AF1"
                        width="62"
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
                        width="90"
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
                        width="110"
                        align="center"
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
                        width="70"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column
                        prop="control"
                        label="Control"
                        width="78"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column
                        prop="N"
                        label="Sample"
                        width="85"
                        align="center"
                        class="custom-column-header"
                        show-overflow-tooltip>
                        <template v-slot="scope">
                            <a-icon type="bar-chart" theme="outlined" @click="fetchPdf(scope.row.Cancertype, scope.row.SNP)" style="font-size: 1.8em; cursor: pointer; color: blueviolet;"/>
                        </template>
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

                <el-pagination
                    :hide-on-single-page="true"
                    :total="recordNumber"
                    :page-size="20"
                    :current-page="currentGWASPage"
                    @current-change="currentGWASChange"
                    layout="prev, pager, next">
                </el-pagination>
            </el-row>
        </el-card>
        
    </div>
</template>

<script>
    import axios from 'axios';
    import Highcharts from 'highcharts';
    import Networkgraph from 'highcharts/modules/networkgraph';

    Networkgraph(Highcharts);

    export default {
        name: "quickSearchSnpEpistasis",
        data() {
            return {
                snpGWASData: [], 
                snpEpiTableData: [],
                snpEpiNetworkData: [],
                loading: false,
                recordNumber: 0,
                epiRecordNumber: 0,
                pdfDialogVisible: false,
                imageUrl: '',
                imageDialogVisible: false,
                downloadClicked: false,
                currentSNP: '',
                currentGWASPage: 1,
                currentEpiPage: 1,
                imageDialogVisibleSample: false,
                imageDialogVisibleOR: false,
                downloadClickedSample: false,
                downloadClickedOR: false,
                useModalAppendToBody: false,
                showAlert: false,
                currentCancertype: '',
                currentSNPepi: '',
                cancerTypes: [
                    "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
                    "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
                    "Rectal", "Stomach", "Uterine"
                ],
            };
        },
        methods: {
            // 添加CSV下载功能
            downloadCSV() {
                if (!Array.isArray(this.snpEpiTableData) || this.snpEpiTableData.length === 0) {
                    this.$message.error('No data available for download');
                    return;
                }

                const headers = ['Cancer', 'SNP epistasis', 'Odds ratio', 'P_epistasis', 'Best SNP', 'P-joint', 'P-boost', 'P-saige'];
                const rows = this.snpEpiTableData.map(item => [
                    item.Cancertype,
                    item.SNPepi,
                    item.OR_INT !== undefined ? item.OR_INT.toFixed(2) : (item.OR !== undefined ? item.OR.toFixed(2) : ''),
                    item.P_epistasis !== undefined ? item.P_epistasis.toExponential(2) : (item.P !== undefined ? item.P.toExponential(2) : ''),
                    item.Best_snp,
                    item.P_joint !== undefined ? item.P_joint.toExponential(2) : '',
                    item.P_boost !== undefined ? item.P_boost.toExponential(2) : '',
                    item.P_saige !== undefined ? (item.P_saige === 0 ? '0' : item.P_saige.toExponential(2)) : (item.saige_p !== undefined ? item.saige_p.toExponential(2) : '')
                ]);

                let csvContent = "data:text/csv;charset=utf-8,"
                    + headers.join(",") + "\n"
                    + rows.map(e => e.join(",")).join("\n");

                const encodedUri = encodeURI(csvContent);
                const link = document.createElement("a");
                const fileName = `epistasis_results_${new Date().getTime()}.csv`;

                link.setAttribute("href", encodedUri);
                link.setAttribute("download", fileName);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            },

            resultsDownload() {
                const queryID = this.$route.params.queryID;
                axios({
                    url: `api/snpGWASdownloadCSV?queryID=${encodeURIComponent(queryID)}`,
                    method: 'GET',
                    responseType: 'blob',
                }).then((response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', `${queryID}_GWAS_res.csv`);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);
                }).catch(error => console.error('Download error:', error));
            },

            handleDownloadSample() {
                this.downloadClickedSample = true; 
                this.SampledownloadPdf();
            },

            handleDownloadOR() {
                this.downloadClickedOR = true; 
                this.ORdownloadPdf();
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
                    ).catch(() => {});
                });
            },

            fetchPdfOR(Cancertype, SNPepi, ORstatus) {
                if (ORstatus === false) {
                    this.showAlert = true;
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
                });
            },

            closeAlert() {
                this.showAlert = false;
            },

            stopPropagation(event) {
                event.stopPropagation();
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
            },

            currentGWASChange(value) {
                this.currentGWASPage = value;
                this.fetchGWASData();
            },

            currentEpiChange(value) {
                this.currentEpiPage = value;
                this.fetchEpiData();
            },

            fetchGWASData() {
                const queryID = this.$route.params.queryID;
                this.loading = true;
                axios.get('api/quickSearchSnpEpistasis', {
                    params: {
                        'queryID': queryID,
                        'page': this.currentGWASPage,
                        'perPage': 20
                    }
                }).then(
                    response => {
                        this.snpGWASData = response.data.SNPGWASPosition;
                        this.recordNumber = response.data.recordsNumber;
                        this.loading = false;
                    },
                    error => {
                        console.log("请求失败", error.message);
                        this.loading = false;
                    }
                );
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

            fetchEpiData() {
                const queryID = this.$route.params.queryID;
                this.loading = true;
                axios.get('api/quickSearchSnpEpistasis', {
                    params: {
                        'queryID': queryID,
                        'page': this.currentEpiPage,
                        'perPage': 20
                    }
                }).then(
                    response => {
                        this.snpEpiTableData = response.data.SNPEpiTable;
                        this.snpEpiNetworkData = response.data.SNPEpiNetwork;
                        this.epiRecordNumber = response.data.epiRecordsNumber;
                        this.initializeHighcharts();
                        this.loading = false;
                    },
                    error => {
                        console.log("请求失败", error.message);
                        this.loading = false;
                    }
                );
            },

            initializeHighcharts() {
                const querySNP = this.currentSNP;
                const epiData = this.snpEpiNetworkData || [];

                let data = [];
                let nodes = [];

                if (epiData.length > 0) {
                    data = epiData.map(item => {
                        const snps = item.SNPepi.split('_');
                        return [snps[0], snps[1]];
                    });
                    nodes = data.flatMap(edge => edge.map(snp => ({
                        id: snp,
                        color: snp === querySNP ? '#B2B2FF' : '#ff0000'
                    })));
                } else {
                    data = [];
                    nodes = [{ id: `${querySNP} Result is null！`, color: '#ff0000' }];
                }

                Highcharts.chart('container', {
                    chart: {
                        type: 'networkgraph',
                        marginTop: 120
                    },
                    title: {
                        text: `The epistasis network associated with ${querySNP}`
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        networkgraph: {
                            keys: ['from', 'to'],
                            layoutAlgorithm: {
                                enableSimulation: true,
                                integration: 'verlet',
                                linkLength: 200 
                            },
                            dataLabels: {
                                enabled: true,
                                style: {
                                    fontSize: '15px',
                                    color: '#000000' 
                                },
                                formatter: function() {
                                    if (this.key === querySNP) {
                                        return `<span style="color: #ff0000">${this.key}</span>`;
                                    }
                                    return this.key;
                                }
                            }
                        }
                    },
                    series: [{
                        marker: {
                            radius: 13,
                        },
                        dataLabels: {
                            enabled: true,
                            linkFormat: '',
                            allowOverlap: true,
                            style: {
                                fontSize: '15px',
                                color: '#000000'
                            },
                            formatter: function() {
                                if (this.key === querySNP) {
                                    return `<span style="color: #ff0000">${this.key}</span>`;
                                }
                                return this.key;
                            }
                        },
                        data: data,
                        nodes: nodes
                    }]
                });
            },
        },
        mounted() {
            const queryID = this.$route.params.queryID;
            this.currentSNP = queryID;
            console.log("mounted params:", {
                queryID: queryID,
                page: 1,
                perPage: 20
            });
            this.fetchGWASData();
            this.fetchEpiData();
        }
    }
</script>

<style scoped>
    /* 灰色星星样式 */
    .star-gray {
        color: #ccc;
    }

    /* 黄色星星样式 */
    .star-yellow {
        color: #ffd700;
    }

    /* 星星容器样式 */
    .stars-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .content-container {
        width: 1140px;
        margin: 0 auto;
        display: flex;
        font-family: 'Helvetica';
    }

    /* download style */    
    .el-button--primary {
        border-color: transparent;
    }

    .header-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0px;
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
        width: 45%;
        height: 40px;
        line-height: 40px;
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
        width: 45%;
        height: 40px;
        line-height: 0px;
    }

    .el-table th .cell, .el-table td .cell {
        font-size: 15px !important;
    }

    .cancel-button:hover, 
    .cancel-button:focus, 
    .cancel-button:active {
        background-color: #77acf1;
        border-color: #77acf1;
    }

    .input-label {
        display: block;
        margin-bottom: 10px;
        font-size: 17px;
        color: #FA8072;
        font-weight: bold;
        font-family: 'Helvetica';
    }

    .search-container {
        width: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .network-container {
        width: 840px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #container {
        width: 100%;
        height: 400px;
    }

    .custom-column-header {
        background-color: #f5f5f5;
        font-weight: bold;
        text-align: center;
        font-family: 'Helvetica';
    }

    .custom-column-header .cell {
        font-size: 15px; 
    }

    .el-icon-zoom-in {
        color: #FF7C43;
        font-size: 1.2em;
    }

    .custom-icon {
        font-size: 20px;
        font-weight: bold;
    }

    .download-button {
        background-color: #A2D9CE; 
        border: 2px solid #A2D9CE; 
        color: black;
        font-size: 16px;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s, border-color 0.3s; 
        font-family: 'Helvetica';
    }

    .download-button:active, .download-button.clicked {
        background-color: #C3DEF1;  
        border-color: #C3DEF1;
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
        font-family: 'Helvetica';
    }

    .text-black {
        display: block;
        color: black;
        cursor: pointer;
        margin-top: 8px;
        font-family: 'Helvetica';
    }

    .text-orange {
        display: block;
        color: orange;
        cursor: pointer;
        margin-top: 8px;
        font-family: 'Helvetica';
    }

    .box-card {
        margin: 5px 0;
        padding: 10px;
        font-family: 'Helvetica';
    }
</style>