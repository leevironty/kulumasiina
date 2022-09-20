const formatEur = new Intl.NumberFormat('fi-FI', {
  style: 'currency',
  currency: 'EUR'
}).format;

const formatDate = (dateString: string) =>
  Intl.DateTimeFormat('fi-FI').format(Date.parse(dateString));

export { formatEur, formatDate };