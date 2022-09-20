<script lang="ts">
  import { onMount } from 'svelte';
  export let filename: string;

  onMount(() => {
    displayProtectedImage(filename, `/api/file/${filename}`, localStorage.getItem('token'))
  })

  function fetchWithAuthentication(url, authToken) {
    const headers = new Headers();
    headers.set('Authorization', `Bearer ${authToken}`);
    return fetch(url, { headers });
  }

  async function displayProtectedImage(
    imageId, imageUrl, authToken
  ) {
    // Fetch the image.
    const response = await fetchWithAuthentication(
      imageUrl, authToken
    );

    // Create an object URL from the data.
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);

    // Update the source of the image.
    const imageElement = document.getElementById(imageId);
    imageElement.src = objectUrl;
    imageElement.onload = () => URL.revokeObjectUrl(objectUrl);
  }
  
  const togglePopup = (event) => {
    
  }
  // TODO: käsittele pdf:t erikseen

</script>

<img id={filename} alt='receipt'/>

<button type="button" class="btn btn-primary" data-toggle="modal" data-target={`${filename}-modal`}>
  Launch demo modal
</button>


<!-- <a href="#myModal" type="" class="" data-bs-toggle="modal" data-bs-target="#myModal">More details</a>

<div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Image Title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <img src="images/img_example_8.png" alt="Image Title" class="img-fluid">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div> -->


<style>
  img {
    max-width: 70%;
  }

  img.popup {
    position:absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 60vw;
  }
</style>