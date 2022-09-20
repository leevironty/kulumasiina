<script lang="ts">
  export let label: String;
</script>

<div class='row'>
  <div class='col-3 text-end'><strong>{label}</strong></div>
  <div class='col-9'><slot/></div>
</div>