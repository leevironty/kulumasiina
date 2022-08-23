<script type='ts'>
  // export let i: number;
  // export let kind: string;
  // $: id = `${kind === 'expense' ? 'expense' : 'allowance'}-item-${i}`;
  export let id: string;
  $: key_desc = `${id}-desc`;
  // $: key_kms = `${id}-kms`;
  // $: key_value = `${id}-value`;
  // $: key_receipt = `${id}-receipt`;
  // let kms: string = '';
  // export let desc: string;
  let desc = '';
  // export let value: string;
  export let onClose: {(): void};
  // let fileUpload: HTMLInputElement;
</script>

<div class='row mb-2< mt-2'>
  <div class='col-3'>
    <label class='form-label col-3' for={key_desc}><slot name='desc'></slot></label>
  </div>
  <div class='col-9'>
    <textarea class='form-control mb-2'rows=3 id={key_desc} name={key_desc} bind:value={desc} placeholder='Description'></textarea>
    <slot name='receiptUpload'></slot>
    <div class='row'>
      <div class='col-8'>
        <div class='input-group'>
          <slot name='valueInput'></slot>
        </div>
      </div>
      <div class='col-4'>
        <button type='button' class='btn btn-danger form-control' on:click={onClose}>Remove</button>
      </div>
    </div>
  </div>
</div>
<hr>
  

<!-- <style>
  .hidden-file {
    display: none;
  }
</style> -->