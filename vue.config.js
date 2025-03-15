const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: [],
  devServer: {
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : '/'
})
