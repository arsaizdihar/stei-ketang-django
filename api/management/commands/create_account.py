import random
import string
from typing import Any, Optional

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        df = pd.read_csv(f"documents/{options.get('file')}.csv")

        for i, row in df.iterrows():
            nim = row["NIM"]
            name = row["Nama"]
            email = f"{nim}@mahasiswa.itb.ac.id"
            user = User.objects.filter(email=email).first()
            if not user:
                chars = string.ascii_letters + string.digits + string.punctuation
                password = "".join(random.choices(chars, k=8))
                user = User.objects.create_user(email, name, password)
                print(user.email)

            
