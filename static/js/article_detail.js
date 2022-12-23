function deleteComment(commentId) {
  const csrftoken = Cookies.get('csrftoken')
  fetch('/comments/' + commentId, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken
      },
      mode: 'same-origin'
    })
    .then((response) => {
      if (response.ok) {
        const comment = document.getElementById("comment-" + commentId)
        const content = comment.getElementsByClassName("comment-content")[0]
        content.innerHTML = "This comment was deleted."
        const buttons = comment.getElementsByClassName("action-buttons")[0]
        buttons.innerHTML = ""
      }
    })
}

function toggleEditForm(commentId) {
  const comment = document.getElementById("comment-" + commentId)
  const content = comment.getElementsByClassName("comment-content")[0]
  const editBtn = comment.getElementsByClassName("comment-edit-btn")[0]
  
  if (!content.dataset.content) {
    editBtn.classList.replace("btn-light", "btn-primary")
    content.dataset.content = content.innerHTML
    content.innerHTML = `<textarea id="comment-${commentId}-textarea" class="form-control">${content.innerHTML.trim()}</textarea>
    <div class="d-flex justify-content-end mt-2">
    <button onclick="saveComment(${commentId})" class="btn btn-primary btn-sm me-2">Save</button>
    <button onclick="toggleEditForm(${commentId})" class="btn btn-secondary btn-sm">Cancel</button>
    </div>`
  } else {
    editBtn.classList.replace("btn-primary", "btn-light")
    content.innerHTML = content.dataset.content
    delete content.dataset.content
  }
}

function saveComment(commentId) {
  const newContent = document.getElementById("comment-" + commentId + "-textarea").value
  const csrftoken = Cookies.get('csrftoken')
  const data = new FormData()
  data.append('content', newContent)
  fetch('/comments/' + commentId, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    mode: 'same-origin',
    body: data
  })
  .then((response) => {
    if (response.ok) {
      const content = document.getElementById("comment-" + commentId).getElementsByClassName("comment-content")[0]
      content.dataset.content = newContent
      toggleEditForm(commentId)
    }
  })
}