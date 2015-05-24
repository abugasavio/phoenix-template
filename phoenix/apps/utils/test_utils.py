from model_mommy import mommy


def login_user(test_case, user, password):
    test_case.client.logout()
    test_case.client.login(username=user.username, password=password)


def create_logged_in_user(test_case, username='mary', password='marypassword'):
    user = mommy.make('auth.User')
    user.username = username
    user.set_password(password)
    user.save()
    login_user(test_case, user, password)
    return user