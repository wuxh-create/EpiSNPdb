<template>
    <div>
        <div class="content-container">
            <div class="home-search" style="margin: 40px 0;">
                <el-row class="row-bg" justify="center" align="middle" type="flex">
                    <el-col :span="16" :offset="1">
                        <el-input 
                            v-model="input" 
                            placeholder="Single Variant ID, Single Variant Position, Epistasis or Trait" 
                            class="search-input" 
                            ref="searchInput"
                            style="font-size: 13px; font-family: Helvetica;" 
                        >
                            <el-button 
                                slot="append" 
                                icon="ant-design:search-outlined"
                                @click.prevent="quickSearch" 
                                style="background-color: #95E1D3; color: black; border-radius: 0;height: 100%;font-size:18px;"
                            >
                            Search
                            </el-button>
                        </el-input>
                        <div class="input-examples" style="font-size: 19px; margin-top: 5px;margin-bottom: 0px; font-family: Helvetica;"> 
                            <span>Input examples: </span>
                            <span :class="{ 'selected': isSelected('rs12924101') }" @mouseover="fillInput('rs12924101')">rs12924101, </span>
                            <span :class="{ 'selected': isSelected('chr1:1003629-1003739') }" @mouseover="fillInput('chr1:1003629-1003739')">chr1:1003629-1003739, </span>
                            <span :class="{ 'selected': isSelected('rs6687430_rs17781327') }" @mouseover="fillInput('rs6687430_rs6687430_rs17781327')">rs6687430_rs17781327, </span>
                            <span :class="{ 'selected': isSelected('Breast') }" @mouseover="fillInput('Breast')">Breast</span>
                        </div>
                    </el-col>
                </el-row>
            </div>


            <div class="panel" style="margin-top: 2px;">
                <div class="panel-header" style="font-family: Helvetica;">
                    <span v-pre style="font-family: Helvetica;">
                        Welcome to the EpiSNP-db database
                    </span>
                </div> 
                <div class="panel-body" >
                    <div style="font-family: Helvetica;">
                        SNP-SNP interaction (Epistasis) refers to any non-additive interactions between two loci that affect the same trait. 
                        Recent studies have revealed that epistasis is associated with the invasiveness of various cancers and is a significant factor contributing to cancer. 
                        Therefore, the identification and characterization of epistasis are important for cancer research. 
                        However, the analysis of epistasis in cancer within large-scale populations remains highly limited.
                    </div>
                    <div style="height: 12px; width: 70%;"></div>
                    <div style="display: flex;">
                        <div style="width: 78%;">
                            <div class="text-section" style="font-family: Helvetica;">
                                <span class="badge alert-info" v-pre style="background-color: #F92A82; color: white; padding: 1px 2px; border-radius: 4px;">EpiSNP-db</span> is designed to investigate the effects of epistasis on cancer phenotypes. 
                                We have systematically identified epistasis associated with 16 cancer types. 
                                Furthermore, we have systematically analyzed their effects on survival and deciphered their functions by integrating other data and mapping to GWAS regions.
                            </div>
                            <div style="height: 12px;"></div>
                            <div class="text-section" style="font-family: Helvetica;">
                                <strong>In EpiSNP-db, users can:</strong><span class="badge alert-info" v-pre></span>
                            </div>
                            <div style="margin-top: 10px;font-family: Helvetica;">
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-search" style="color: red; font-size: 20px;"></i>
                                &nbsp;&nbsp;Browse or search for <span class="badge alert-info" v-pre style="background-color: #FF5964; color: white; padding: 1px 2px; border-radius: 4px;">epistatic SNPs (epiSNPs)</span> across different cancer types;
                                <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-search" style="color: red; font-size: 20px;"></i>
                                &nbsp;&nbsp;Browse or search for the <span class="badge alert-info" v-pre style="background-color: #FF9933; color: white; padding: 1px 2px; border-radius: 4px;">annotation</span> of epiSNPs across different cancer types;
                                <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-search" style="color: red; font-size: 20px;"></i>
                                &nbsp;&nbsp;Browse or search for <span class="badge alert-info" v-pre style="background-color: #35A7FF; color: white; padding: 1px 2px; border-radius: 4px;">epiSNP-related GWAS loci</span> across different cancer types;
                                <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-search" style="color: red; font-size: 20px;"></i>
                                &nbsp;&nbsp;Browse or search for <span class="badge alert-info" v-pre style="background-color: #ffa0c2; color: white; padding: 1px 2px; border-radius: 4px;">survival-related epiSNPs</span> across different cancer types;
                                <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-download" style="color: red; font-size: 20px;"></i>
                                &nbsp;&nbsp;<span class="badge alert-info" v-pre style="background-color: #CC99CC; color: white; padding: 1px 2px; border-radius: 4px;">Download</span> figures and the results of epistasis analyses.
                            </div>
                        </div>
                        <div style="width: 34%; margin-left: 30px;padding: 15px;">
                            <img src="EpiSNP-db/home_epistasis.svg" alt="Image description" style="max-width: 100%; height: auto;">
                        </div>
                    </div>
                </div>
            </div>






            
            <!-- First Row -->
            <div class="panel">
                <div class="panel-header">
                    <span style="font-family: Helvetica;">
                        Browse by cancer type
                    </span>
                </div> 
                <div class="panel-body">
                    <el-row gutter="20">
                        <el-col v-for="(item, index) in speciesList.slice(0, 6)" :key="index" :span="4">
                            <div class="card" @click="handleImageClick(item.name)" @mouseover="showDetails(index)" @mouseleave="hideDetails(index)">
                                <img :src="item.image" class="card-img-top" :alt="item.name">
                                <div class="card-body">
                                    <h5 class="card-title" style="font-family: Helvetica;">{{ item.name }}</h5>
                                    <div v-show="item.showDetails" class="card-text" style="font-family: Helvetica;">
                                        <p>{{ item.descriptionLine1 }}</p>
                                        <p>{{ item.descriptionLine2 }}</p>
                                        <p>{{ item.descriptionLine3 }}</p>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                    
                    <!-- Second Row -->
                    <el-row gutter="20">
                        <el-col v-for="(item, index) in speciesList.slice(6, 12)" :key="index" :span="4">
                            <div class="card" @click="handleImageClick(item.name)" @mouseover="showDetails(index + 6)" @mouseleave="hideDetails(index + 6)">
                                <img :src="item.image" class="card-img-top" :alt="item.name">
                                <div class="card-body">
                                    <h5 class="card-title" style="font-family: Helvetica;">{{ item.name }}</h5>
                                    <div v-show="item.showDetails" class="card-text" style="font-family: Helvetica;">
                                        <p>{{ item.descriptionLine1 }}</p>
                                        <p>{{ item.descriptionLine2 }}</p>
                                        <p>{{ item.descriptionLine3 }}</p>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                    
                    <!-- Third Row -->
                    <el-row gutter="20" justify="start">
                        <el-col v-for="(item, index) in speciesList.slice(12)" :key="index" :span="4">
                            <div class="card" @click="handleImageClick(item.name)" @mouseover="showDetails(index + 12)" @mouseleave="hideDetails(index + 12)">
                                <img :src="item.image" class="card-img-top" :alt="item.name">
                                <div class="card-body">
                                    <h5 class="card-title" style="font-family: Helvetica;">{{ item.name }}</h5>
                                    <div v-show="item.showDetails" class="card-text" style="font-family: Helvetica;">
                                        <p>{{ item.descriptionLine1 }}</p>
                                        <p>{{ item.descriptionLine2 }}</p>
                                        <p>{{ item.descriptionLine3 }}</p>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </div>

            <!-- Data summary section -->
            <div class="panel data-summary">
                <div class="panel-header" style="font-family: Helvetica;">
                    Data summary
                </div>
                <div class="panel-body">
                    <el-row type="flex">
                        <el-col :span="6" :offset="1">
                            <el-row type="flex" justify="center">
                                <h1 style="font-size: 20px;font-family: Helvetica;">
                                    EpiSNP-db Statistics
                                </h1>
                            </el-row>
                            <div class="innerBody">
                                <el-table :data="showData" style="width: 100%">
                                    <el-table-column
                                        prop="name"
                                        label="Category"
                                        width="143" 
                                        :header-cell-style="{ backgroundColor: '#F5DBCB', color: 'white' }">
                                        <template slot-scope="scope">
                                            <span :style="{ color: getColor(scope.row.name) }">{{ scope.row.name }}</span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                        prop="number"
                                        label="Total"
                                        width="126" 
                                        :header-cell-style="{ backgroundColor: '#004D40', color: 'white' }">
                                        <template slot-scope="scope">
                                            <span :style="{ color: getColor(scope.row.number) }">{{ scope.row.number }}</span>
                                        </template>
                                    </el-table-column>
                                </el-table>

                            </div>
                        </el-col>
                        <el-col :span="15" :offset="1">
                            <el-carousel indicator-position="outside">
                                <el-carousel-item v-for="item in chartTitles" :key="item.id">
                                    <div class="carousel-item-container">
                                        <h1 class="carousel-title" style="font-size: 20px;font-family: Helvetica;">{{ item.title }}</h1>
                                        <div :id='"option"+item.id' class="carousel-chart"></div>
                                    </div>
                                </el-carousel-item>
                            </el-carousel>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import 'animate.css'
