import logging
from pynput.keyboard import Controller
import pytesseract



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("google_genai.models").setLevel(logging.ERROR)
logging.getLogger("telegram.ext.Application").setLevel(logging.WARNING)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # <-- default tesseract path
keyboard = Controller()
