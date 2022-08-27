<script type='ts'>
  import ExpenseItem from "./ExpenseItem.svelte";
  import AllowanceItem from "./AllowanceItem.svelte";
  export let kind: 'expense' | 'allowance';
  export let i: number;
  export let value: string;
  export let onClose: {(): void};
</script>

{#if kind === 'expense'}
  <ExpenseItem i={i}, onClose={onClose} bind:value={value}/>
{:else}
  <AllowanceItem i={i}, onClose={onClose} bind:value={value}/>
{/if}