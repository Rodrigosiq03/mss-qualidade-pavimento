import requests
from src.environments import Environments
from src.domain.entities.pavimento import Pavimento
from src.domain.repositories.pavimento_repository_interface import IPavimentoRepository

class GaiaPavimentoRepositoryHttp(IPavimentoRepository):
  def __init__(self):
    self.base_url = Environments.gaia_pavimento_url
    
  def get_pavimento(self, protocolo_id: int, access_token: str) -> Pavimento:
    url = f"{self.base_url}/pavimento/qualidade?protocolo_id={protocolo_id}"
    response = requests.get(url, headers={"Authorization": access_token})
    
    if response.status_code == 200:
      data = response.json()
      
      pavimento_entity = Pavimento.from_dict(data)
      
      return pavimento_entity
    else:
      
      json_error = response.json()
      
      if "Qualidade do pavimento não encontrada para o protocolo" in json_error.get("message"):
        return None
      
      raise Exception(f"Error fetching pavimento data: {response.status_code} - {response.text}")
    
  def save_pavimento(self, pavimento):
    pass
  
  def authenticate(self):
    body = {
      "username": Environments.gaia_username,
      "password": Environments.gaia_password
    }

    response = requests.post(
      f"{Environments.gaia_pavimento_url}/pavimento/authenticate", 
      headers={"Content-Type": "application/json"},
      json=body
    )
    
    if response.status_code == 200:
      json_response = response.json()

      tokens = json_response.get("tokens")

      return tokens.get("access_token")