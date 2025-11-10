<template>
    <div>
        <!-- 动态效果的容器 -->
        <div class="content-container">
            <el-row>
                <!-- 左边的查询搜索框 -->
                <el-col :span="6" class="search-container">
                    <!-- 查询搜索框内容 -->
                    <!-- 假设这里放置查询搜索框的内容 -->
                    <el-input placeholder="Search..." v-model="searchQuery" clearable></el-input>
                    <el-button type="primary" style="background-color: #FF7F7F; border-color: #FF7F7F;" @click="handleSearch">Submit</el-button>
                    <el-button style="background-color: #87CEFA; border-color: #87CEFA;" @click="handleCancel">Cancel</el-button>
                </el-col>
                
                <!-- 右边的动态网络图 -->
                <el-col :span="18" class="network-container">
                    <div id="container"></div>
                </el-col>
            </el-row>
        </div>
        <el-card class="box-card" style="margin-top: 20px; width: 1140px;">
            <el-row style="background-color: #ACD1E9; height: 50px; text-align: left; line-height: 50px; border: 1px solid #ACD1E9; 
            border-radius: 5px 5px 0px 0px;margin-bottom: 0px;">
                <el-col :span="21">
                    <span style="padding: 0px 20px; font-weight: bold; color: #29506D;font-size:21px">Epistasis results</span>
                </el-col>
            </el-row>
            <el-row style="border-radius: 0px 0px 5px 5px; border: 1px solid #D6EADF;margin-bottom: 0px;">
                <el-table
                    v-loading="loading"
                    border
                    :data="snpEpiTableData"
                    style="width: 100%;"
                    max-height="500"
                    stripe>
                    <el-table-column
                        prop="Cancertype"
                        label="Cancer"
                        width="105"
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
                    <el-table-column prop="SNPepi" label="SNP Epistasis" width="260" align="center" class-name="custom-column-header">
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
                    <el-table-column prop="OR" label="OR" width="73" align="center" class-name="custom-column-header">
                            <template v-slot:header>
                            OR
                            <el-tooltip class="item" effect="dark" content="OR calculated by PLINK" placement="top">
                            <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                            <template v-slot="scope">
                            {{ scope.row.OR !== undefined ? scope.row.OR.toFixed(2) : '' }}
                        </template>
                        </el-table-column>
                        <el-table-column prop="STAT" label="STAT" width="78" align="center" class-name="custom-column-header">
                            <template v-slot:header>
                                STAT
                            <el-tooltip class="item" effect="dark" content="STAT calculated by PLINK" placement="top">
                            <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.STAT !== undefined ? scope.row.STAT.toFixed(2) : '' }}
                        </template>
                        </el-table-column>
                        <el-table-column prop="P" label="P-value" width="130" sortable align="center" show-overflow-tooltip class-name="custom-column-header">
                        <template v-slot:header>
                            P-value
                            <el-tooltip class="item" effect="dark" content="P-value calculated by PLINK" placement="top">
                            <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.P !== undefined ? scope.row.P.toExponential(2) : '' }}
                        </template>
                        </el-table-column>
                        <el-table-column prop="Best_snp" label="Best SNP" width="125" align="center" class-name="custom-column-header">
                        <template v-slot:header>
                            Best SNP
                            <el-tooltip class="item" effect="dark" content="The SNP identifier of the best SNP identified by PLINK" placement="top">
                            <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        </el-table-column>
                        <el-table-column prop="saige_p" label="P-saige" width="130" sortable align="center" class-name="custom-column-header">
                        <template v-slot:header>
                            P_saige
                            <el-tooltip class="item" effect="dark" content="P-value calculated by SAIGE" placement="top">
                            <i class="el-icon-question"></i>
                            </el-tooltip>
                        </template>
                        <template v-slot="scope">
                            {{ scope.row.saige_p !== undefined ? scope.row.saige_p.toExponential(2) : '' }}
                        </template>
                        </el-table-column>
                    <!-- <el-table-column prop="IsSPA" label="Is.SPA" width="89" align="center" class-name="custom-column-header">
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
                    <el-table-column prop="alleles1" label="Sample" width="87" align="center" class-name="custom-column-header">
                    <template v-slot="scope">
                        <a-icon type="fund" theme="twoTone" 
                        @click="fetchPdfSample(scope.row.Cancertype, scope.row.SNPepi)" 
                        style="font-size: 2.3em; cursor: pointer; color: #AED4D4;" />
                    </template>
                    </el-table-column>
                    <el-table-column prop="alleles1" label="OR_plot" width="87" align="center" class-name="custom-column-header">
                    <template v-slot="scope">
                        <a-icon type="bar-chart" theme="outlined"
                        @click="fetchPdfOR(scope.row.Cancertype, scope.row.SNPepi)" 
                        style="font-size: 2.5em; cursor: pointer; color: blue;" 
                        />
                    </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    :hide-on-single-page="true"
                    :total="epiRecordNumber"
                    :page-size="8"
                    :current-page="currentEpiPage"
                    @current-change="currentEpiChange"
                    layout="prev, pager, next">
                </el-pagination>
            </el-row>
            <el-dialog 
                :visible.sync="imageDialogVisibleSample" 
                :style="{ maxWidth: '700px', margin: '0 auto' }" 
                width="auto" 
                @close="handleCloseSample" 
                :close-on-click-modal="false" 
                :close-on-press-escape="true" 
                :modal-append-to-body="useModalAppendToBody"
            >
                <div style="display: flex; flex-direction: column; align-items: center; position: relative;">
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
                <div style="display: flex; flex-direction: column; align-items: center; position: relative;">
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
                    <strong style="color: black;">sample filtration</strong>in the context of the current cancer phenotype.
                    </div>
                    <el-button @click="closeAlert" style="margin-top: 20px;">OK</el-button>
                </div>
            </div>
            <el-dialog :visible.sync="imageDialogVisible" :style="{ maxWidth: '560px', margin: '0 auto' }" width="auto" @close="handleClose">
                <div style="text-align: center;">
                    <img :src="imageUrl" style="width: 530px; height: 500px; object-fit: contain;" alt="Image Preview">
                    <!-- 下载按钮 -->
                    <button class="download-button"
                            :class="{ 'clicked': downloadClicked }"
                            @click="handleDownload">
                        Download
                    </button>
                </div>
            </el-dialog>
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
                    style="width: 100%;"
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
                        width="158"
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
                        width="99"
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
                        width="95"
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
                        width="113"
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
                        width="60"
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
                            <a-icon type="bar-chart" theme="outlined" @click="fetchPdf(scope.row.Cancertype, scope.row.SNP)" style="font-size: 2.7em; cursor: pointer; color: blueviolet;"/>
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
                    :page-size="8"
                    :current-page="currentGWASPage"
                    @current-change="currentGWASChange"
                    layout="prev, pager, next">
                </el-pagination>
            </el-row>
            
            <el-dialog :visible.sync="imageDialogVisible" :style="{ maxWidth: '560px', margin: '0 auto' }" width="auto" @close="handleClose">
                <div style="text-align: center;">
                    <img :src="imageUrl" style="width: 530px; height: 500px; object-fit: contain;" alt="Image Preview" @click="imageDialogVisible = false">
                    <!-- 下载按钮 -->
                    <button class="download-button"
                            :class="{ 'clicked': downloadClicked }"
                            @click="handleDownload">
                        Download
                    </button>
                </div>
            </el-dialog>
        </el-card>
    </div>
