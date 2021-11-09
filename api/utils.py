from django.core.signing import Signer
from users.models import ChangePasswordKey


def create_code(user_id) -> str:
    key = ChangePasswordKey.objects.create(user_id=user_id)
    signer = Signer()
    code = signer.sign(key.id)
    return code
