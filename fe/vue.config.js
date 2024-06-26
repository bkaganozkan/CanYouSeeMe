const { defineConfig } = require('@vue/cli-service')
const dotenv = require('dotenv');



dotenv.config();

module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
