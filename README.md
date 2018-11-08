# uprofile
For this project, you’ll build a form that takes in details about a registered user and displays those details on a profile page. The profile page should only be visible once the user has logged in. The profile page should include first name, last name, email, date of birth, confirm email, short bio and the option to upload an avatar

You’ll also set up validation for email, date of birth and the biography. The date of birth validation should accept three date formats: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. The Email validation should check if the email addresses match and are in a valid format. The bio validation should check that the bio is 10 characters or longer and properly escapes HTML formatting

You’ll also create a "change password page" that updates the user’s password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy:

* not the same as current password
* has a minimum length of 14 characters
* uses both uppercase and lowercase letters
* includes one or more numerical digits
* includes one or more special characters, such as @, #, $
* doesn't contain the username or parts of the user’s full name, such as their first name
