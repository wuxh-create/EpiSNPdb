// 引入 Vue
import Vue from 'vue';

// 引入 App
import App from './App.vue';
// 引入路由
import router from './router/index';
// 引入 VueRouter
import VueRouter from 'vue-router';

// 引入 Ant Design Vue
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

// 引入 ElementUI 组件库
import ElementUI from 'element-ui';
// 引入 ElementUI 全部样式
import 'element-ui/lib/theme-chalk/index.css';


Vue.use(VueRouter);
// 确保 VueRouter 是在引入并使用之后再使用其他插件
Vue.use(Antd);
Vue.use(ElementUI);

// 关闭生产提示
Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
  router,
}).$mount('#app');
