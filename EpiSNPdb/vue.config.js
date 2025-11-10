
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: false,
  lintOnSave: false, //关闭语法检查
  //开启代理服务器
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:50000/',
        pathRewrite: { "^/api": "" },
        ws: true, 
        changeOrigin: true 
      }
    },
  },
  css: {
    loaderOptions: {
      sass: {
      }
    }
  },
  publicPath: '/EpiSNPdb/',
  // publicPath: '/',
  assetsDir: 'assets'

});
