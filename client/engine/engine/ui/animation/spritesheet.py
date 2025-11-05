from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SpriteSheetData:
    image: str
    rows: int
    columns: int
    animations: Dict[str, List[int]] = field(default_factory=dict)
