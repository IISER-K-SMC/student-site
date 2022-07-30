<script lang="ts">
import "@picocss/pico/css/pico.min.css";
import { logout_user } from "./api";
import BalancesOrders from "./routes/BalancesOrders.svelte";
import Login from "./routes/Login.svelte";
import MenuFeedBack from "./routes/MenuFeedBack.svelte";
import { authDetails } from "./stores/auth";
import { currentRoute } from "./stores/routes";



function getCachedUser() {
	const token = localStorage.getItem("token");
	const username = localStorage.getItem("username");

	if (token !== null)
		authDetails.set({token, username});
}

async function onlogout() {
	logout_user($authDetails.token)
	$authDetails = undefined;
	try {
	localStorage.clear();
	} catch {};
}


function gotoLogin() {
	$currentRoute=Login
}
function gotoBalancesOrders() {
	$currentRoute=BalancesOrders
}
getCachedUser();
$currentRoute = MenuFeedBack;
</script>

<main class="container">
	
<header class="headings">
<img style="position: absolute; right:30px ; margin: 1em; border-radius: 5em;" src="/smc-logo.jpg" alt="SMC logo" width="60" height="-1">
<h1>SMC</h1>

<aside>
	<nav>
		<ul>
		</ul>
		<ul>
			<li>
				<a href="https://docs.google.com/forms/d/e/1FAIpQLSfRkplSmeklsEd8QWFpTFY3DTeuVpwUu-42SVYJtPsAgGmVvQ/viewform"
				  target="_blank">Recharge form</a>
			</li>


			{#if $authDetails === undefined }

				<li>
					Not logged in.
					<a href="." on:click|preventDefault={gotoLogin}>Login</a>
				</li>

			{:else}

				<li>
				<a href="." on:click|preventDefault={gotoBalancesOrders}> 
					Previous orders and balance</a>
				</li>
				<li>
					Logged in as <b>{$authDetails.username}</b>.
					<a href="." on:click|preventDefault={onlogout}>Logout</a>
				</li>

			{/if}
		</ul>
	</nav>
</aside>
</header>
<hr>

<svelte:component this={$currentRoute}/>
</main>
<style>
header {
	padding-top: 1em;
	padding-bottom: 0;
	margin-bottom: 0;
}
nav {
	padding-bottom: 0;
	margin-bottom: 0;
}
:global(html) {
  scroll-behavior: smooth;
}
</style>
