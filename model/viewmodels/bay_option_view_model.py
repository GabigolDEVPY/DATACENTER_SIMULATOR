from dataclasses import dataclass
from server.models import Bay


@dataclass
class BayOption:
    bay: Bay
    max_instances: int | None = None

    @property
    def id(self):
        return self.bay.id

    @property
    def name(self):
        return self.bay.name

    @property
    def rack(self):
        return getattr(self.bay, "rack", None)