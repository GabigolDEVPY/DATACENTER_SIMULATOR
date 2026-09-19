from dataclasses import dataclass
from server.models import Bay

@dataclass
class BayOption:
    bay: Bay
    max_instances: int