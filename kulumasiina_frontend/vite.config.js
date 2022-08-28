import { sveltekit } from '@sveltejs/kit/vite';
// import { defineConfig } from 'vite';
/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': 'http://localhost:5000'
		},
		cors: false
	}
};

export default config;
