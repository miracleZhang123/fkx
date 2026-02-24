<template>
  <div class="analyzer">
    <h2>Vision Transformer 表情分析</h2>
    <div class="upload-area">
      <input type="file" @change="onFileChange" accept="image/*" />
      <div v-if="preview" class="preview-box">
        <img :src="preview" />
      </div>
    </div>
    
    <button @click="analyze" class="action-btn" :disabled="!file || loading">
      {{ loading ? 'Transformer 推理中...' : '开始识别' }}
    </button>

    <div v-if="result" class="result-area">
      <h3>识别结果: <span class="highlight">{{ result.emotion }}</span></h3>
      <div class="prob-bar">
        <div class="bar-fill" :style="{ width: result.confidence * 100 + '%' }"></div>
      </div>
      <p>置信度: {{ (result.confidence * 100).toFixed(2) }}%</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      preview: null,
      result: null,
      loading: false
    }
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
      this.preview = URL.createObjectURL(this.file);
      this.result = null;
    },
    async analyze() {
      this.loading = true;
      const formData = new FormData();
      formData.append('file', this.file);
      
      try {
        // 指向 FastAPI 后端
        const res = await axios.post('http://localhost:8000/predict/image', formData);
        this.result = res.data;
      } catch (err) {
        alert("后端服务未连接或出错");
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.preview-box img { max-width: 100%; max-height: 300px; margin-top: 10px; border-radius: 5px; }
.action-btn { margin-top: 15px; background: #3498db; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; }
.highlight { color: #e74c3c; font-weight: bold; font-size: 1.2em; }
.prob-bar { width: 100%; height: 10px; background: #eee; border-radius: 5px; margin-top: 5px; overflow: hidden;}
.bar-fill { height: 100%; background: #2ecc71; transition: width 0.5s ease; }
</style>