<script lang="ts">
import {getFeedbacks} from "./../api";
import type {FeedbackResponse} from "./../api";

let formDateBefore = '';
let formDateAfter = '';

let feedbackResults: FeedbackResponse[] = [];

async function onSubmit() {
	const after = new Date(formDateAfter).toISOString();
	const before = new Date(formDateBefore).toISOString();
	feedbackResults = await getFeedbacks(after, before);
}

function prettyDate(dtstr: string) {
	const dt = new Date(dtstr);
	return `${dt.toDateString()} ${dt.toTimeString()}`
}
</script>

<form on:submit|preventDefault={onSubmit}>
<p>After</p>
<input type="date" bind:value={formDateAfter} required>
<p>Before</p>
<input type="date"  bind:value={formDateBefore} required>
<input type="submit" value="Search Feedbacks in range">
</form>

{#each feedbackResults as feedback}
<article>

<p>Username: {feedback.username}</p>
<p>Rating: {feedback.stars}/5</p>
<p>Item: {feedback.productName}</p>
<p>Datetime: {prettyDate(feedback.datetime)}</p>
<p>
{feedback.feedback}
</p>

</article>
{/each}
