import os

from dotenv import load_dotenv
load_dotenv()

TIMEOUT_DOCKER= int(os.getenv('TIMEOUT_DOCKER'))
WORK_DIR_DOCKER=os.getenv('WORK_DIR_DOCKER')
MODEL_OPENAI = os.getenv('MODEL_OPENAI')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
DEFAULT_TERMINATION_PHRASE=os.getenv('DEFAULT_TERMINATION_PHRASE')
DEFAULT_MAX_TURNS=int(os.getenv('DEFAULT_MAX_TURNS'))