</template>

<script>
    import axios from 'axios';
    import Highcharts from 'highcharts';
    import Networkgraph from 'highcharts/modules/networkgraph';

    Networkgraph(Highcharts);

    export default {
        name: "quickSearchCancer",
        props: {
            speciesName: {
                type: String,
                default: null
            }
        },
        data() {
            return {
                snpGWASData: [], 
                snpEpiTableData: [],
                snpEpiNetworkData: [],
                loading: false,
                recordNumber: 0,
                epiRecordNumber: 0, // 新增：用于Epistasis结果的分页
                pdfDialogVisible: false,
                imageUrl: '',
                imageDialogVisible: false,
                downloadClicked: false,
                currentSNP: '',
                currentGWASPage: 1,
                currentEpiPage: 1,
                imageDialogVisibleSample: false,
                imageDialogVisibleOR: false,
                imageUrl: '',
                downloadClickedSample: false,
                downloadClickedOR: false,
                useModalAppendToBody: false,
                showAlert: false,
                useModalAppendToBody: false,
                cancerTypes: [
                    "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
                    "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
                    "Rectal", "Stomach", "Uterine"
                ],
            };
        },
        methods: {
            initializeHighcharts() {
                const querySNP = this.currentSNP;
                const epiData = this.snpEpiNetworkData || [];
                const cancerType = this.speciesName || this.$route.params.speciesName || this.$route.params.queryID;

                let data = [];
                let nodes = [];

                if (epiData.length > 0) {
                    data = epiData.map(item => {
                        const snps = item.SNPepi.split('_');
                        return [snps[0], snps[1]];
                    });
                    nodes = data.flatMap(edge => edge.map(snp => ({
                        id: snp,
                        color: snp === querySNP ? '#ff0000' : '#B2B2FF'
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
                        text: `The epistasis network associated with ${cancerType}`
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
                                linkLength: 100
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
            resultsDownload() {
                const queryID = this.$route.params.queryID; // 获取当前查询的ID
                axios({
                    url: `api/snpGWASdownloadCSV?queryID=${encodeURIComponent(queryID)}`,
                    method: 'GET',
                    responseType: 'blob', // 重要，因为我们希望接收的是文件
                }).then((response) => {
                    // 创建一个URL链接并模拟点击进行下载
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', `${queryID}_GWAS_res.csv`); // 设定下载文件名
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
            fetchPdfOR(Cancertype, SNPepi) {
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
                this.loading = true;
                this.currentGWASPage = value;
                axios.get('api/quickSearchCancer', {
                    params: {
                        'cancertype': this.$route.params.queryID,
                        'page': value,
                        'perPage': 8
                    }
                }).then(
                    response => {
                        this.snpGWASData = response.data.CancerGWAS;
                        this.recordNumber = response.data.recordsNumber;
                        this.loading = false;
                    },
                    error => {
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
            handleOutsideClick(event) {
                const dialogElement = event.target.closest('.el-dialog');
                if (!dialogElement) {
                    this.handleClose();
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
            currentEpiChange(value) {
                const cancertype = this.speciesName || this.$route.params.speciesName || this.$route.params.queryID;
                if (!cancertype) {
                    return;
                }
                this.loading = true;
                this.currentEpiPage = value;

                axios.get('api/quickSearchCancer', {
                    params: {
                        'cancertype': cancertype,
                        'page': value,
                        'perPage': 8
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
                        this.loading = false;
                    }
                );
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
            handleClose() {
                this.imageDialogVisible = false;
            },
            handleDownload() {
                this.downloadClicked = true;
                const link = document.createElement('a');
                link.href = this.imageUrl;
                link.download = `${this.currentCancertype}_${this.currentSNP}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                this.downloadClicked = false;
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
                    ).catch(() => {}); 
                });
            },
            fetchPdfOR(Cancertype, SNPepi) {
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
        },
        mounted() {
            this.currentGWASChange(1);
            this.currentEpiChange(1);
        }
    }
</script>

<style scoped>
    .content-container {
        width: 1140px;
        margin: 0 auto;
        display: flex;
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
    .custom-column-header .cell {
        font-size: 15px; 
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
    }
</style>
