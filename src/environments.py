from enum import Enum
import os
from dotenv import load_dotenv

class STAGE(Enum):
    TEST = "TEST"
    DEV = "DEV"
    INTEGRATION = "INTEGRATION"
    QA = "QA"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"

class Environments:
    load_dotenv()
    stage: STAGE = STAGE(os.environ.get('STAGE', 'TEST'))
    gaia_pavimento_url: str = os.environ.get('GAIA_PAVIMENTO_URL', '')
    gaia_username: str = os.environ.get("GAIA_USERNAME", "")
    gaia_password: str = os.environ.get("GAIA_PASSWORD", "")