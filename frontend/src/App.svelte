<script lang="ts">
  import "@picocss/pico/css/pico.min.css";
  import MenuItems from "./lib/MenuItems.svelte";
  import Feedback from "./lib/Feedback.svelte";
</script>

<main class="container">
  <header class="headings">
  	<h1>SMC</h1>
	<h3>Menu and Feedback section</h3>
  </header>


  <details open>
  <summary><b>Menu</b></summary>
	  <MenuItems/>
  </details>

  <details open>
  <summary><b>Feedback</b></summary>
	  <Feedback/>
  </details>

</main>

<style>
header {
	padding-top: 1em;
}
</style>
