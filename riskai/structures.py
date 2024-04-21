import networkx as nx
from enum import Enum

class Card(Enum):
    INFANTRY = 1
    CAVALRY = 2
    ARTILLERY = 3
    WILD = 4



class Draft:
    def __init__(self, draft_id, draft_name, draft_type, draft_date, draft_status, draft_rounds, draft_teams):
        self.draft_id = draft_id
        self.draft_name = draft_name
        self.draft_type = draft_type
        self.draft_date = draft_date
        self.draft_status = draft_status
        self.draft_rounds = draft_rounds
        self.draft_teams = draft_teams
