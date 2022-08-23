<script type='ts'>
  import AbstractItem from './AbstractItem.svelte';
  export let i: string;
  export let value: string = '';
  export let onClose: {(): void};
  const per_km = 0.22;
  let kms: string = '';
  $: id = `allowance-item-${i.slice(0, -1)}`;
  $: key_kms = `${id}-kms`;
  $: key_value = `${id}-value`;
  $: value = String(Number(kms) * per_km);
</script>

<AbstractItem id={id} onClose={onClose}>
  <svelte:fragment slot='desc'>Mileage allowance</svelte:fragment>
  <svelte:fragment slot='valueInput'>
    <input bind:value={kms} placeholder='0' type='text' class='form-control' name={key_kms}>
    <span class='input-group-text'>km x {per_km} €/km = {value}€</span>
    <input type='text' value={value} name={key_value} hidden>
  </svelte:fragment>
</AbstractItem>