import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/

export default defineConfig(({ command, mode, ssrBuild }) => {
  if (command === 'serve') {
    return {
      // dev specific config
	  define: {
		  API_URL: JSON.stringify("http://localhost:8000/")
	  },
	  plugins: [svelte()],
	  base: '/'
    }
  } else {
    // command === 'build'
    return {
	  define: {
		  API_URL: JSON.stringify("http://10.20.62.110:8000/")
	  },
	  plugins: [svelte()],
	  base: '/'
    }
  }
})


