from typing import Any, List, Optional

import pandas as pd
from api.models import Candidate
from django.core.management.base import BaseCommand, CommandParser
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("session", type=int)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        names = []
        emails = []
        voted = []
        session = options.get("session")
        users = User.objects.prefetch_related("votes").all()

        for user in users:
            names.append(user.full_name)
            emails.append(user.email)
            voted.append(user.votes.filter(session=session).exists())
        
        df = pd.DataFrame({"nama": names, "email": emails, "voted": voted})
        df.sort_values(["voted", "email"], inplace=True)
        df.to_excel(f"documents/votes_detail{session}.xlsx", index=False)

        

            
