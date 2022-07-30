<script lang="ts">
	import { sendFeedback } from "./../api";
  	import {ratingDetails} from "./../stores/ratingStore"
	import {authDetails} from "./../stores/auth";
	import { currentRoute } from "./../stores/routes";
	import Login from "./../routes/Login.svelte";
	import { fade, slide } from "svelte/transition";


	let formStars: number = 5;
	let formFeedback: string = "";

	let feedbackPromise: Promise<void>;

	async function sumbitForm() {
		const product_id = $ratingDetails.product_id;
		const product_name = $ratingDetails.name;
		await sendFeedback({
			product_id,
			product_name,
			stars: formStars,
			feedback: formFeedback,
		}, $authDetails.token);
		formFeedback = '';
		formStars = 5;
	}

	ratingDetails.subscribe(()=>{
		feedbackPromise = undefined;
	})
</script>

<!-- OVERALL FEEDBACK PROMPT -->
{#if $ratingDetails.product_id !== 0}
	<a href="./" on:click|preventDefault={()=>{
		ratingDetails.set({
			product_id: 0,
			name: "Overall"
		});
	}}
	transition:slide
	>Give overall feedback instead</a>
{/if}




<form id="rating-form"
 on:submit|preventDefault={()=>{
  feedbackPromise=sumbitForm()
 }}
 transition:fade
 >

  <!-- Grid -->
  <div class="grid">
  	<h1
	>Feedback for <b>{$ratingDetails.name}</b></h1>

  	<p hidden={$authDetails !== undefined}>Please <a on:click={()=> $currentRoute = Login} >login</a> to be able to submit</p>

    <label>
	  Rating (<b>{formStars}/5</b>)
      <input type="range" min="1" max="5" bind:value={formStars}>
    </label>

    <label>
	  Feedback
	  <textarea rows="4" cols="50" bind:value={formFeedback}
	   placeholder="Enter your feedback here"
	   required
  	   disabled={$authDetails === undefined}
	   ></textarea>
    </label>

  </div>

  {#if feedbackPromise !== undefined}
	  {#await feedbackPromise}
		<div aria-busy="true">Submitting feedback</div>
	  {:then}
		<p>✅ Submitted feedback for {$ratingDetails.name}.</p>
		<p> Thank you for submitting feedback.</p>
	  {:catch error}
		<p style="color: red">{error.message}</p>
		<b>Try connecting to IISER K and retry</b>
	  {/await}
  {/if}

  <button type="submit" 
  disabled={$authDetails === undefined}
  >Submit</button>
</form>

