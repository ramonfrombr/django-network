document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
      fetch(`/like/${button.dataset.post_id}`, {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        if (data.action == 'like') {
          button.innerHTML = "<i class=\"fas fa-thumbs-up\"></i> " + (Number(button.dataset.likes++) + 1)
          button.classList.add('post__liked-button')
        } else {
          button.innerHTML = "<i class=\"fas fa-thumbs-up\"></i> " + (Number(button.dataset.likes--) - 1)
          button.classList.remove('post__liked-button')
        }
      })
    })
  })
})
