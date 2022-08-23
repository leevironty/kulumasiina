<script>
  import Group from './FormGroup.svelte';
  import CostItem from './CostItem.svelte';
  let formItems = [
    {
      value: 10,
      desc: 'Kävin kaupassa',
      kind: 'expense',
    },
    {
      value: 100,
      desc: 'Ajoin Ouluun',
      kind: 'allowance'
    }
  ];

  $: total = formItems.reduce((v, i) => v + Number(i.value), 0)
  $: needSocialSecurity = formItems.some(({kind}) => kind === 'allowance');

  const newExpense = () => {
    formItems = [...formItems, {
      value: '',
      desc: '',
      kind: 'expense',
    }]; 
  }

  const newAllowance = () => {
    formItems = [...formItems, {
      value: '',
      desc: '',
      kind: 'allowance',
    }]; 
  }

  const delNthCallback = (i) => () => {
    formItems.splice(i, 1);
    formItems = formItems;
  }

  const handleSubmit = (event) => {
    // event.preventDefault();
    const { currentTarget } = event;
    console.log(event);
    console.log(currentTarget);
    const data = new FormData(currentTarget);
    console.log(data);
    fetch('/api/submit', {
      method: 'POST',
      body: data,
    })
      .then(res => res.json())
      .then(data => console.log(data))
  }
</script>

<div class='container'>
  <div class='row'>
    <div class='col-8'>
      <div class='row flex-row-reverse'>
        <div class='col-9'>
          <h1>Reimbursements</h1>
          <h3>Guild of Physics</h3>
        </div>
        <div class='col-3'>
          <img src='https://www.fyysikkokilta.fi/wp-content/uploads/2019/02/fii_pelle2-valk.png'>
        </div>
      </div>
    </div>
  </div>
  <div class='row flex-row-reverse'>
    <div class='summary col-4'>
      <h2>Summary</h2>
      <p>Total: {total}€</p>

    </div>
    <form id='form' class='col-8' on:submit|preventDefault={handleSubmit}>
      <Group key='firstName' label='First name'/>
      <Group key='lastName' label='Last name'/>
      <Group key='iban' label='IBAN' placeholder='FI 12 3456 7890 1234 56'/>
      {#if needSocialSecurity}
        <Group key='socialSecurity' label='Social security number'/>
      {/if}
      <hr>
      {#each formItems as item, i}
        <CostItem i={i} bind:desc={item.desc} bind:value={item.value} kind={item.kind} onClose={delNthCallback(i)}/>
      {/each}
      <div class='row flex-row-reverse'>
        <div class='col-9'>
          <div class='row m-0 g-0'>
            <div class='col-6'>
              <button type='button' class='btn btn-primary form-control' on:click={newExpense}>+ new expense</button>
            </div>
            <div class='col-6'>
              <button type='button' class='btn btn-primary form-control' on:click={newAllowance}>+ new mileage allowance</button>  
            </div>
          </div>
          <button type='submit' class='btn btn-secondary form-control mt-1 mb-4'>Submit</button>
        </div>
      </div>
    </form>
  </div>
</div>

<style>
  .container {
    /* max-width: 1080px; */
    max-width: 900px;
    /* border: 1px solid red; */
  }
  img {
    max-width: 100%;
    /* max-height: px; */
    filter: invert(100%);
  }
</style>