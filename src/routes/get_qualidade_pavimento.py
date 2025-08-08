from datetime import datetime
import os
import time
import psutil
from flask import Blueprint, request
from src.helpers.errors.errors import MissingParameters, NoItemsFound
from src.helpers.external_interfaces.http_lambda_requests import CloudFunctionHttpRequest, CloudFunctionHttpResponse
from src.helpers.functions.logger import Logger
from src.infra.repositories.repository import Repository
from src.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.helpers.external_interfaces.external_interface import IRequest

logger = Logger.get_logger()

class Controller:
  @staticmethod
  def execute(request: IRequest):
    try:
      process = psutil.Process(os.getpid())
      start_time = time.perf_counter()
      start_memory = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
      start_cpu = process.cpu_percent()
      
      logger.info(f"Request received: {request.data}")
      
      usecase = Usecase()
      
      protocolo_id = request.data.get("protocolo_id")
      
      if not protocolo_id:
        logger.error('Missing protocolo_id in request')
        raise MissingParameters("protocolo_id")
      
      protocolo_id = int(protocolo_id)
      
      logger.info('Finished processing params of request')
      
      response = usecase.execute(protocolo_id)      
      
      return OK(
        body=response.to_dict()
      )
      
    except MissingParameters as e:
      logger.error(f"Missing parameters: {e.message}")
      
      return BadRequest({'message': e.message})
    except NoItemsFound as e:
      logger.error(f"No items found: {e.message}")
      
      return NotFound({'message': e.message})
    except Exception as e:
      logger.error(f"An INTERNAL error occurred: {str(e)}")
      
      return InternalServerError(str(e))
    
    finally:
      end_time = time.perf_counter()
      end_memory = process.memory_info().rss / (1024 * 1024)
      end_cpu = process.cpu_percent()
      
      elapsed_time = end_time - start_time
      memory_usage = end_memory - start_memory
      
      logger.info(f"Request processing time: {elapsed_time:.2f} seconds")
      logger.info(f"Final Memory: {end_memory:.2f} MB (Δ {memory_usage:+.2f} MB)")
      logger.info(f"Final CPU: {end_cpu:.2f}%")
      logger.info(f"System Memory: {psutil.virtual_memory().percent:.1f}% used")
      logger.info(f"System CPU: {psutil.cpu_percent(interval=1):.1f}% used")

class Usecase:
  repository: Repository
  
  def __init__(self):
    self.repository = Repository(pavimento_repo=True)
    self.http_repo = self.repository.pavimento_repo[0]
    self.cache_repo = self.repository.pavimento_repo[1]
    
  def execute(self, protocolo_id: int):
    logger.info(f"Executing usecase with protocolo_id: {protocolo_id}")
    
    access_token = self.http_repo.authenticate()
    
    logger.info(f"Authenticated successfully!")
    
    today = datetime.now()
    first_day_of_month = today.day == 1
    
    logger.info(f"Is first day of month: {first_day_of_month}")
    
    if not first_day_of_month:
      logger.info(f"Not first day of month, checking cache for protocolo_id: {protocolo_id}")
      pavimento = self.cache_repo.get_pavimento(protocolo_id)
      
      if not pavimento:
        logger.info(f"Pavimento not found in cache for protocolo_id: {protocolo_id}, fetching from HTTP repository")
        
        pavimento = self.http_repo.get_pavimento(protocolo_id, access_token)
        
        if not pavimento:
          logger.error(f"No pavimento found for protocolo_id: {protocolo_id}")
          raise NoItemsFound(f"protocolo_id - {protocolo_id}")
        
        logger.info(f"Fetched pavimento from HTTP repository for protocolo_id: {protocolo_id}")
        
        self.cache_repo.save_pavimento(pavimento)
        
        logger.info(f"Saved pavimento to cache for protocolo_id: {protocolo_id}")
      
      else:
        logger.info(f"Pavimento found in cache for protocolo_id: {protocolo_id}")
        
        return pavimento
    else:
      logger.info(f"First day of month, fetching pavimento from HTTP repository for protocolo_id: {protocolo_id}")
      
      pavimento = self.http_repo.get_pavimento(protocolo_id, access_token)
      if not pavimento:
        logger.error(f"No pavimento found for protocolo_id: {protocolo_id}")
        raise NoItemsFound(f"protocolo_id - {protocolo_id}")
      
      self.cache_repo.save_pavimento(pavimento)
      
      logger.info(f"Saved pavimento for protocolo_id: {protocolo_id}")
    
    if not pavimento:
      logger.error(f"No pavimento found for protocolo_id: {protocolo_id}")
      raise NoItemsFound(f"protocolo_id - {protocolo_id}")
      
    return pavimento
    
  
app = Blueprint("qualidade_pavimento", __name__)
@app.route("/qualidade-pavimento", methods=["GET"])
def qualidade_pavimento():
  http_request = CloudFunctionHttpRequest(request)
  response = Controller.execute(http_request)
  print(f"Response: {response}")
  http_response = CloudFunctionHttpResponse(
    body=response.body,
    status_code=response.status_code,
    headers=response.headers
  )
  
  return http_response.to_flask_response()
  