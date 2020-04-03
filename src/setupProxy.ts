const proxy = require('http-proxy-middleware')

module.exports = function (app: any) {
	app.use(proxy('/user', { target: 'http:localhost:5000/user', changeOrigin: true }))
}