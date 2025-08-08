from src.domain.entities.pavimento import Pavimento
from src.domain.entities.segmento import Segmento
from src.domain.repositories.pavimento_repository_interface import IPavimentoRepository
from sqlalchemy.orm import Session
from src.infra.repositories.cache.sqlalchemy.models import SegmentoModel
from shapely.wkb import dumps as wkb_dumps, loads as wkb_loads
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer

class PavimentoRepositorySQLite(IPavimentoRepository):
  def __init__(self, db_connection: Session):
    self.db_connection = db_connection
    
  def get_pavimento(self, protocolo_id: int):
    # 1 pavimento is an array of segmentos
    segmentos = self.db_connection.query(SegmentoModel).filter(SegmentoModel.protocolo_id == protocolo_id).all()
    
    if not segmentos:
      return None
    
    segmentos_list = []
    transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)
    
    for segmento in segmentos:
      shapely_geom_31983 = wkb_loads(segmento.geometria, hex=True)
      shapely_geom_4326 = transform(transformer.transform, shapely_geom_31983)
      geojson_geom = mapping(shapely_geom_4326)
      
      segmento_entity = Segmento(
        obra_id=segmento.obra_id,
        data=segmento.data,
        cor=segmento.cor,
        geometria=geojson_geom
      )
      
      segmentos_list.append(segmento_entity)
    
    pavimento = Pavimento(
      protocolo_id=protocolo_id,
      trechos=segmentos_list
    )
    
    return pavimento
  
  def save_pavimento(self, pavimento: Pavimento):
    segmentos_model_dicts = []
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)
    
    for segmento in pavimento.trechos:
      shapely_geom_4326 = shape(segmento.geometria)
      shapely_geom_31983 = transform(transformer.transform, shapely_geom_4326)
      wkb_geom = wkb_dumps(shapely_geom_31983, hex=True, include_srid=True, srid=31983)
      
      segmentos_model_dicts.append({
        "obra_id": segmento.obra_id,
        "geometria": wkb_geom,
        "data": segmento.data,
        "cor": segmento.cor,
        "protocolo_id": pavimento.protocolo_id
      })
      
    self.db_connection.bulk_insert_mappings(SegmentoModel, segmentos_model_dicts)
    self.db_connection.commit()
      