<script lang="ts">
	import {getMenu} from "./../api";
	import type {MenuItem} from "./../api";
	import ItemTable from "./ItemTable.svelte";

	let updatingPromise: Promise<MenuItem[]>;

	function filterMeanNumber(menuItems: MenuItem[], mealNumber: number) {
		return menuItems.filter((val)=>val.meal==mealNumber)
	}

	updatingPromise = getMenu();
	// #TODO open menu based on time of day
</script>


{#await updatingPromise}

<div aria-busy="true" >Loading menu</div>

{:then menuItems}
<ItemTable mealName="Breakfast"
 menuItems={filterMeanNumber(menuItems,1)}/>

<ItemTable mealName="Lunch"
 menuItems={filterMeanNumber(menuItems,2)}/>

<ItemTable mealName="Snacks"
 menuItems={filterMeanNumber(menuItems,3)}/>

<ItemTable mealName="Dinner"
 menuItems={filterMeanNumber(menuItems,4)}/>

{:catch error}

<p style="color: red">{error.message}</p>
<b>Connect to IISER K connection to access menu</b>

{/await}
