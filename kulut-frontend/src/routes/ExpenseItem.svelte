<script type='ts'>
  import AbstractItem from './AbstractItem.svelte';
  export let i: string;
  // export let kind: string;
  $: id = `expense-item-${i.slice(0, -1)}`;
  // $: key_desc = `${id}-desc`;
  // $: key_kms = `${id}-kms`;
  $: key_value = `${id}-value`;
  $: key_receipt = `${id}-receipt`;
  // let kms: string = '';
  // export let desc: string;
  $:{
    console.log({i, id, key_value, key_receipt});
  }
  export let value: string = '';
  export let onClose: {(): void};
  let fileUpload: HTMLInputElement;
</script>

<!-- <div class='row mb-2< mt-2'>
  <div class='col-3'>
    <label class='form-label col-3' for={key_desc}>{kind === 'expense' ? 'Expense' : 'Milege allowance'}</label>
  </div>
  <div class='col-9'>
    <textarea class='form-control mb-2'rows=3 id={key_desc} name={key_desc} bind:value={desc} placeholder='Description'></textarea>
    {#if (kind === 'expense')}
      <input class='hidden-file' type='file' name={key_receipt} bind:this={fileUpload}>
      <button type='button' class='btn btn-primary form-control mb-2' on:click={() => fileUpload.click()} >Upload receipt</button>
    {/if}
    <div class='row'>
      <div class='col-8'>
        <div class='input-group'>
            
        </div>
      </div>
      <div class='col-4'>
        <button type='button' class='btn btn-danger form-control' on:click={onClose}>Remove</button>
      </div>
    </div>
  </div>
</div> -->
<AbstractItem onClose={onClose} id={id}>
  <svelte:fragment slot='desc'>Expense</svelte:fragment>
  <svelte:fragment slot='receiptUpload'>
    <input class='hidden-file' type='file' name={key_receipt} bind:this={fileUpload}>
    <button type='button' class='btn btn-primary form-control mb-2' on:click={() => fileUpload.click()}>Upload receipt</button>
  </svelte:fragment>
  <svelte:fragment slot='valueInput'>
    <span class='input-group-text'>Value</span>
    <input type='text' class='form-control' placeholder='0.00' bind:value={value} name={key_value}>
    <span class='input-group-text'>€</span>
  </svelte:fragment>
</AbstractItem>
  

<style>
  .hidden-file {
    display: none;
  }
</style>