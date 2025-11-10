<template>
    <div class="footer">
        <el-divider></el-divider>
        <!-- <el-divider> 是一个分割线组件，可能是来自 Element UI 库，用于在视觉上区分底部信息与页面的其他内容。 -->
        <div id="footer" class="copy-right">
            <p class="container">
                <strong>Copyright &copy;</strong>
                <a href="https://gong_lab.hzau.edu.cn/#!/" target="_blank">Gong Lab</a>,
                <a href="http://coi.hzau.edu.cn/" target="_blank">College of informatics</a>,
                <a href="http://www.hzau.edu.cn/" target="_blank">HZAU</a>,
                China.
            </p>
            <p>
                Any comments and suggestions, please <router-link to="/help">contact us</router-link>
            </p>
        </div>
    </div>
</template>

<script>
    // 这里定义了 Vue 组件的 JavaScript 部分。export default 表示导出一个对象作为组件的配置。
    // name: 'SNP-Footer' 定义了组件的名称。根据最新的 Vue 和 ESLint 规则，组件名称应该是多单词的，并且使用 PascalCase（大驼峰命名法），所以更好的命名可能是 SnpFooter。
    export default {
        name:'SnpFooter',
    }
</script>

<style>
/* 定义了组件内元素的 CSS 样式 */
    .footer{
        margin-top: 0px;
        /* 定义了根元素的顶部外边距（margin-top: 40px;），使得底部信息与页面其他内容有一定的间距。 */
    }
    .copy-right{
        text-align: center;
        font-size: 13px;
        /* 居中对齐和字体大小。 */
    }
    a{
        text-decoration: none;
        /* 链接的默认样式 */
        /* 移除了链接下划线 */
    }
    a:hover{
        text-decoration: underline;
        color: #FF7C43;
        /* 鼠标悬停时的样式 */
        /* 尝试设置鼠标悬停时的下划线为实线 */
    }
</style>

