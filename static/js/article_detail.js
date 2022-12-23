function deleteComment(commentId) {
  const csrftoken = Cookies.get('csrftoken');
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