import Vue from 'vue';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import { Icon } from 'ant-design-vue';

Vue.use(Antd);
Vue.component('a-icon', Icon);

export default {
    name: 'Home',
    data() {
        return {
            input: '',
            chartSample: null,
            chartInteraction: null,
            charQTL: null,
            showData: [
                { name: "Cancer type", number: "16" },
                { name: "Cancer samples", number: "82,018" },
                { name: "GWAS loci", number: "174,172" },
                { name: "Interaction Pairs", number: "147,782" },
            ],
            chartTitles: [
                { id: 1, title: "The number of cancer samples across 16 cancers" },
                { id: 2, title: "The number of identified epiSNPs across 16 cancer types" },
                { id: 3, title: "The number of epiSNP related GWAS loci across 16 cancer types" }
            ],
            speciesList: [
                { name: 'Breast', image: 'EpiSNP-db/Breast.png', descriptionLine1: 'Case=19,207', descriptionLine2: 'Control=161,999', descriptionLine3: 'epiSNPs=10,605', showDetails: false },
                { name: 'Prostate', image: 'EpiSNP-db/Prostate.png', descriptionLine1: 'Case=14,466', descriptionLine2: 'Control=136,966', descriptionLine3: 'epiSNPs=11,461', showDetails: false },
                { name: 'Melanoma', image: 'EpiSNP-db/Melanoma.png', descriptionLine1: 'Case=8,416', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,080', showDetails: false },
                { name: 'Colon', image: 'EpiSNP-db/Colon.png', descriptionLine1: 'Case=6,834', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=9,718', showDetails: false },
                { name: 'Cervical', image: 'EpiSNP-db/Cervical.png', descriptionLine1: 'Case=6,740', descriptionLine2: 'Control=161,999', descriptionLine3: 'epiSNPs=11,027', showDetails: false },
                { name: 'Lung', image: 'EpiSNP-db/Lung.png', descriptionLine1: 'Case=4,960', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,970', showDetails: false },
                { name: 'Bladder', image: 'EpiSNP-db/Bladder.png', descriptionLine1: 'Case=4,128', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,224', showDetails: false },
                { name: 'Rectal', image: 'EpiSNP-db/Rectal.png', descriptionLine1: 'Case=3,142', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,470', showDetails: false },
                { name: 'Uterine', image: 'EpiSNP-db/Uterine.png', descriptionLine1: 'Case=2,768', descriptionLine2: 'Control=161,999', descriptionLine3: 'epiSNPs=10,661', showDetails: false },
                { name: 'Kidney', image: 'EpiSNP-db/Kidney.png', descriptionLine1: 'Case=2,314', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,841', showDetails: false },
                { name: 'Ovarian', image: 'EpiSNP-db/Ovarian.png', descriptionLine1: 'Case=2,182', descriptionLine2: 'Control=161,999', descriptionLine3: 'epiSNPs=10,526', showDetails: false },
                { name: 'Pancreatic', image: 'EpiSNP-db/Pancreatic.png', descriptionLine1: 'Case=1,668', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=10,681', showDetails: false },
                { name: 'Esophagus', image: 'EpiSNP-db/Esophagus.png', descriptionLine1: 'Case=1,609', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=11,563', showDetails: false },
                { name: 'Stomach', image: 'EpiSNP-db/Stomach.png', descriptionLine1: 'Case=1,305', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=11,369', showDetails: false },
                { name: 'Brain', image: 'EpiSNP-db/Brain.png', descriptionLine1: 'Case=1,157', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=11,605', showDetails: false },
                { name: 'Liver', image: 'EpiSNP-db/Liver.png', descriptionLine1: 'Case=1,122', descriptionLine2: 'Control=298,965', descriptionLine3: 'epiSNPs=11,371', showDetails: false },
            ]
        }
    },
    methods: {
        getColor(value) {
            if (value === 'Cancer type' || value === '16') return '#FF9933';
            if (value === 'Cancer samples' || value === '82,018') return 'red';
            if (value === 'GWAS loci' || value === '174,172') return 'blue';
            if (value === 'Interaction Pairs' || value === '147,782') return '#7dce94';
            return 'black';
        },
        determineQueryType(input) {
            const cancerTypes = [
                'Bladder', 'Brain', 'Breast', 'Lung', 'Cervical',
                'Colon', 'Melanoma', 'Esophagus', 'Kidney',
                'Liver', 'Ovarian', 'Pancreatic',
                'Prostate', 'Rectal', 'Stomach', 'Uterine'
            ];
            if (cancerTypes.includes(input)) {
                return 'quickSearchCancer';
            } else if (input.includes('-') && input.includes(':')) {
                return 'quickSearchPosition';
            } else if (input.includes('_')) {
                return 'quickSearchSnpEpistasis';
            } else if (input.startsWith('rs')) {
                return 'quickSearchSnp';
            } else {
                return null;
            }
        },
        handleImageClick(name) {
            this.$router.push({ name: 'quickSearchCancer', params: { speciesName: name } });
        },
        showDetails(index) {
            this.$set(this.speciesList[index], 'showDetails', true);
        },
        hideDetails(index) {
            this.$set(this.speciesList[index], 'showDetails', false);
        },
        sampleNumPlot() {
            this.chartSample = echarts.init(document.getElementById("option1"));
            this.chartSample.setOption({
                title: {
                    x: 'center',
                    y: '20px',
                    textStyle: {
                        fontSize: 18
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    appendToBody: true,
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                xAxis: {
                    data: ["Breast", "Prostate", "Melanoma", "Colon", "Cervical", "Lung", "Bladder",
                        "Rectal", "Uterine", "Kidney", "Ovarian", "Pancreatic", "Esophagus", "Stomach", "Brain", "Liver"],
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLabel: { rotate: 45 }
                },
                yAxis: {},
                grid: {
                    left: '10%',
                    right: '15%',
                    bottom: '0%',
                    top: '8%',
                    containLabel: true
                },
                series: [
                    {
                        data: [19207,14466,8416,6834,6740,4960,4128,3142,2768,2314,2182,1668,1609,1305,1157,1122],
                        type: "bar",
                        barWidth: '30%',
                        barCategoryGap: '10%',   
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    var colorList = [
                                        "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff",
                                        "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff", "#93c4ff",
                                    ];
                                    return colorList[params.dataIndex]
                                }
                            }
                        },
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#FF7C43'
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{c}'
                            }
                        }
                    }
                ]
            })
        },
        gwasPlot() {
            this.chartInteraction = echarts.init(document.getElementById("option3"));
            this.chartInteraction.setOption({
                title: {
                    x: 'center',
                    y: '20px',
                    textStyle: {
                        fontSize: 18
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    appendToBody: true,
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                xAxis: {
                    data: ["Breast", "Prostate", "Melanoma", "Colon", "Cervical", "Lung", "Bladder",
                        "Rectal", "Uterine", "Kidney", "Ovarian", "Pancreatic", "Esophagus", "Stomach", "Brain", "Liver"],
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLabel: { rotate: 45 }
                },
                yAxis: {},
                grid: {
                    left: '10%',
                    right: '15%',
                    bottom: '0%',
                    top: '8%',
                    containLabel: true
                },
                series: [
                    {
                        data: [10605,11461,10080,9718,11027,10970,10224,10470,10661,10841,10526,10681,11563,11369,11605,11371],
                        type: "bar",
                        barWidth: '30%',
                        barCategoryGap: '10%', 
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    var colorList = [
                                        "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2",
                                        "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2", "#a7a7f2",
                                    ];
                                    return colorList[params.dataIndex]
                                }
                            }
                        },
                        // label: {
                        //     show: true,
                        //     position: 'top',
                        //     formatter: '{c}'
                        // },
                        emphasis: {
                            itemStyle: {
                                color: '#FF7C43'
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{c}'
                            }
                        }
                    }
                ]
            })
        },
        interactionNumPlot() {
            this.chartInteraction = echarts.init(document.getElementById("option2"));
            this.chartInteraction.setOption({
                title: {
                    x: 'center',
                    y: '25px',
                    textStyle: {
                        fontSize: 18
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    appendToBody: true,
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                xAxis: {
                    data: ["Breast", "Prostate", "Melanoma", "Colon", "Cervical", "Lung", "Bladder",
                        "Rectal", "Uterine", "Kidney", "Ovarian", "Pancreatic", "Esophagus", "Stomach", "Brain", "Liver"],
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLabel: { rotate: 45 }
                },
                yAxis: {},
                grid: {
                    left: '10%',
                    right: '15%',
                    bottom: '0%',
                    top: '8%',
                    containLabel: true
                },
                series: [
                    {
                        data: [6840,7717,7322,6347,18207,17227,7019,7421,7855,8128,7802,8221,9156,9302,9630,9588],
                        type: "bar",
                        barWidth: '30%',
                        barCategoryGap: '10%',   
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    var colorList = [
                                        "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A",
                                        "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A", "#FF8A9A",
                                    ];
                                    return colorList[params.dataIndex]
                                }
                            }
                        },
                        // label: {
                        //     show: true,
                        //     position: 'top',
                        //     formatter: '{c}'
                        // },
                        emphasis: {
                            itemStyle: {
                                color: '#FF7C43'
                            },
                            label: {
                                show: true,
                                position: 'top',
                                formatter: '{c}'
                            }
                        }
                    }
                ]
            })
        },
        
        fillInput(example) {
            this.input = example;
            this.selectedExample = example
        },
        isSelected(example) {
            return this.selectedExample === example
        },
        quickSearch() {
            if (!this.input) {
                this.$message.error('Please enter a query.');
                return;
            }
            const queryType = this.determineQueryType(this.input);
            if (!queryType) {
                this.$message.error('Invalid input format.');
                return;
            }
            if (queryType === 'quickSearchPosition') {
                const [chromosome, positions] = this.input.split(':');
                const [start, end] = positions.split('-');
                this.$router.push({
                    name: queryType,
                    params: {
                        chromosome: chromosome,
                        start: parseInt(start),
                        end: parseInt(end)
                    }
                });
            } else {
                this.$router.push({ name: queryType, params: { queryID: this.input } });
            }
        },
    },
    mounted() {
        this.$nextTick(() => {
            this.$refs.searchInput.focus();
            this.sampleNumPlot();
            this.interactionNumPlot();
            this.gwasPlot();
        });
        this.$nextTick(() => {
            this.$refs.searchInput.$el.querySelector('.el-input__inner').style.fontSize = '19px';
        });
    }
}
</script>

<style>
.content-container {
    width: 1140px;
    margin: 0 auto;
    font-family: Helvetica;
}

.badge {
    padding: .4em .4em; /* 控制徽章的内边距 */
    font-size: 100%; /* 调整字体大小为标准大小的75% */
    font-weight: 700; /* 字体加粗 */
    line-height: 1; /* 行高 */
    text-align: center; /* 文本居中 */
    white-space: nowrap; /* 防止文本换行 */
    vertical-align: baseline; /* 垂直对齐 */
    border-radius: .15rem; /* 边角的圆滑程度 */
    font-family: Helvetica;
}

.alert-info {
    color: #F75C03; /* 这里需要替换为图片中文字的具体颜色代码 */
    font-family: Helvetica;
    /* background-color: ; 这里需要替换为图片中背景的具体颜色代码 */
    /* border-color: ; 如果有边框的话，也需要替换为具体颜色代码 */ 
}

.input-examples {
    color: #2A2A2A; /* Adjust the color to match your theme */
    font-size: 19px; /* Adjust the size as needed */
    text-align: center; /* Center the example text */
    margin: 10px 10px;
    font-family: Helvetica;
}

.selected {
    color: #FF7C43;
    font-family: Helvetica;
}

.search-input .el-button {
    border-radius: 5px 10px 10px 0; /* Rounded corners for the button */
    font-size: 18px; /* Make the input text larger */
    padding: 10px 15px; /* Increase padding for the input field */
    font-family: Helvetica;
}

.home-search {
    margin: 20px 0px 15px;
    font-family: Helvetica;
}

.panel {
    border: 1px solid #d9d9f3;
    border-radius: 5px;
    margin: 0 0 10px 0;
    font-family: Helvetica;
}

.panel-header {
    padding: 8px;
    background-color: #d9d9f3;
    font-size: 17px;
    font-weight: bold;
    font-family: Helvetica;
}

.el-carousel .el-carousel__container .el-carousel__indicators {
    position: absolute !important;
    bottom: 0px !important; /* 根据实际情况调整，使指示器线与边框对齐 */
    font-family: Helvetica;
}

/* 第一个框 */
.panel-body {
    padding: 10px;
    line-height: 25px;
    font-size: 15px;
    font-family: Helvetica;
}

/* 第二个框的大小 */
.data-summary {
    height: 408px;
    overflow: auto;
    font-family: Helvetica;
}

/* 第二个框中，统计边框的大小 */
.innerBody {
    border: 1px solid #A2D9CE;
    border-radius: 5px;
    width: 100%;
    padding: 0;
    font-family: Helvetica;
}

.innerBody .el-table {
    width: 100%; /* 确保表格宽度填充整个容器 */
    margin: 0; /* 去掉默认的外边距 */
    font-family: Helvetica;
}

.el-carousel {
    height: auto; /* 设置高度为自动 */
    font-family: Helvetica;
}

.el-carousel .el-carousel__item {
    height: auto; /* 设置高度为自动 */
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: Helvetica;
}

.image-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    object-fit: cover;
    padding: 0 10px;
    font-family: Helvetica;
}

.card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 3px;
    width: 100%;
    position: relative;
    font-family: Helvetica;
}

.card-img-top {
    width: 135px;
    height: 135px;
    object-fit: cover;
    border-radius: 10%;
    border: 2px solid #ccc; /* Adding border to images */
    cursor: pointer;
    font-family: Helvetica;
}

.card-title {
    font-size: 1.2em;
    margin-top: 10px;
    text-align: center;
    font-family: Helvetica;
}

.card-text {
    color: BLUE;
    font-size: 1em;
    text-align: center;
    margin-bottom: 0;
    position: absolute;
    bottom: 10px;
    left: 0;
    right: 0;
    background-color: rgba(255, 255, 255, 0.7);
    display: none;
    font-family: Helvetica;
}

.card-text p {
    margin: 2px 0; /* 缩小字样与字样之间的距离 */
    font-family: Helvetica;
}

.card:hover .card-text {
    display: block;
    font-family: Helvetica;
}

.el-row {
    margin-bottom: 10px;
    padding: 0px;
    font-family: Helvetica;
}

.el-table .cell {
    /* font-weight: bold;  */
    font-size: 16px; /* 增大字体尺寸 */
    font-family: Helvetica;
}

/* .el-table th {
    background-color: #D2B4DE !important; 
    color: #143a52 !important;
    font-size: 20px !important;
} */
.carousel-item-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: Helvetica;
}

.carousel-title {
    margin-bottom: 10px; 
    font-size: 18px;
    text-align: center;
    font-family: Helvetica;
}

.carousel-chart {
    width: 800px;  /* 控制宽度 */
    height: 250px;  /* 控制高度 */
    margin-left: 70px;  /* 增大距离左端的距离 */
    margin-right: 10px;  /* 减少距离右端的距离 */
    font-family: Helvetica;
}

.el-carousel .el-carousel__container .el-carousel__indicators {
    bottom: -30px !important; 
    font-family: Helvetica;
}
</style>





