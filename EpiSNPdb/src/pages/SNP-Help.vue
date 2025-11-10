<!-- App.vue -->
<template>
  <div class="content-container">
  <div id="app">
    <div class="sidebar">
      <ul>
        <li :class="{ active: activeSection === 'data-collection' }">
          <button @click="scrollTo('data-collection')">Data collection</button>
        </li>
        <li :class="{ active: activeSection === 'methods-and-tools' }">
          <button @click="scrollTo('methods-and-tools')">Methods and Tools</button>
        </li>
        <li :class="{ active: activeSection === 'data-contributors' }">
          <button @click="scrollTo('data-contributors')">Data Contributors</button>
        </li>
        <li :class="{ active: activeSection === 'contact' }">
          <button @click="scrollTo('contact')">Contact</button>
        </li>
      </ul>
    </div>
    <div class="content">
      <section id="data-collection">
        <h1>Data collection</h1>
        <p>The EpiSNP-db database is a data integration platform collected from multiple sources, primarily including the following two data sources:</p>
        <p>EpiSNP-db obtained genotyping data, disease codes, and phenotypic information for a cohort of 500,000 individuals from the <span style="color: #007AFF; font-weight: bold;">UK Biobank</span> database, and mutation data related to cancer from <span style="color: #007AFF; font-weight: bold;">The Cancer Genome Atlas (TCGA)</span>.</p>
        <p>Firstly, the data acquired from the UK Biobank database includes <span style="color: #f6003c; font-weight: bold;">82,018</span> British White cancer samples and <span style="color: #f6003c; font-weight: bold;">298,965</span> British White non-cancer samples, covering <span style="color: #f6003c; font-weight: bold;">16</span> different types of cancer. These cancer types include breast cancer (Breast), prostate cancer (Prostate), melanoma (Melanoma), colon cancer (Colon), cervical cancer (Cervical), lung cancer (Lung), bladder cancer (Bladder), rectal cancer (Rectal), uterine cancer (Uterine), kidney cancer (Kidney), ovarian cancer (Ovarian), pancreatic cancer (Pancreatic), esophageal cancer (Esophagus), stomach cancer (Stomach), brain cancer (Brain), and liver cancer (Liver).</p>
        <p>Secondly, the data obtained from The Cancer Genome Atlas (TCGA) includes <span style="color: #f6003c; font-weight: bold;">6,685</span> cancer samples, covering <span style="color: #f6003c; font-weight: bold;">18</span> different types of cancer. These cancer types include bladder urothelial carcinoma (BLCA), glioblastoma multiforme (GBM), lower-grade glioma (LGG), breast invasive carcinoma (BRCA), cervical squamous cell carcinoma and endocervical adenocarcinoma (CESC), colon adenocarcinoma (COAD), esophageal carcinoma (ESCA), kidney renal clear cell carcinoma (KIRC), liver hepatocellular carcinoma (LIHC), lung adenocarcinoma (LUAD), lung squamous cell carcinoma (LUSC), skin cutaneous melanoma (SKCM), ovarian serous cystadenocarcinoma (OV), pancreatic adenocarcinoma (PAAD), prostate adenocarcinoma (PRAD), rectum adenocarcinoma (READ), stomach adenocarcinoma (STAD), and uterine corpus endometrial carcinoma (UCEC).</p>
        <h2>Number of cancer samples in the UK Biobank and TCGA databases:</h2>
        <table>
              <thead>
                  <tr>
                      <th style="width: 19%;">UK Biobank Cancer</th>
                      <th style="width: 18%;">The number of cancer</th>
                      <th style="width: 22%;">The number of non-cancer</th>
                      <th style="width: 19%;">TCGA Cancer</th>
                      <th style="width: 21%;">The number of cancer</th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="(row, index) in tableData" :key="index">
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
                  </tr>
              </tbody>
          </table>






      </section>
      <section id="methods-and-tools">
        <h1>Methods and Tools</h1>
        <p>This study utilized genotyping data from 500,000 individuals in the <span style="color: #007AFF; font-weight: bold;">UK Biobank</span> to identify <span style="color: #f6003c; font-weight: bold;">SNP epistasis</span> using <span style="color: #f6003c; font-weight: bold;">PLINK</span> software. To minimize the impact of population stratification, we focused on the largest cohort of British Whites. We analyzed SNP epistasis in cancer types with <span style="color: #f6003c; font-weight: bold;">more than 1,000</span> British White samples, as detailed in the Data Collection section.</p>
        <p>To address the imbalance between cancer and non-cancer samples, we applied the saddlepoint approximation method in <span style="color: #f6003c; font-weight: bold;">SAIGE</span> software for a sensitivity analysis of the SNP epistasis results obtained from PLINK.</p>
        <p>To understand the functional roles of the identified epistatic SNPs, we performed functional annotation using <span style="color: #f6003c; font-weight: bold;">ANNOVAR</span> software. Additionally, we conducted a genome-wide association analysis (GWAS) with the <span style="color: #f6003c; font-weight: bold;">fastGWAS-GLMM</span> method in GCTA software to explore the association between epistatic SNPs and disease occurrence.</p>
        <p>For evaluating the impact of epistatic SNPs on cancer prognosis, we performed Kaplan-Meier survival analysis using additive, dominant, and recessive models with the <span style="color: #f6003c; font-weight: bold;">survival</span> and <span style="color: #f6003c; font-weight: bold;">survminer</span> packages in R.</p>
        <p>To study the interactions of mutations corresponding to cancers, we used mutation data from the TCGA database for the 16 cancer types in the UK Biobank and conducted interaction analysis using <span style="color: #f6003c; font-weight: bold;">Fisher's exact test</span>.</p>


        <div>
              <h2>Data Sources:</h2>
              <table class="data-sources-table">
                  <thead>
                      <tr>
                          <th style="width: 5%;">#</th>
                          <th style="width: 10%;">Name</th>
                          <th style="width: 35%;">Usage</th>
                          <th style="width: 50%;">Url</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr>
                          <td>1</td>
                          <td>UK Biobank</td>
                          <td>Data Collection</td>
                          <td>https://www.ukbiobank.ac.uk/</td>
                      </tr>
                      <tr>
                          <td>2</td>
                          <td>TCGA</td>
                          <td>Data Collection</td>
                          <td>https://www.cancer.gov/ccg/research/genome-sequencing/tcga</td>
                      </tr>
                      <tr>
                          <td>3</td>
                          <td>STRING</td>
                          <td>Functional Annotation of Interaction Networks</td>
                          <td>https://cn.string-db.org/</td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <div>
              <h2>Tools:</h2>
              <table class="tools-table">
                  <thead>
                      <tr>
                          <th style="width: 5%;">#</th>
                          <th style="width: 19.5%;">Name</th>
                          <th style="width: 75%;">Usage</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr>
                          <td>1</td>
                          <td>PLINK</td>
                          <td>Extract specific single nucleotide polymorphism (SNP) genotype data from particular samples, perform quality filtering of samples and SNPs, and conduct epistasis identification.</td>
                      </tr>
                      <tr>
                          <td>2</td>
                          <td>SAIGE</td>
                          <td>Conduct sensitivity analysis of SNP epistasis using the saddlepoint approximation method.</td>
                      </tr>
                      <tr>
                          <td>3</td>
                          <td>GCTA(fastGWA-GLMM)</td>
                          <td>Investigate the relationship between binary traits and genetic variation in the genome using generalized linear mixed models (GLMM).</td>
                      </tr>
                      <tr>
                          <td>4</td>
                          <td>ANNOVAR</td>
                          <td>Perform functional annotation of genetic variation.</td>
                      </tr>
                      <tr>
                          <td>5</td>
                          <td>survival</td>
                          <td>Define survival objects and fit Kaplan-Meier survival curves.</td>
                      </tr>
                      <tr>
                          <td>6</td>
                          <td>survminer</td>
                          <td>Visualize the results of survival analysis.</td>
                      </tr>
                  </tbody>
              </table>
          </div>


      </section>
      <section id="data-contributors">
        <h1>Data Contributors</h1>
        <p>This research was conducted using the UK Biobank Resource under application 97563. We thank the participants of UK Biobank for making this work possible.</p>
        <p>The UK Biobank dataset used in this study is not publicly available but can be obtained by application 
          <a href="https://www.ukbiobank.ac.uk/" style="color: blue;">https://www.ukbiobank.ac.uk/</a>.
        </p>
      </section>
      <section id="contact">
        <h1>Contact</h1>
        <p class="contact-text">Any comments and suggestions, please contact us</p>
        <div class="contact-info">
          <h3>Jing Gong, Ph.D. Professor of Bioinformatics<br>
            <span>Email:</span> <canvas id="email1" width="300" height="30" style="display: inline-block; vertical-align: middle;"></canvas>
          </h3>
          <h3>Xiaohong Wu, Master<br>
            <span>Email:</span> <canvas id="email2" width="300" height="30" style="display: inline-block; vertical-align: middle;"></canvas>
          </h3>
          <h3>Jianye Yang, Doctoral Student<br>
            <span>Email:</span> <canvas id="email3" width="300" height="30" style="display: inline-block; vertical-align: middle;"></canvas>
          </h3>
          <p class="contact-text">Huazhong Agricultural University, Wuhan 430070, P.R. China</p>
        </div> 
      </section>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeSection: '',
      tableData: [
          ['Breast', '19,207', '161,999', 'BRCA', '791'],
          ['Prostate', '14,466', '136,966', 'PRAD', '495'],
          ['Melanoma', '8,416', '298,965', 'SKCM', '466'],
          ['Colon', '6,834', '298,965', 'COAD', '288'],
          ['Cervical', '6,740', '161,999', 'CESC', '289'],
          ['Lung', '4,960', '298,965', 'LUAD;LUSC', '513;480'],
          ['Bladder', '4,128', '298,965', 'BLCA', '411'],
          ['Rectal', '3,142', '298,965', 'READ', '89'],
          ['Uterine', '2,768', '161,999', 'UCEC', '447'],
          ['Kidney', '2,314', '298,965', 'KIRC', '368'],
          ['Ovarian', '2,182', '161,999', 'OV', '64'],
          ['Pancreatic', '1,668', '298,965', 'PAAD', '177'],
          ['Esophagus', '1,609', '298,965', 'ESCA', '184'],
          ['Stomach', '1,305', '298,965', 'STAD', '439'],
          ['Brain', '1,157', '298,965', 'GBM;LGG', '311;510'],
          ['Liver', '1,122', '298,965', 'LIHC', '363']
      ]
    };
  },
  methods: {
    scrollTo(id) {
      const element = document.querySelector(`#${id} h1`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
      this.activeSection = id;
    },
    drawEmail(canvasId, emailText) {
      const canvas = document.getElementById(canvasId);
      const context = canvas.getContext('2d');
      context.font = '18px Arial';
      context.fillStyle = '#000';
      context.fillText(emailText, 10, 20);
    },
  },
  mounted() {
    this.drawEmail('email1', 'gong.jing@mail.hzau.edu.cn');
    this.drawEmail('email2', 'wu.xiaohong@webmail.hzau.edu.cn');
    this.drawEmail('email3', 'jyyang@webmail.hzau.edu.cn');
  },
};
</script>

