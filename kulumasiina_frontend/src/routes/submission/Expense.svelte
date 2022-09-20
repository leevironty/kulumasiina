<script lang='js'>
  import InfoRow from './infoRow.svelte';
  import Receipt from './receipt.svelte';
  import { formatEur } from '$lib/formatters';
  export let expense;
</script>

<div class='row pt-3 pb-3'>
  <div class='col-6'>
    <InfoRow label='Description'>{expense.description}</InfoRow>
    <InfoRow label='Receipt value'>{formatEur(expense.value)}</InfoRow>
  </div>
  <div class='col-6'>
    <Receipt filename={expense.receipt_filename}/>
  </div>
  <!-- <InfoRow label='Receipt'><Receipt filename={expense.receipt_filename}/></InfoRow> -->
</div>