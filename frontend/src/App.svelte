<script lang="ts">
  import "@picocss/pico/css/pico.min.css";
  import MenuItems from "./lib/MenuItems.svelte";
  import Feedback from "./lib/Feedback.svelte";
</script>

<main class="container">
  <header class="headings">
  	<h1>SMC</h1>
	<nav>
  		<a href="https://docs.google.com/forms/d/e/1FAIpQLSfRkplSmeklsEd8QWFpTFY3DTeuVpwUu-42SVYJtPsAgGmVvQ/viewform"
  	 	  target="_blank">Recharge form</a>
	</nav>
  </header>
	<hr>
	<h3>Menu and Feedback section</h3>

 


  <details open>
  <summary><b>Menu</b></summary>
	  <MenuItems/>
  </details>

  <Feedback/>

</main>

<style>
header {
	padding-top: 1em;
}
:global(html) {
  scroll-behavior: smooth;
}
</style>


