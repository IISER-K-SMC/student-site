
<script lang="ts">
import { currentRoute } from "./../stores/routes";

import { fade } from 'svelte/transition';

import {authenticate} from "./../api";
import {authDetails} from "./../stores/auth";
import MenuFeedBack from "./MenuFeedBack.svelte";

let username = "";
let password = "";
let submitDetails = "";

async function submit() {
	try {
		const token = await authenticate(username, password);
		try {
			localStorage.setItem("token", token);
			localStorage.setItem("username", username);
		} catch {}
		authDetails.set({ username, token });

		$currentRoute = MenuFeedBack;
	} catch (err) {
		submitDetails = err.message;
	}
}

</script>


<button on:click={()=>{$currentRoute = MenuFeedBack}}>Back to menu</button>
<form in:fade on:submit|preventDefault={submit}>
  <h2>Login</h2>

  <!-- Grid -->
  <div class="grid">
    <!-- Markup example 1: input is inside label -->
    <label>
	Username <small>(IISER K login username)</small>
      <input bind:value={username} type="text" placeholder="username" required>
    </label>

    <label>
	Password
      <input bind:value={password} type="password" placeholder="password" required>
    </label>
  </div>
  <p>{submitDetails}</p>
  <button type="submit">Login</button>

</form>
