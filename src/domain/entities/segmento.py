from datetime import datetime


class Segmento:
  obra_id: int
  geometria: dict
  cor: int
  data: datetime
  
  def __init__(
    self,
    obra_id: int,
    geometria: dict,
    cor: int,
    data: datetime
  ):
    
    self.obra_id = obra_id
    self.geometria = geometria
    self.cor = cor
    self.data = data
    
  def to_dict(self):
    return {
      "obra_id": self.obra_id,
      "geometria": self.geometria,
      "cor": self.cor,
      "data": self.data.isoformat() if isinstance(self.data, datetime) else self.data
    }
  
  @classmethod
  def from_dict(cls, data: dict):
    return cls(
      obra_id=data.get("obra_id"),
      geometria=data.get("geometria"),
      cor=data.get("cor"),
      data=datetime.fromisoformat(data.get("data")) if data.get("data") else None
    )
    
  