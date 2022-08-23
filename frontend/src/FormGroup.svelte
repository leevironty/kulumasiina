<script>
  // export let value;
  export let key;  // ID and key value in form data
  export let label;  // Label text shown to users
  export let placeholder = '';
</script>

<div class='form-group row mb-3'>
  <label class='col-form-label col-3' for={key}>{label}</label>
  <div class='col-9'>
    <input class='form-control' type='text' id={key} name={key} placeholder={placeholder}>
  </div>
</div>