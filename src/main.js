import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// Import Bootstrap JavaScript bundle
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
