<script type="ts">
	export let key: string; // ID and key value in form data
	export let label: string; // Label text shown to users
	export let placeholder = '';
</script>

<div class="form-group row mb-3">
	<label class="col-form-label col-3" for={key}>{label}</label>
	<div class="col-9">
		<input required class="form-control" type="text" id={key} name={key} {placeholder} />
	</div>
</div>
