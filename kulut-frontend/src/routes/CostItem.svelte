<script type='ts'>
  import ExpenseItem from "./ExpenseItem.svelte";
  import AllowanceItem from "./AllowanceItem.svelte";
  export let kind: string;
  export let i: number;
  export let value: string;
  export let onClose: {(): void};
  $: {
    console.log(i);
    // console.log(`id-${i}`);
    // console.log(`id-${String(i)}`);
    console.log(String(i));
  }
</script>

{#if kind === 'expense'}
  <ExpenseItem i={i}, onClose={onClose} bind:value={value}/>
{:else}
  <AllowanceItem i={i}, onClose={onClose} bind:value={value}/>
{/if}