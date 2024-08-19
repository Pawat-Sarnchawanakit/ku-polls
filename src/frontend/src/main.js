import { createApp } from 'vue'
import App from './App.vue'

import yamlWorker from 'monaco-yaml/yaml.worker?worker'

self.MonacoEnvironment = {
    getWorker: function (_, __) {
        return new yamlWorker();
    }
};

createApp(App).mount('#app')