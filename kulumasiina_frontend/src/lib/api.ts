import { setMsg } from '$lib/store';

export const postForm = async (event: SubmitEvent) => {
  const { currentTarget } = event;
  console.log(event);
  console.log(currentTarget);
  const data = new FormData(currentTarget);
  console.log(data);
  const response = await fetch('/api/submit', {
    method: 'POST',
    body: data
  });
  const isJson = response.headers.get('content-type')?.includes('application/json');
  const responseData = isJson ? await response.json() : null;
  if (!response.ok) {
    const err = (responseData && responseData.msg) || response.status;
    console.log('Upload failed.')
    setMsg({status: 'danger', msg: `Upload failed: ${err}`})
  } else {
    console.log('Success')
    setMsg({status: 'success', msg: 'Upload succeeded'})
  }

    // .then(async (response) => {

    //   // check for error response
    //   if (!response.ok) {
    //     // get error message from body or default to response status
    //     const error = (data && data.message) || response.status;
    //     return Promise.reject(error);
    //   }
    // })
    // .then(() => {
    // })
    // .catch((err) => {
    //   console.log({ err });
    // })
    // .finally(() => {
    // });
};