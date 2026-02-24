<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="brand">基于改进 Transformer 的多模态情绪识别系统</div>
    </nav>

    <div class="main-content">
      <div class="mode-selector">
        <button 
          :class="{ active: currentTab === 'image' }" 
          @click="currentTab = 'image'">
          📷 图像情绪识别 (ViT)
        </button>
        <button 
          :class="{ active: currentTab === 'text' }" 
          @click="currentTab = 'text'">
          📝 文本情感分析 (Transformer)
        </button>
      </div>

      <div class="workspace">
        <keep-alive>
          <component :is="currentTabComponent" />
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script>
import ImageAnalyzer from './components/ImageAnalyzer.vue'
import TextAnalyzer from './components/TextAnalyzer.vue'

export default {
  components: { ImageAnalyzer, TextAnalyzer },
  data() {
    return {
      currentTab: 'image'
    }
  },
  computed: {
    currentTabComponent() {
      return this.currentTab === 'image' ? 'ImageAnalyzer' : 'TextAnalyzer'
    }
  }
}
</script>

<style>
/* 简单样式 */
body { margin: 0; font-family: 'Helvetica Neue', sans-serif; background: #f0f2f5; }
.navbar { background: #2c3e50; color: white; padding: 1rem; text-align: center; font-size: 1.2rem; }
.main-content { max-width: 800px; margin: 2rem auto; padding: 1rem; }
.mode-selector { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; }
.mode-selector button {
  padding: 10px 20px; border: none; background: white; cursor: pointer; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s;
}
.mode-selector button.active { background: #42b983; color: white; transform: scale(1.05); }
.workspace { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
</style>