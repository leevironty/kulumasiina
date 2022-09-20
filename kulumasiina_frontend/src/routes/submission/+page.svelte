<script>
  import { onMount } from 'svelte';
  import InfoRow from './infoRow.svelte';
  import { formatDate, formatEur } from '$lib/formatters';
  import Receipt from './receipt.svelte';
  import Expense from './Expense.svelte';
  import Allowance from './Allowance.svelte';
// import ExpenseItem from '../ExpenseItem.svelte';
// import ExpenseSlots from '../ExpenseSlots.svelte';

   onMount(() => {
    const h = document.getElementById('h');
    if (h !== null) {
      const query = new URLSearchParams(location.search);
      h.innerText = `${h.innerText} #${query.get('id')}`
      updateData(query.get('id'));
    }
   })
   let data = null;

   const updateData = async (id) => {
    const token = localStorage.getItem('token');
		if (token === null) {
			location.replace('/login/');
		}
    const resData = await fetch('/api/submissions/' + id, {
			method: 'GET',
			headers: {
				Authorization: 'Bearer ' + token
			}
		}).then(async (res) => {
			if ((await res.status) === 403) {
				location.replace('/login/');
			}
			return res.json();
		});
    console.log(resData);
    data = resData;
   }
</script>

<div class='row flex-row-reverse'>
  <h1 id='h' class='col-9'>Submission</h1>
</div>

<!-- <p>Content: {JSON.stringify(data)}</p> -->

{#if data !== null}
<!-- <div class='row'>
  <strong class='col-3 text-end'>Name</strong>
  <p class='col-9'>{data.name}</p>
</div> -->
  <InfoRow label='Name'>{data.name}</InfoRow>
  <InfoRow label='IBAN'>{data.iban}</InfoRow>
  <InfoRow label='Submitted at'>{formatDate(data.submitted_at)}</InfoRow>
  <InfoRow label='Total'>{formatEur(data.expenses.reduce( (l, r) => l + r.value, 0))}</InfoRow>
  <InfoRow label='Accepted'>{data.accepted_meeting || 'not accepted'}</InfoRow>
  <InfoRow label='Paid'>{data.paid_at || 'not paid'}</InfoRow>
  {#if data.expenses !== null}
    <div class='row flex-row-reverse'>
      <h2 class='col-9'>Expenses</h2>
    </div>
    {#each data.expenses as expense}
      <Expense expense={expense}/>
    {/each}
  {/if}
  {#if data.allowances !== null}
    <div class='row flex-row-reverse'>
      <h2 class='col-9'>Allowances</h2>
    </div>
    {#each data.allowances as allowance}
      <Allowance allowance={allowance}/>
    {/each}
  {/if}
{/if}
      
<!-- <span>{`${formatEur(expense.value)}: `}</span>{expense.description} -->