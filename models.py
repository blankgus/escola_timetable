@dataclass
class Feriado:
    data: str
    motivo: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))