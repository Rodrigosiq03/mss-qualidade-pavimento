import os
import tempfile
from src.environments import STAGE, Environments
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import atexit
from src.infra.repositories.cache.sqlalchemy.models import Base

class Connection:
  _instance = None
  _engine = None
  _Session = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Connection, cls).__new__(cls)
      cls._instance._initialize()
    return cls._instance

  def _initialize(self):
    if self._engine is None:
      if Environments.stage.value == STAGE.TEST.value:
        self.database_url = ""
      else:
        self._temp_file = tempfile.mktemp(suffix='.db', prefix='pavement_cache_')
        self.database_url = f"sqlite:///{self._temp_file}"
        self.connect_args = {"check_same_thread": False}
        
        self._engine = create_engine(
          self.database_url,
          connect_args=self.connect_args,
          pool_pre_ping=True,
          echo=True,
        )
        
        Base.metadata.create_all(self._engine)
        
        self._Session = sessionmaker(
          bind=self._engine, expire_on_commit=False, autoflush=False
        )
        
        atexit.register(self._cleanup)

  def _cleanup(self):
    if self._temp_file and os.path.exists(self._temp_file):
      try:
        os.unlink(self._temp_file)
        print(f"🧹 Cache file {self._temp_file} cleaned up")
      except Exception as e:
        print(f"⚠️ Could not cleanup cache file: {e}")
  
  @property
  def engine(self):
    return self._engine
    
  def get_session(self):
    return self._Session()