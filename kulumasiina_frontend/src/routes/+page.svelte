<script type='ts'>
  import Group from './TextInput.svelte';
  import Header from './Header.svelte';
  import CostItem from './CostItem.svelte';

  const formatEur = new Intl.NumberFormat('fi-FI', {
    style: 'currency',
    currency: 'EUR',
  }).format;

  interface costItem {
    kind: 'expense' | 'allowance',
    value: string
  }
  let costItems: Array<costItem> = [];

  $: total = costItems.reduce((v, {value}) => v + Number(value), 0);
  $: needSocialSecurity = costItems.some(({kind}) => kind === 'allowance');

  const newExpense = () => {
    costItems = [...costItems, {
      kind: 'expense',
      value: ''
    }];
  }

  const newAllowance = () => {
    costItems = [...costItems, {
      value: '',
      kind: 'allowance',
    }]; 
  }

  const delNthCallback = (i: number) => () => {
    costItems.splice(i, 1);
    costItems = costItems;
  }

  const handleSubmit = (event: SubmitEvent) => {
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

<Header/>
<div class='row'>
  <form id='form' class='col-lg-8' on:submit|preventDefault={handleSubmit}>
    <Group key='fullName' label='Full name'/>
    <Group key='iban' label='IBAN' placeholder='FI 12 3456 7890 1234 56'/>
    {#if needSocialSecurity}
      <Group key='socialSecurity' label='Social security number'/>
    {/if}
    <hr>
    {#each costItems as item, i}
      <CostItem i={i} bind:value={item.value} kind={item.kind} onClose={delNthCallback(i)}/>
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
  <div class='summary col-lg-4 text-end text-lg-start'>
    <h2>Summary</h2>
    <p>Total: {formatEur(total)}</p>
  </div>
</div>
