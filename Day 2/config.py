"""Shared configuration: chooses the LLM provider and loads the private
internship data."""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads the .env file in this folder

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":  # Option A: local model, no key
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"  # any text works for Ollama
    MODEL = os.getenv("MODEL", "qwen3:4b")
elif PROVIDER == "groq":  # Option B: free cloud key
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
elif PROVIDER == "huggingface":  # Option C: free cloud key
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# ---------------------------------------------------------------------------
# Private internship data that no public LLM has ever seen.
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "offers.json") as f:
    OFFERS = json.load(f)

with open(DATA_DIR / "payment_history.json") as f:
    PAYMENT_HISTORY = json.load(f)

with open(DATA_DIR / "intern_profile.json") as f:
    INTERN_PROFILE = json.load(f)

# Quick lookup: company name -> its offer entry
OFFERS_BY_COMPANY = {item["company"]: item for item in OFFERS}

QUESTIONS = [
    "How much total net stipend will Saran receive by the end of the TechNova internship?",
    "Which internship offer gives the highest total net stipend overall?",
    "How much net stipend has Saran already been paid so far?",
    "Write a two-line summary comparing all three offers by total net stipend.",
]


def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")
