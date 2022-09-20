<script lang="ts">
  import { msg, type Msg} from '$lib/store';
  let msgValue: Msg = {status: null, msg: ''};
  msg.subscribe(v => {
    console.log('msg value updated.')
    msgValue = v;
  })
</script>

{#if msgValue?.status !== null}
	<div class={`alert fixed alert-${msgValue.status}`} role="alert">
		{msgValue.msg}
	</div>
{/if}

<style>
  .fixed {
    position: fixed;
    top: 1em;
    left: 50%;
    transform: translate(-50%);
  }
</style>
