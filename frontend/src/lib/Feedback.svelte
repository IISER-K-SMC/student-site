<script lang="ts">
	import { sendFeedback } from "./../api";
  	import {ratingDetails} from "./../stores/ratingStore"


	let formStars: number = 5;
	let formFeedback: string = "";
	let formUsername: string = "";

	let feedbackPromise: Promise<void>;

	async function sumbitForm() {
		const product_id = $ratingDetails.product_id
		await sendFeedback({
			product_id,
			stars: formStars,
			feedback: formFeedback,
			username: formUsername,
		})
		formFeedback = ''
	}
</script>


{#if $ratingDetails.product_id !== 0}
	<button on:click={()=>{
		$ratingDetails.product_id = 0;
		$ratingDetails.name = "Overall";
	}}>Rate General</button>
{/if}

<form id="rating-form"
 on:submit|preventDefault={()=>{
  feedbackPromise=sumbitForm()
 }}>

  <!-- Grid -->
  <div class="grid">
  	<h4>Rating {$ratingDetails.name}</h4>

    <label>
	  Name or Rollnumber
      <input type="text" placeholder="Name or Rollnumber"
	   bind:value={formUsername} required>
    </label>

    <label>
	  Rating (<b>{formStars}/5</b>)
      <input type="range" min="1" max="5" bind:value={formStars}>
    </label>

    <label>
	  Feedback
	  <textarea rows="4" cols="50" bind:value={formFeedback}
	   placeholder="Enter your feedback here"></textarea>
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
