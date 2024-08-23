import { createApp } from 'vue'
import Editor from './components/Editor.vue';

import yamlWorker from 'monaco-yaml/yaml.worker?worker'

self.MonacoEnvironment = {
    getWorker: function (_, __) {
        return new yamlWorker();
    }
};

createApp(Editor).mount('#app')