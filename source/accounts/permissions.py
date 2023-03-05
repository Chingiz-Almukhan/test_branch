from django.contrib.auth.mixins import UserPassesTestMixin


def is_admin(user) -> bool:
    return user.groups.filter(name='admin').exists()


class AdminPassedTestMixin(UserPassesTestMixin):

    def test_func(self) -> bool:
        return self.request.user.groups.filter(name='admin').exists()
