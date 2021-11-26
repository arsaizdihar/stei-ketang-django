from typing import Any, List, Optional

import pandas as pd
from api.models import Candidate
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("session", type=int)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        numbers = []
        names = []
        votes = []
        session = options.get("session")
        candidates = Candidate.objects.filter(active=True).all()

        for candidate in candidates:
            numbers.append(candidate.number)
            names.append(candidate.name)
            votes.append(candidate.votes.filter(session=session).count())
        df = pd.DataFrame({"No": numbers, "Nama": names, "Vote": votes})
        
        df.to_excel(f"documents/votes{session}.xlsx", index=False)

        

            
