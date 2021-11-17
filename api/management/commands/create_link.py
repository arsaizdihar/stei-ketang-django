import random
import string
from typing import Any, List, Optional

import pandas as pd
from api.utils import create_code
from django.core.management.base import BaseCommand, CommandParser
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        emails = []
        full_names = []
        links = []
        users: List[User] = User.objects.select_related("change").order_by("email").all()

        for user in users:
            if not hasattr(user, "change"):
                code = create_code(user.id)
                emails.append(user.email)
                full_names.append(user.full_name)
                links.append(f"https://stei-ketang.vercel.app/password?code={code}")
        
        df = pd.DataFrame({"email": emails, "nama": full_names, "link": links})
        df.to_csv(f"documents/{options.get('file')}.csv", index=False)

            
