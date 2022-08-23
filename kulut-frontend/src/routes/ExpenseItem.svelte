<script type='ts'>
  import AbstractItem from './AbstractItem.svelte';
  export let onClose: {(): void};
  export let value: string = '';
  export let i: string;
  let fileUpload: HTMLInputElement;
  $: id = `expense-item-${i.slice(0, -1)}`;
  $: key_value = `${id}-value`;
  $: key_receipt = `${id}-receipt`;
</script>

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