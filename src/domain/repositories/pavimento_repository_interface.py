from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.pavimento import Pavimento


class IPavimentoRepository(ABC):
  @abstractmethod
  def get_pavimento(self, protocolo_id: int, acess_token: Optional[str] = None) -> Pavimento:
    pass
  
  @abstractmethod
  def save_pavimento(self, pavimento) -> Pavimento:
    pass