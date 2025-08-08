from typing import List
from src.domain.entities.segmento import Segmento

class Pavimento:
  protocolo_id: int
  trechos: List[Segmento]
  
  def __init__(self, protocolo_id: int, trechos: List[Segmento]):
    self.protocolo_id = protocolo_id
    self.trechos = trechos
    
  def to_dict(self):
    return {
      "protocolo_id": self.protocolo_id,
      "trechos": [trecho.to_dict() for trecho in self.trechos]
    }    
    
  @classmethod
  def from_dict(cls, data: dict):
    return cls(
      protocolo_id=data.get("protocolo_id"),
      trechos=[Segmento.from_dict(trecho) for trecho in data.get("trechos", [])]
    )