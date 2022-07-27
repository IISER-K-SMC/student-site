<script lang="ts">
	import type {MenuItem} from "./../api";
	export let menuItems: MenuItem[];
	export let mealName: string;

  	import {ratingDetails} from "./../stores/ratingStore"
</script>

<details>
<summary role="button" class="secondary">{mealName}</summary>
<table>
	<tbody>
		{#each menuItems as item}
		<tr>
			{#if !item.special}
			<td>
				{item.name}
			</td>
			{:else}
			<td>
				<u><b>{item.name}</b></u>
			</td>
			{/if}
			<td>
			<div class="rate-button"
			     on:click={()=>{
				 ratingDetails.set({
				 	name: item.name,
					product_id: item.product_id});
					document.getElementById("rating-form").scrollIntoView();
				 }}>
				rate
			</div>
			</td>
		</tr>
		{/each}
	<tbody>
</table>
</details>

<style>
.rate-button {
	cursor: pointer;
	max-height: 4em;
	background: rgba(255, 122, 89, .3);
	border-radius: 10%;
	text-align: center;
}
</style>
