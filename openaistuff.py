import os, sys
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
print(openai.api_key)
