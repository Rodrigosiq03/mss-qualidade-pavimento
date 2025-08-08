from src.domain.entities.pavimento import Pavimento
from src.domain.entities.segmento import Segmento
from src.domain.repositories.pavimento_repository_interface import IPavimentoRepository

class GaiaPavimentoRepositoryMock(IPavimentoRepository):
  def __init__(self):
    self.pavimentos = [
      {
        "protocolo_id": 1,
        "trechos": [
          {
            "obra_id": 1,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.578918236, -23.498351634]
            },
            "cor": 1,
            "data": "2018-05-20T00:00:00.000Z"
          }
        ]
      },
      {
        "protocolo_id": 2,
        "trechos": [
          {
            "obra_id": 2,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.578918236, -23.498351634]
            },
            "cor": 3,
            "data": "2019-08-01T00:00:00.000Z"
          }
        ]
      },
      {
        "protocolo_id": 3,
        "trechos": [
          {
            "obra_id": 3,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.581234567, -23.501234567]
            },
            "cor": 2,
            "data": "2020-03-15T00:00:00.000Z"
          }
        ]
      },
      {
        "protocolo_id": 4,
        "trechos": [
          {
            "obra_id": 4,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.585432109, -23.505432109]
            },
            "cor": 1,
            "data": "2021-06-22T00:00:00.000Z"
          }
        ]
      },
      {
        "protocolo_id": 5,
        "trechos": [
          {
            "obra_id": 5,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.590987654, -23.510987654]
            },
            "cor": 4,
            "data": "2022-11-08T00:00:00.000Z"
          }
        ]
      },
      {
        "protocolo_id": 6,
        "trechos": [
          {
            "obra_id": 6,
            "geometria": {
              "type": "Point",
              "coordinates": [-46.595123456, -23.515123456]
            },
            "cor": 5,
            "data": "2023-02-14T00:00:00.000Z"
          }
        ]
      }
    ]
      
  def get_pavimento(self, protocolo_id: int, access_token: str = None) -> Pavimento:
    for pavimento in self.pavimentos:
      if pavimento["protocolo_id"] == protocolo_id:
        return pavimento
    return None
  
  def save_pavimento(self, pavimento: Pavimento):
    pass
  
  def authenticate(self):
    return "mocked_token"
    
  