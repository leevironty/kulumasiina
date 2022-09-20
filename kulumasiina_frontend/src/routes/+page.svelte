<script type="ts">
	import Group from './TextInput.svelte';
	import Header from './Header.svelte';
	import CostItem from './CostItem.svelte';
  import MsgBox from '$lib/MsgBox.svelte';
  import { formatEur } from '$lib/formatters';
  import { postForm } from '$lib/api';

	interface costItem {
		kind: 'expense' | 'allowance';
		value: string;
	}
	let costItems: Array<costItem> = [];
	let uploading = false;

	$: total = costItems.reduce((v, { value }) => v + Number(value), 0);
	$: needSocialSecurity = costItems.some(({ kind }) => kind === 'allowance');

	const newExpense = () => {
		costItems = [
			...costItems,
			{
				kind: 'expense',
				value: ''
			}
		];
	};

	const newAllowance = () => {
		costItems = [
			...costItems,
			{
        kind: 'allowance',
				value: ''
			}
		];
	};

	const delNthCallback = (i: number) => () => {
		costItems.splice(i, 1);
		costItems = costItems;
	};


	const handleSubmit = async (event: SubmitEvent) => {
		uploading = true;
    await postForm(event);
    uploading = false;
	};
</script>

<Header />
<MsgBox/>

<div class="row">
	<form id="form" class="col-lg-8" on:submit|preventDefault={handleSubmit}>
		<Group key="fullName" label="Full name" />
		<Group key="iban" label="IBAN" placeholder="FI 12 3456 7890 1234 56" />
		{#if needSocialSecurity}
			<Group key="socialSecurity" label="Social security number" />
		{/if}
		<hr />
		{#each costItems as item, i}
			<CostItem {i} bind:value={item.value} kind={item.kind} onClose={delNthCallback(i)} />
		{/each}
		<div class="row flex-row-reverse">
			<div class="col-9">
				<div class="row m-0 g-1">
					<div class="col-6 ps-0">
						<button
              type="button"
              class="btn btn-primary form-control tall"
              on:click={newExpense}>add expense</button>
					</div>
					<div class="col-6 pe-0">
						<button
              type="button"
              class="btn btn-primary form-control tall"
              on:click={newAllowance}>add mileage allowance</button>
					</div>
				</div>
				<button type="submit" class="btn btn-secondary form-control mt-1 mb-4">
					{#if !uploading}
						Submit
					{:else}
						<div class="spinner-border spinner-border-sm" role="status" />
					{/if}
				</button>
			</div>
		</div>
	</form>
	<div class="summary col-lg-4 text-end text-lg-start">
		<h2>Summary</h2>
		<p>Total: {formatEur(total)}</p>
	</div>
</div>

<style>
  .tall {
    height: 100%;
  }
</style>