<script lang="ts">
	import { sendFeedback } from "./../api";
  	import {ratingDetails} from "./../stores/ratingStore"


	let formStars: number = 5;
	let formFeedback: string = "";
	let formUsername: string = "";

	let feedbackPromise: Promise<void>;

	async function sumbitForm() {
		const product_id = $ratingDetails.product_id;
		const product_name = $ratingDetails.name;
		await sendFeedback({
			product_id,
			product_name,
			stars: formStars,
			feedback: formFeedback,
			username: formUsername,
		});
		formFeedback = '';
		formStars = 5;
	}

	ratingDetails.subscribe(()=>{
		feedbackPromise = undefined;
	})
</script>

	<!-- OVERALL FEEDBACK PROMPT -->
	{#if $ratingDetails.product_id !== 0}
		<a href="..." on:click|preventDefault={()=>{
			ratingDetails.set({
				product_id: 0,
				name: "Overall"
			});
		}}>Give overall feedback instead</a>
	{/if}




<form id="rating-form"
 on:submit|preventDefault={()=>{
  feedbackPromise=sumbitForm()
 }}>

  <!-- Grid -->
  <div class="grid">
  	<h1>Feedback for <b>{$ratingDetails.name}</b></h1>

    <label>
	  Name or Rollnumber
      <input type="text" placeholder="Name or Rollnumber"
	   bind:value={formUsername} minlength="3" required>
    </label>

    <label>
	  Rating (<b>{formStars}/5</b>)
      <input type="range" min="1" max="5" bind:value={formStars}>
    </label>

    <label>
	  Feedback
	  <textarea rows="4" cols="50" bind:value={formFeedback}
	   placeholder="Enter your feedback here" required></textarea>
    </label>

  </div>

  {#if feedbackPromise !== undefined}
	  {#await feedbackPromise}
		<div aria-busy="true">Submitting feedback</div>
	  {:then}
		<p>✅ Submitted feedback for {$ratingDetails.name}. Thank you for submitting feedback.</p>
	  {:catch error}
		<p style="color: red">{error.message}</p>
		<b>Try connecting to IISER K and retry</b>
	  {/await}
  {/if}

  <button type="submit">Submit</button>
</form>

