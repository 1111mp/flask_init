const { override, addWebpackAlias, fixBabelImports, removeModuleScopePlugin } = require('customize-cra');
const rewireStyl = require("react-app-rewire-stylus-modules");
const path = require('path');

const addStylus = () => (config, env) => {
	config = rewireStyl(config, env)
	return config
}

module.exports = override(
	removeModuleScopePlugin(),
	fixBabelImports('import', {
		libraryName: 'antd',
		libraryDirectory: 'es',
		style: 'css',
	}),
	addWebpackAlias({
		"@": path.resolve(__dirname, "./src"),
		"config": path.resolve(__dirname, "./src/config"),
		"pages": path.resolve(__dirname, "./src/pages"),
		"react-dom": '@hot-loader/react-dom'
	}),
	addStylus()
)