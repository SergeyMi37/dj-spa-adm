export default {
  plugins: [require('@vitejs/plugin-vue')()],
  base: "/static/spa/",
  build: {
    outDir: '../static/spa',
    assetsDir: './assets'
  }
}