<style scoped>
#app {
  display: flex;
  height: 100vh;
}
.contact-info {
/* border: 1px solid #ccc; */
padding: 5px;
width: 1140px;
margin: 0 auto;
}
canvas {
display: block;
margin-top: 5px;
}
.content-container {
  width: 1140px;
  margin: 0 auto; /* Ensure content is centered */
}
.sidebar {
  width: 200px;
  background-color: white;
  margin-top: 50px;
  padding: 10px;
  position: fixed; 
  height: 100%; 
  overflow-y: auto; 
}

.table-container {
flex: 1;
overflow: auto;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar button {
  width: 100%;
  padding: 10px;
  background-color: #cddeff;
  border: none;
  font-weight: bold; /* 字体加粗 */
  color: #005792;
  cursor: pointer;
}

.sidebar button:hover {
  background-color: #cddeff;
}

.sidebar li.active button {
  background-color: #EEEBD0;
}

.content {
  margin-left: 200px; 
  padding: 10px;
  flex: 1;
  overflow-y: auto; 
}

section {
  margin-bottom: 50px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
border: 1px solid #ddd;
padding: 7px;
text-align: left;
}

th {
background-color: #A2D5F2;
font-weight: bold;
}
tbody {
display: block;
max-height: 1000px; 
overflow-y: auto;
width: 100%;
}

thead, tbody tr {
display: table;
width: 100%;
table-layout: fixed;
}
.contact-text {
font-size: 20px; /* 设置为你需要的字体大小 */
}



th:nth-child(1), td:nth-child(1) {
width: 19%; 
}
th:nth-child(2), td:nth-child(2) {
width: 18%; 
}
th:nth-child(3), td:nth-child(3) {
width: 22%; 
}
th:nth-child(4), td:nth-child(4) {
width: 19%; 
}
th:nth-child(5), td:nth-child(5) {
width: 21%; 
}
.data-sources-table, .tools-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin-top: 20px;
  margin-bottom: 20px;
}

.data-sources-table th, .data-sources-table td,
.tools-table th, .tools-table td {
  border: 1px solid #ddd;
  padding: 7px;
  text-align: left;
}

.data-sources-table th:nth-child(1), .data-sources-table td:nth-child(1){
  width: 5%;
}

.tools-table th:nth-child(1), .tools-table td:nth-child(1) {
  width: 5%;
}


.data-sources-table th:nth-child(2), .data-sources-table td:nth-child(2){
  width: 10%;
}

.tools-table th:nth-child(2), .tools-table td:nth-child(2) {
  width: 19.5%;
}

.data-sources-table th:nth-child(3), .data-sources-table td:nth-child(3) {
  width: 35%;
}

.data-sources-table th:nth-child(4), .data-sources-table td:nth-child(4) {
  width: 50%;
}

.tools-table th:nth-child(3), .tools-table td:nth-child(3) {
  width: 75%;
}

</style>
