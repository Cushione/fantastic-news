# Manual Testing

[Go to README](README.md)

| Testcase                          | Expected Result                                                       | Test Result |
|-----------------------------------|-----------------------------------------------------------------------|-------------|
| Open the Homepage                 | Homepage loads with the correct template and data                     | ✅ PASS          |
| Register a user with valid data   | Request is successful, user is registered and logged in               | ✅ PASS          |
| Register a user with invalid data | Request fails, form loads again with data and errors                  | ✅ PASS          |
| Login a user with valid data      | Request is successful, user is logged in                              | ✅ PASS          |
| Login a user with invalid data    | Request fails, form loads again with data and errors                  | ✅ PASS          |
| Open an article by clicking       | Article Detail page loads with correct template and data              | ✅ PASS          |
| Open an article through url       | Article Detail page loads with correct template and data              | ✅ PASS          |
| Open an article with invalid url  | 404 Error page is shown                                               | ✅ PASS          |
| Liking an article                 | Like count increases and like button changes                          | ✅ PASS          |
| Unliking an article               | Like count decreases and like button changes                          | ✅ PASS          |
| **Commenting**                    |                                                                       |             |
| Writing a comment                 | Request is successful, comment is added to the list, message is shown | ✅ PASS          |
| Editing a comment                 | Request is successful, comment content is edited, message is shown    | ✅ PASS          |
| Delete a comment                  | Request is successful, comment is deleted, message is shown           | ✅ PASS          |
| **Unauthorised requests**         |                                                                       |             |
| Liking an article                 | Request fails, redirect to login page                                 | ✅ PASS          |
| Writing a comment                 | Request fails, redirect to login page                                 | ✅ PASS          |
| Editing a comment                 | Request fails, redirect to login page                                 | ✅ PASS          |
| Delete a comment                  | Request fails, redirect to login page                                 | ✅ PASS          |