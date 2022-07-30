<script lang="ts">

import type {MenuItem} from "src/api";
import { ratingDetails } from "src/stores/ratingStore";
import { slide } from "svelte/transition";

export let menuItems: MenuItem[];
export let mealName: string;
</script>

<details
 transition:slide
>
<summary role="button" on:click={()=>{ratingDetails.set({name:"Overall", product_id:0})}} class="secondary" >{mealName}</summary>
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
				feedback
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
	padding-left: 5px;
	padding-right: 5px;
	background: rgba(255, 122, 89, .3);
	border-radius: 10%;
	text-align: center;
}

details[open] summary ~ * {
  animation: sweep .2s ease-out;
}

@keyframes sweep {
  0%    {opacity: 0; margin-top: -20px}
  100%  {opacity: 1; margin-top: 0px}
}
</style>
