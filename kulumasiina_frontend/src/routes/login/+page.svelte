<svelte:head>
  <script src="https://accounts.google.com/gsi/client" async defer on:load={googleLoaded}></script>
  <!-- <script src="https://accounts.google.com/gsi/client" async defer></script> -->
</svelte:head>

<script type='ts'>
  const GOOGLE_CLIENT_ID = '449017889620-74gdp1v6be7sj6rb0hfnf6r141p9hg25.apps.googleusercontent.com';
  import {onMount} from 'svelte';
  let googleReady = false;
  let mounted = false;
  onMount(() => {
    mounted = true;
    if (googleReady) {
        displaySignInButton()
    }
  });

  const googleLoaded = () => {
    googleReady = true;
    if (mounted) {
        displaySignInButton()
    }
  }

  const displaySignInButton = () => {
    google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
      document.getElementById("buttonDiv"),
      { theme: "outline", size: "large" }  // customization attributes
    );
    google.accounts.id.prompt(); // also display the One Tap dialog
  }
  let ssoButton: HTMLElement;
  const decodeJwtResponse = (token)  => {
    let base64Url = token.split('.')[1]
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    let jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload)
  }
  const handleCredentialResponse = async (response) => {
    // decodeJwtResponse() is a custom function defined by you
    // to decode the credential response.
    console.log(response);
    let responsePayload = decodeJwtResponse(response.credential);
    console.log("ID: " + responsePayload.sub);
    console.log('Full Name: ' + responsePayload.name);
    console.log('Given Name: ' + responsePayload.given_name);
    console.log('Family Name: ' + responsePayload.family_name);
    console.log("Image URL: " + responsePayload.picture);
    console.log("Email: " + responsePayload.email);
  }
  // onMount(() => {
  //   ssoButton.setAttribute('data-callback', handleCredentialResponse)
  // })
</script>

<h1 class='text-center'>Reimbursements</h1>
<h3 class='text-center'>Guild of Physics</h3>

<div class='abs-center'>
  <h4 class='text-center'>Login</h4>
  <!--<div id="g_id_onload"
    bind:this={ssoButton}
    data-client_id={GOOGLE_CLIENT_ID}
    data-itp_support="true"
    data-auto_prompt="false"></div>
  <div class="g_id_signin"
    data-type="standard"
    data-size="large"
    data-theme="outline"
    data-text="sign_in_with"
    data-shape="rectangular"
    data-logo_alignment="left"></div> -->
    <div id='buttonDiv'></div>
</div>

<!-- <div class='abs-center'>
  <h4 class='text-center'>Login</h4>
  <div id="g_id_onload"
    data-client_id={GOOGLE_CLIENT_ID}
    data-login_uri="http://localhost:5173/api/login"
    data-auto_prompt="false"></div>
  <div class="g_id_signin"
    data-type="standard"
    data-size="large"
    data-theme="outline"
    data-text="sign_in_with"
    data-shape="rectangular"
    data-logo_alignment="left"></div>
</div> -->

<style>
  /* img {
    max-width: 100%;
    max-height: px;
    filter: invert(100%);
  } */
  .abs-center {
    position:absolute;
    top:50%;
    left:50%;
    transform: translate(-50%, -50%);
    border: 1px solid #fff;
    padding: 1.5em;
    border-radius: 10px;
    box-shadow: #0003 0px 1px 5px 0px;
  }
</style>