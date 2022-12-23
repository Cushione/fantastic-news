function deleteComment(commentId) {
  toggleBtnLoading(commentId, 'comment-delete-btn')
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
      } else {
        toggleBtnLoading(commentId, 'comment-delete-btn')
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
    <button onclick="saveComment(${commentId})" class="btn btn-primary btn-sm me-2 comment-save-btn">Save</button>
    <button onclick="toggleEditForm(${commentId})" class="btn btn-secondary btn-sm">Cancel</button>
    </div>`
  } else {
    editBtn.classList.replace("btn-primary", "btn-light")
    content.innerHTML = content.dataset.content
    delete content.dataset.content
  }
}

function saveComment(commentId) {
  toggleBtnLoading(commentId, 'comment-save-btn')
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
      } else {
        toggleBtnLoading(commentId, 'comment-save-btn')
      }
    })
}

function toggleBtnLoading(commentId, btnClass) {
  const comment = document.getElementById("comment-" + commentId)
  const btn = comment.getElementsByClassName(btnClass)[0]
  const icon = btn.getElementsByTagName("i")[0]
  if (icon && !icon.classList.contains("loading-icon")) {
    if (icon.classList.contains("fa-spin")) {
      btn.classList.remove("disabled")
      icon.classList.replace("fa-solid", "fa-regular")
      icon.classList.remove("fa-spin")
      icon.classList.replace("fa-circle-notch", btn.dataset.icon)
    } else {
      btn.classList.add("disabled")
      iconName = Array.from(icon.classList).filter(c => c !== "fa-regular").pop()
      icon.dataset.icon = iconName
      icon.classList.remove(iconName)
      icon.classList.replace("fa-regular", "fa-solid")
      icon.classList.add("fa-spin", "fa-circle-notch")
    }
  } else {
    if (btn.innerHTML.includes("loading-icon")) {
      btn.innerHTML = btn.dataset.content
      btn.classList.remove("disabled")
    } else {
      btn.classList.add("disabled")
      btn.dataset.content = btn.innerHTML
      btn.innerHTML = `<i class="fa-solid fa-spin fa-circle-notch loading-icon"></i>`
    }
  }
}