//该文件专门用于专门用于创建整个应用的路由器
//引入vue-router
import VueRouter from 'vue-router'
//导入各个路由组件
import Home from '../pages/SNP-Home'
import EpiSNPGWAS from '../pages/EpiSNPGWAS'
import EpistasisSNP from '../pages/EpistasisSNP'
import EpistasisGene from '../pages/EpistasisGene'
import EpiSNPAnnotation from '../pages/EpiSNPAnnotation'
import EpiSNPSurvival from '../pages/EpiSNPSurvival'
import Download from '../pages/SNP-Download'
import Document from '../pages/SNP-Help'
import Contact from '../pages/SNP-Contact'
import quickSearchSnp from '../pages/quickSearchSnp'
import quickSearchPosition from '../pages/quickSearchPosition'
import quickSearchCancer from '../pages/quickSearchCancer'
import quickSearchSnpEpistasis from '../pages/quickSearchSnpEpistasis'
import EpistasisMutation from '../pages/EpistasisMutation'




//创建并暴露一个路由
export default new VueRouter({
    routes:[
        {
            name:'home',
            path:'/',
            component:Home,
        },
        {
            path:'/EpiSNPGWAS',
            component:EpiSNPGWAS,
        },
        {
            path:'/EpiSNPSurvival',
            component:EpiSNPSurvival,
        },
        {
            path:'/download',
            component:Download,
        },
        {
            path:'/EpistasisSNP',
            component:EpistasisSNP,
        },
        {
            path:'/EpistasisGene',
            component:EpistasisGene,
        },
        {
            path:'/EpiSNPAnnotation',
            component:EpiSNPAnnotation,
        },
        {
            path:'/EpistasisMutation',
            component:EpistasisMutation,
        },
        {
            path:'/Document',
            component:Document,
        },
        {
            path:'/contact',
            component:Contact,
        },
        {
            name:'quickSearchSnp',
            path:'/quickSearchSnp',
            component:quickSearchSnp,
        },
        {
            name:'quickSearchPosition',
            path:'/quickSearchPosition',
            component:quickSearchPosition,
        },
        {
            name:'quickSearchCancer',
            path:'/quickSearchCancer',
            component:quickSearchCancer,
        },
        {
            name:'quickSearchSnpEpistasis',
            path:'/quickSearchSnpEpistasis',
            component:quickSearchSnpEpistasis,
        },
    ]
})

