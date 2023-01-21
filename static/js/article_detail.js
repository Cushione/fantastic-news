function deleteComment(commentId) {
  // Confirm comment deletion
  if (!confirm("Do you really want to delete this comment?")) {
    // Stop function if deletion is cancelled
    return;
  }
  // Set delete button to loading
  toggleBtnLoading(commentId, "comment-delete-btn");
  // Retrieve CSRF token from the cookies
  const csrftoken = Cookies.get("csrftoken");
  // Send delete request
  fetch("/comments/" + commentId, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
  })
    .then((response) => {
      if (response.ok) {
        // If request was successful, overwrite comment content and remove buttons
        const comment = document.getElementById("comment-" + commentId);
        const content = comment.getElementsByClassName("comment-content")[0];
        content.innerHTML = "This comment was deleted.";
        const buttons = comment.getElementsByClassName("action-buttons")[0];
        buttons.innerHTML = "";
      }
    })
    .catch(() => {
      // If request failed, enable delete button
      toggleBtnLoading(commentId, "comment-delete-btn");
    });
}

function toggleEditForm(commentId) {
  // Find all necessary HTML elements
  const comment = document.getElementById("comment-" + commentId);
  const content = comment.getElementsByClassName("comment-content")[0];
  const editBtn = comment.getElementsByClassName("comment-edit-btn")[0];

  // Check if the content has the data attribute content i.e. if the form is active
  if (!content.dataset.content) {
    // If the data attribute does not exist, set it with the comment content and replace
    // the comment body with the editing form and buttons
    editBtn.classList.replace("btn-light", "btn-primary");
    content.dataset.content = content.innerHTML;
    content.innerHTML = `
    <textarea id="comment-${commentId}-textarea" class="form-control">${content.innerHTML.trim()}</textarea>
    <div class="d-flex justify-content-end mt-2">
    <button onclick="saveComment(${commentId})" class="btn btn-primary btn-sm me-2 comment-save-btn">Save</button>
    <button onclick="toggleEditForm(${commentId})" class="btn btn-secondary btn-sm">Cancel</button>
    </div>`;
  } else {
    // If the data attribute exists, replace the comment body with the original
    // comment body and delete the data attribute
    editBtn.classList.replace("btn-primary", "btn-light");
    content.innerHTML = content.dataset.content;
    delete content.dataset.content;
  }
}

function saveComment(commentId) {
  // Set save button to loading
  toggleBtnLoading(commentId, "comment-save-btn");
  // Retrieve CSRF token from the cookies
  const csrftoken = Cookies.get("csrftoken");
  // Wrap new comment content in form data
  const newContent = document.getElementById(
    "comment-" + commentId + "-textarea"
  ).value;
  const data = new FormData();
  data.append("content", newContent);
  // Send post request with form data as body
  fetch("/comments/" + commentId, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: data,
  })
    .then((response) => {
      if (response.ok) {
        // If request was successful, set content data attribute to the
        // new content and toggle form
        const content = document
          .getElementById("comment-" + commentId)
          .getElementsByClassName("comment-content")[0];
        content.dataset.content = newContent;
        toggleEditForm(commentId);
      }
    })
    .catch(() => {
      // If request failed, enable save button
      toggleBtnLoading(commentId, "comment-save-btn");
    });
}

function toggleBtnLoading(commentId, btnClass) {
  // Find all necessary HTML elements
  const comment = document.getElementById("comment-" + commentId);
  const btn = comment.getElementsByClassName(btnClass)[0];
  const icon = btn.getElementsByTagName("i")[0];
  // If the button has an icon but is not a currently loading text button
  // i.e. the button is an icon button
  if (icon && !icon.classList.contains("loading-text-button")) {
    // If the button icon is currently spinning i.e. loading,
    // then enable button and restore original icon
    if (icon.classList.contains("fa-spin")) {
      btn.classList.remove("disabled");
      icon.classList.replace("fa-solid", "fa-regular");
      icon.classList.remove("fa-spin");
      icon.classList.replace("fa-circle-notch", btn.dataset.icon);
      // If the button icon is not spinning i.e. active,
      // disable button, store original icon and replace with spinning icon
    } else {
      btn.classList.add("disabled");
      const iconName = Array.from(icon.classList)
        .filter((c) => c !== "fa-regular")
        .pop();
      icon.dataset.icon = iconName;
      icon.classList.remove(iconName);
      icon.classList.replace("fa-regular", "fa-solid");
      icon.classList.add("fa-spin", "fa-circle-notch");
    }
    // If the button is a text button
  } else {
    // If the button has an icon, then the button is loading,
    // so we replace icon with the original text and enable the button
    if (btn.innerHTML.includes("loading-text-button")) {
      btn.innerHTML = btn.dataset.content;
      btn.classList.remove("disabled");
      // If the button has no icon, then the button is not loading,
      // so we store the original text, add loading icon and disable the button
    } else {
      btn.classList.add("disabled");
      btn.dataset.content = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-spin fa-circle-notch loading-text-button"></i>`;
    }
  }
}
