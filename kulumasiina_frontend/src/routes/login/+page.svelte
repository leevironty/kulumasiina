<svelte:head>
  {#if mounted}
    <script src="https://accounts.google.com/gsi/client" async defer on:load={displaySignInButton}></script>
  {/if}
</svelte:head>

<script type="ts">
  let mounted = false;
	const GOOGLE_CLIENT_ID =
		'449017889620-74gdp1v6be7sj6rb0hfnf6r141p9hg25.apps.googleusercontent.com';
	import { onMount } from 'svelte';
	// let googleReady = false;
	// let mounted = false;
	onMount(() => {
		console.log('mounted');
    mounted = true;
    // displaySignInButton();
	});

	// const googleLoaded = () => {
	// 	console.log('google loaded');
	// 	googleReady = true;
	// 	if (mounted) {
	// 		displaySignInButton();
	// 	}
	// };

	const displaySignInButton = () => {
    console.log('displaying login button');
		google.accounts.id.initialize({
			client_id: GOOGLE_CLIENT_ID,
			callback: handleCredentialResponse
		});
		google.accounts.id.renderButton(
			document.getElementById('buttonDiv'),
			{ theme: 'outline', size: 'large' } // customization attributes
		);
		google.accounts.id.prompt(); // also display the One Tap dialog
	};

	const handleCredentialResponse = (response) => {
		fetch('/api/login', {
			method: 'POST',
			body: response.credential
		}).then(async (response) => {
			if (response.status === 200) {
				window.localStorage.setItem('token', await response.text());
				location.replace('/admin/');
			} else {
				console.log('Authentication failed');
			}
		});
	};
</script>


<h1 class="text-center">Reimbursements</h1>
<h3 class="text-center">Guild of Physics</h3>

<div class="abs-center">
	<h4 class="text-center">Login</h4>
	<div id="buttonDiv" />
</div>

<style>
	.abs-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		border: 1px solid #fff;
		padding: 1.5em;
		border-radius: 10px;
		box-shadow: #0003 0px 1px 5px 0px;
	}
</style>
