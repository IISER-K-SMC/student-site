import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tsconfigPaths from 'vite-tsconfig-paths'
const HOSTING_URL = '10.20.82.223';

// https://vitejs.dev/config/

export default defineConfig(({ command, mode, ssrBuild }) => {
  if (command === 'serve') {
    return {
      // dev specific config
	  define: {
		  API_URL: JSON.stringify("http://localhost:8000/")
	  },
	  plugins: [
		  svelte(),
		  tsconfigPaths(),
	  ],
    }
  } else {
    // command === 'build'
    return {
	  define: {
		  API_URL: JSON.stringify("http://" + HOSTING_URL + ":8000/")
	  },
	  plugins: [
		  svelte(),
		  tsconfigPaths(),
	  ],
	  base: '/'
    }
  }
})


