import pytest

email = "test.task.test.01@gmail.com"
password = "123456qwerty123456!"
phone_number = "+380969648973"

account_not_found_msg = "Couldn’t find your Google Account"
invalid_email_msg = "Enter a valid email or phone number"
enter_email_or_phone_message = "Enter an email or phone number"

enter_password_msg = "Enter a password"
wrong_password_msg = "Wrong password. Try again or click Forgot password to reset it."


# Positive tests:
@pytest.mark.parametrize("email", [
    email,                  # correct email
    email.upper(),          # correct email upper case
    email.capitalize(),     # correct email, first item is upper case
    f" {email} ",           # correct email with whitespaces
    f"           {email}",  # correct email with many whitespaces
])
def test_login_with_email(desktop_app, email):
    desktop_app.login(email, password)
    assert desktop_app.check_gmail_inbox(), "Error: Gmail login failed"


@pytest.mark.parametrize("mobile_number", [
    phone_number,
    phone_number[1:],
    phone_number[3:],
    phone_number[4:],
])
def test_login_with_phone_number_captcha(desktop_app, mobile_number):
    pass
    #  TODO:  Add a method to check the captcha (JIRA-XXX)


@pytest.mark.parametrize("mobile_number", [
    phone_number,
    phone_number[1:],
    phone_number[3:],
    phone_number[4:],
])
def test_login_with_mobile_number_and_password(desktop_app, mobile_number):
    desktop_app.login_with_phone_number_and_password(mobile_number, password)
    assert (
        desktop_app.check_gmail_inbox(),
        "Error: Gmail login with mobile number failed"
    )


#  Negative tests:
@pytest.mark.parametrize(("email", "message"), [
    ("test.task.test.01gmail.com", account_not_found_msg),  # Email without @ symbol
    ("task.test.01gmail.com", account_not_found_msg),       # Non-existing email
    (f"{password}", account_not_found_msg),                 # Using password instead of login email
    (f"o{phone_number[4:]}", account_not_found_msg),        # Phone number with incorrect format
    ("", enter_email_or_phone_message),                     # Empty field
    ("                     ", invalid_email_msg),           # Many white spaces
    ("test.task.test.01@", invalid_email_msg),              # Email without gmail
    (f"<{email}>", invalid_email_msg),                      # Correct email with <>
    ("~!#$%^&*()?>@,./\<][/*<!–", invalid_email_msg),       # Special characters
    (f"{phone_number[2:]}", invalid_email_msg),             # Phone number without prefix
])
def test_login_invalid_or_nonexistent_user(desktop_app, email, message):
    desktop_app.enter_user_email_or_phone_number(email)
    assert (
        desktop_app.verify_field_not_found_message(message),
        f"Verify that {account_not_found_msg} or {invalid_email_msg} or {enter_email_or_phone_message} message is displayed"
    )


@pytest.mark.parametrize(("password", "message"), [
    ("password123", wrong_password_msg),                # Incorrect password
    ("", enter_password_msg),                           # Empty password
    ("~!#$%^&*()?>@,./\<][/*<!–", wrong_password_msg),  # Special characters
    ("123456qWerty123456!", wrong_password_msg),        # correct email 'W' upper case
    ("123456 qwerty123456", wrong_password_msg),        # correct email with whitespace
])
def test_login_invalid_password(desktop_app, password, message):
    desktop_app.login(email, password)
    assert (
        desktop_app.verify_field_not_found_message(message),
        f"Verify that {enter_password_msg} or {wrong_password_msg} message is displayed"
    )
