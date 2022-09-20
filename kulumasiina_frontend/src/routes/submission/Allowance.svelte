<script lang='js'>
  import InfoRow from './infoRow.svelte';
  import { formatEur } from '$lib/formatters';
  export let allowance;
</script>

<div class='row pt-3 pb-3'>
  <InfoRow label='Plate number'>{allowance.plate_no}</InfoRow>
  <InfoRow label='Description'>{allowance.description}</InfoRow>
  <InfoRow label='Route'>{allowance.route}</InfoRow>
  <InfoRow label='Allowance'>{allowance.trip_length} km &times; {allowance.per_km} €/km = {formatEur(allowance.trip_length * allowance.per_km)}</InfoRow>
</div>