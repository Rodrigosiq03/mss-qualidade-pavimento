from typing import Any, List

from src.infra.repositories.cache.sqlalchemy.connection import Connection
from src.domain.repositories.pavimento_repository_interface import IPavimentoRepository
from src.environments import STAGE, Environments
from src.infra.repositories.cache.pavimento_repository_sqlite import PavimentoRepositorySQLite
from src.infra.repositories.http.gaia_pavimento_repository_http import GaiaPavimentoRepositoryHttp
from src.infra.repositories.mock.gaia_pavimento_repository_mock import GaiaPavimentoRepositoryMock
from src.infra.repositories.mock.pavimento_repository_mock import PavimentoRepositoryMock

class Repository:
    pavimento_repo: List[IPavimentoRepository]
    
    def __init__(
            self,
            pavimento_repo: bool = False,
    ):
        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                pavimento_repo
            )
        else:
            connection = Connection()
            self.session = connection.get_session()
            self.engine = connection.engine
            
            self._initialize_repositories(
                pavimento_repo
            )

    def _initialize_mock_repositories(self, pavimento_repo: bool = False):
        if pavimento_repo:
            self.pavimento_repo = [
                GaiaPavimentoRepositoryMock(), 
                PavimentoRepositoryMock()
            ]

    def _initialize_repositories(self, pavimento_repo: bool = False):
        if pavimento_repo:
            self.pavimento_repo = [
                GaiaPavimentoRepositoryHttp(),
                PavimentoRepositorySQLite(db_connection=self.session)
            ]