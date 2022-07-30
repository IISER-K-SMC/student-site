<script lang="ts">
import { get_past_orders } from "src/api";
import { authDetails } from "src/stores/auth";
import { currentRoute } from "src/stores/routes";
import { fade } from "svelte/transition";
import MenuFeedBack from "./MenuFeedBack.svelte";


let menuItems: any[] = [];

async function getOrders() {
	if ($authDetails!==undefined)
	menuItems = await get_past_orders($authDetails.token);
}


let loading = getOrders();
</script>

<button on:click={()=>{$currentRoute = MenuFeedBack}}>Back to menu</button>
{#await loading}
	<div aria-busy="true"> Getting your previous orders.</div>
{:then}

	{#each menuItems as meal}
	<article in:fade>
		<table role="grid">
		<tr>
		<td>{(new Date(meal.datetime)).toLocaleString()} </td>
		<td>balance: ₹{meal.balance}</td>
		</tr>
		{#each JSON.parse(JSON.parse(meal.items)) as meal_item}
			<tr>
			<td>{meal_item[0]}</td>
			<td>₹{meal_item[1]}</td>
			<td>x{meal_item[2]}</td>
			</tr>
		{/each}
		</table>
	</article>
	{/each}
	<button on:click={()=>{$currentRoute = MenuFeedBack}}>Back to menu</button>
{:catch err}
	<p style="color: red;">err</p>
	<button on:click={()=>{$currentRoute = MenuFeedBack}}>Back to menu</button>
{/await}
