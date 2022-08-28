<script type="ts">
	import { onMount } from 'svelte';
	const formatEur = new Intl.NumberFormat('fi-FI', {
		style: 'currency',
		currency: 'EUR'
	}).format;
	const formatDate = (dateString: string) =>
		Intl.DateTimeFormat('fi-FI').format(Date.parse(dateString));

	let loaded: boolean = true;

	interface submission {
		submission_id: number;
		name: string;
		submitted_at: string;
		allowance_sum: number;
		expense_sum: number;
		expense_count: number;
		allowance_count: number;
		accepted_meeting: string;
		paid_at: string;
		is_selected: boolean;
	}

	let submissions: Array<submission> = [];
	let lastChecked: Number | null = null;

	const fetchSubmissions = async () => {
		const token = localStorage.getItem('token');
		if (token === null) {
			location.replace('/login/');
		}
		const data = await fetch('/api/submissions', {
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
		// const data = await res.json();
		data.forEach((element) => {
			element.is_selected = false;
		});
		submissions = data;
	};

	onMount(fetchSubmissions);
</script>

<h2>Admin view</h2>

<table class="table table-bordered table-striped table-hover">
	<thead>
		<tr>
			<th><input type="checkbox" /></th>
			<th>ID</th>
			<th style="width: 100%;">Name</th>
			<th class="text-end">Date</th>
			<th class="text-end">Accepted</th>
			<th class="text-end">Paid</th>
			<th class="text-end">Items</th>
			<th class="text-end">Value</th>
		</tr>
	</thead>
	<tbody>
		{#each submissions as submission}
			<tr class="clickable">
				<td><input type="checkbox" bind:checked={submission.is_selected} /></td>
				<td>{submission.submission_id}</td>
				<td>{submission.name}</td>
				<td class="text-end">{formatDate(submission.submitted_at)}</td>
				<td class="text-end">{submission.accepted_meeting || '-'}</td>
				<td class="text-end">{submission.paid_at ? formatDate(submission.paid_at) : '-'}</td>
				<td class="text-end">{submission.allowance_count + submission.expense_count}</td>
				<td class="text-end">{formatEur(submission.allowance_sum + submission.expense_sum)}</td>
			</tr>
		{/each}
	</tbody>
</table>

<style>
	.clickable {
		cursor: pointer;
	}
</style>
