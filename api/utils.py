from django.core.signing import Signer
from users.models import ChangePasswordKey


def create_code(user_id) -> str:
    key = ChangePasswordKey.objects.create(user_id=user_id)
    signer = Signer()
    code = signer.sign_object({
        "id": key.id,
        "full_name": key.user.full_name,
        "email": key.user.email
    })
    return code
