from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        token = text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        print(token)
        return token


account_activation_token = TokenGenerator()