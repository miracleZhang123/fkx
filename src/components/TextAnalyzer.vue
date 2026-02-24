<template>
  <div class="analyzer">
    <h2>Text Transformer 情感分析</h2>
    
    <div class="input-area">
      <textarea 
        v-model="textInput" 
        placeholder="请输入一段英文文本（例如：I really enjoyed this movie, it was fantastic!）..."
        rows="5"
      ></textarea>
    </div>
    
    <button @click="analyze" class="action-btn" :disabled="!textInput || loading">
      {{ loading ? 'Transformer 推理中...' : '开始分析' }}
    </button>

    <div v-if="result" class="result-area">
      <h3>分析结果: <span :class="['highlight', result.sentiment]">{{ result.sentiment }}</span></h3>
      
      <div class="prob-bar">
        <div 
          class="bar-fill" 
          :style="{ width: result.confidence * 100 + '%', backgroundColor: getColor(result.sentiment) }"
        ></div>
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
      textInput: '',
      result: null,
      loading: false
    }
  },
  methods: {
    async analyze() {
      if (!this.textInput.trim()) return;
      
      this.loading = true;
      const formData = new FormData();
      formData.append('text', this.textInput);
      
      try {
        // 调用后端 API
        const res = await axios.post('http://localhost:8000/predict/text', formData);
        this.result = res.data;
      } catch (err) {
        console.error(err);
        alert("后端服务连接失败，请检查 backend/app.py 是否运行");
      } finally {
        this.loading = false;
      }
    },
    getColor(sentiment) {
      if (sentiment.includes('Positive') || sentiment.includes('正面')) return '#2ecc71'; // Green
      if (sentiment.includes('Negative') || sentiment.includes('负面')) return '#e74c3c'; // Red
      return '#95a5a6'; // Gray for Neutral
    }
  }
}
</script>

<style scoped>
.input-area textarea {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: inherit;
  resize: vertical;
}
.action-btn { margin-top: 15px; background: #9b59b6; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
.action-btn:hover { background: #8e44ad; }
.action-btn:disabled { background: #ccc; cursor: not-allowed; }

.highlight { font-weight: bold; font-size: 1.2em; }
.prob-bar { width: 100%; height: 10px; background: #eee; border-radius: 5px; margin-top: 10px; overflow: hidden; }
.bar-fill { height: 100%; transition: width 0.5s ease; }
</style>