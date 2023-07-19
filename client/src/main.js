import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import { ElMessage } from "element-plus"

const app = createApp(App)
app.mount('#app')

app.config.globalProperties.$message = ElMessage