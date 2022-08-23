<script type='ts'>
  import AbstractItem from './AbstractItem.svelte';
  const per_km = 0.22;
  export let i: string;
  $: id = `allowance-item-${i.slice(0, -1)}`;
  $: key_kms = `${id}-kms`;
  let kms: string = '';
  export let value: string = '';
  $: value = String(Number(kms) * per_km);
  export let onClose: {(): void};

</script>

<AbstractItem id={id} onClose={onClose}>
  <svelte:fragment slot='desc'>Mileage allowance</svelte:fragment>
  <svelte:fragment slot='valueInput'>
    <input bind:value={kms} placeholder='00' type='text' class='form-control' name={key_kms}>
    <span class='input-group-text'>km x {per_km} €/km = {value}€</span>
  </svelte:fragment>

</AbstractItem>