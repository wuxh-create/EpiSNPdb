<template>
    <div>
        <el-card class="box-card">
            <el-row style="background-color: #F0F0F0; height: 50px; text-align: left; line-height: 50px; border: 1px solid #D9D9D9; border-radius: 5px 5px 0px 0px; margin-top: 1px">
                <el-col :span="21">
                    <span style="padding: 0px 20px; font-weight: bold; color: brown;">SNP GWAS results</span>
                </el-col>
                <el-col :span="2">
                    <el-link :underline="false" @click="resultsDownload">
                        <span style="padding: 0px 20px; color: brown;"><strong style="font-size:16px">Download</strong></span>
                    </el-link>
                </el-col>
            </el-row>
            <el-row style="border-radius: 0px 0px 5px 5px; border: 1px solid #D9D9D9;">
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
                        width="130"
                        align="center">
                        <template v-slot="props">
                            <a target="_blank" :href="'https://www.ncbi.nlm.nih.gov/snp/' + props.row.SNP">{{ props.row.SNP }}</a>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="Position"
                        width="140"
                        align="center">
                        <template v-slot="scope">
                            <a target="_blank" :href="'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=' + scope.row.Position">
                            {{ scope.row.Pos }} : {{ scope.row.POS }}
                            </a>
                        </template>
                    </el-table-column>
                    <el-table-column
                        prop="Alleles"
                        label="Alleles(A/a)"
                        width="105"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="MAF"
                        label="MAF"
                        width="70"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="A1"
                        label="A1"
                        width="50"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="A2"
                        label="A2"
                        width="50"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="AF1"
                        label="AF1"
                        width="70"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="BETA"
                        label="Beta"
                        width="70"
                        align="center">
                    </el-table-column>
                    <el-table-column
                        prop="P"
                        label="P_value"
                        width="85"
                        align="center">
                        <template v-slot="scope">
                            {{ parseFloat(scope.row.P).toFixed(4) }}
                        </template>
                    </el-table-column>
                    <el-table-column
                        prop="N"
                        label="Sample"
                        width="105"
                        align="center">
                    </el-table-column>
                    <el-table-column prop="sample" label="Sample" width="88" align="center">
                        <template v-slot="scope">
                            <el-button size="small" @click="fetchPdf(scope.row.Cancertype, scope.row.SNP)">Plot</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    :hide-on-single-page="true"
                    :total="recordNumber"
                    :page-size="8"
                    :current-page="1"
                    @current-change="currentChange"
                    layout="prev, pager, next">
                </el-pagination>
            </el-row>
            
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
    </div>
</template>



<script>
    import axios from 'axios'
    // import pdfjsLib from 'pdfjs-dist'
    export default {
        name:"quickSearch",
        data(){
            return {
                snpGWASData: [],
                loading: false,
                recordNumber: 0,
                pdfDialogVisible: false, // Controls visibility of the PDF dialog
                imageUrl: '', // 存储图片URL
                imageDialogVisible: false, // 控制图片对话框的显示
                downloadClicked: false,
                cancerTypes: [
                    "Bladder", "Brain", "Breast", "Cancertype", "Cervical", "Colon", "Esophagus",
                    "Kidney", "Liver", "Lung", "Melanoma", "Ovarian", "Pancreatic", "Prostate",
                    "Rectal", "Stomach", "Uterine"
                ],
            };
        },
        methods:{
            exportCsv(){
                const header = {"Cancer type":"Cancer type", "SNP":"SNP", "Position":"Position","Alleles(A/a)":"Alleles(A/a)","Sample":"Sample",
                "Beta":"Beta","SE":"SE","P-value":"P-value","CONVERGE":"CONVERGE"}
                export_csv(header, this.tableData)
                function export_csv(header,data){
                    let csv = '';
                    for (let key in header){
                        csv += header[key] + ',';
                    }
                    csv = csv.substr(0,csv.length - 1) + '\r\n';
                    for (let i in data){
                        for (let key in header){
                            csv += data[i][key].replace(',',';') + ','
                        }
                        csv = csv.substr(0, csv.length -1) + '\r\n'
                    }
                    //定义文件内容，类型必须为Bolb，否则createObjectURL会报错
                    let content = new Blob(['\uFEFF' + csv])
                    //生成url对象
                    let urlObject = window.URL || window.webkitURL || window
                    let url = urlObject.createObjectURL(content)
                    //生成<a></a>DOM元素
                    let el = document.createElement('a')
                    //链接赋值
                    el.href = url
                    el.download = "snpGWAS.csv"
                    //必须点击否则不会下载
                    el.click()
                    //移除链接释放资源
                    urlObject.revokeObjectURL(url)
                }
            },
            resultsDownload(){},
            handleDownload() {
                this.downloadClicked = true; // 将按钮状态更新为点击
                this.downloadPdf();
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
                    this.downloadClicked = false; // 如果下载失败, 重置点击状态
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
            handleClose() {
                this.imageDialogVisible = false; // 确保对话框被隐藏
                this.downloadClicked = false;
                // 可选的清理操作
                if (this.imageUrl) {
                    URL.revokeObjectURL(this.imageUrl); // 释放Blob URL以节省资源
                    this.imageUrl = ''; // 清除图片URL
                }
            },
            // 与后端通信和参数传递的部分
            currentChange(value){
                // 处理分页时的页码变化
                // 当分页组件的当前页发生变化时，此方法会被触发。
                // 方法中的value参数是新的页码。
                console.log("currentChange params:", {
                    queryID: this.$route.params.queryID,
                    page: value,
                    perPage: 8
                });
                axios.get('api/quickSearch',{
                    params:{
                        'queryID':this.$route.params.queryID,
                        'page':value,
                        'perPage':8
                    }
                    // 使用axios.get向后端发送请求，请求URL和mounted方法中相同，但页码page是根据分页组件的当前页动态变化的。
                }).then(
                    response => {
                        console.log("请求成功",response.data)
                        this.snpGWASData = response.data.SNPGWAS
                        this.recordNumber = response.data.recordsNumber
                    },
                //    响应成功后，同样更新this.snpGWASData和this.recordNumber以反映新的数据。
                    error => {
                        console.log("请求失败",error.message)
                    }
                )
            },
        },
        mounted(){
            console.log("mounted params:", {
                queryID: this.$route.params.queryID,
                page: 1,
                perPage: 8
            });
            axios.get('api/quickSearch',{
                params:{
                    'queryID':this.$route.params.queryID,
                    'page':1,
                    'perPage':8
                }
            }).then(
                response => {
                    console.log("请求成功",response.data),
                    this.snpGWASData = response.data.SNPGWAS,
                    this.recordNumber = response.data.recordsNumber
                },
                 // 成功获取响应后，将响应数据存储到this.snpGWASData和this.recordNumber中，用于渲染页面。
                error => {
                    console.log("请求失败",error.message)
                }
            )
        }
    }
</script>


<style>
.download-button {
    background-color: #A2D9CE;  /* 初始背景颜色 */
    border: 2px solid #A2D9CE;  /* 初始边框颜色 */
    color: black;
    font-size: 16px;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s; /* 平滑过渡效果 */
}

.download-button:active, .download-button.clicked {
    background-color: #C3DEF1;  /* 点击时的背景和边框颜色 */
    border-color: #C3DEF1;
}

::v-deep .el-table thead th {
  color: #2d4059 !important;
  font-family: 'Helvetica';
  font-weight: bold;
}
</style>



