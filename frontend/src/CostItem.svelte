<script>
  export let i;
  export let kind;
  $: id = `${kind === 'expense' ? 'expense' : 'allowance'}-item-${i}`;
  $: key_desc = `${id}-desc`;
  $: key_kms = `${id}-kms`;
  $: key_value = `${id}-value`;
  $: key_receipt = `${id}-receipt`;
  export let desc;
  export let value;
  export let onClose;
</script>

<div class='row mb-2< mt-2'>
  <div class='col-3'>
    <label class='form-label col-3' for={key_desc}>{kind === 'expense' ? 'Expense' : 'Milege allowance'}</label>
  </div>
  <div class='col-9'>
    <textarea class='form-control mb-2'rows=3 id={key_desc} name={key_desc} bind:value={desc} placeholder='Description'></textarea>
    {#if (kind === 'expense')}
      <input class='hidden-file' type='file' name={key_receipt} id={key_receipt}>
      <button type='button' class='btn btn-primary form-control mb-2' on:click={document.getElementById(key_receipt).click()} >Upload receipt</button>
    {/if}
    <div class='row'>
      <div class='col-8'>
        <div class='input-group'>
          <span class='input-group-text'>Value</span>
          <input type='text' class='form-control' placeholder='0.00' bind:value={value}>
          <span class='input-group-text'>€</span>
        </div>
      </div>
      <div class='col-4'>
        <button type='button' class='btn btn-danger form-control' on:click={onClose}>Remove</button>
      </div>
    </div>
  </div>
</div>
<hr>
  

<style>
  .nopad {
    padding: 0 !important;
  }
  .hidden-file {
    display: none;
  }
  .custom-receipts::before {
    content: 'Upload receipt';
    display: inline-block;
    background: #333;
    color: #fff;
    cursor: pointer;
    padding: 0.5em 1em;
    border-radius: 5px;;
  }
  .custom-receipts::-webkit-file-upload-button {
    visibility: hidden;
  }
  .custom-receipts::after {
    visibility: hidden;
  }
  .custom-file-input::-webkit-file-upload-button {
  visibility: hidden;
}
  .custom-file-input::before {
    content: 'Select some files';
    display: inline-block;
    background: linear-gradient(top, #f9f9f9, #e3e3e3);
    border: 1px solid #999;
    border-radius: 3px;
    padding: 5px 8px;
    outline: none;
    white-space: nowrap;
    -webkit-user-select: none;
    cursor: pointer;
    text-shadow: 1px 1px #fff;
    font-weight: 700;
    font-size: 10pt;
  }
  .custom-file-input:hover::before {
    border-color: black;
  }
  .custom-file-input:active::before {
    background: -webkit-linear-gradient(top, #e3e3e3, #f9f9f9);
  }
</style>