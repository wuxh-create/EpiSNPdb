<template>
  <div class="container">
      <Header/>
      <div class="mainer">
          <router-view></router-view>
      </div>
      <Footer/>
  </div>
</template>

<script>
  import Header from './components/SNP-Header.vue'
  import Footer from './components/SNP-Footer.vue'

  export default {
      name:'App',
      components:{Header,Footer}
  }
</script>

<style>
  .container {
      padding-right: 15px;
      padding-left: 15px;
      margin-right: auto;
      margin-left: auto;
  }
  @media (min-width: 768px) {
      .container {
          width: 750px;
      }
  }
  @media (min-width: 992px) {
      .container {
          width: 970px;
      }
  }
  @media (min-width: 1200px) {
      .container {
          width: 1140px;
      }
  }
  .container-fluid {
      padding-right: 15px;
      padding-left: 15px;
      margin-right: auto;
      margin-left: auto;
  }

  /* .mainer{
      margin-top: 10px;
  } */
</style>