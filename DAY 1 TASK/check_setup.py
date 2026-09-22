"""Step 1: run this first. It checks the environment and the model connection."""
import sys

from config import INTERN_PROFILE, MODEL, PROVIDER, client

print("Python version :", sys.version.split()[0])
print("Provider       :", PROVIDER)
print("Model          :", MODEL)
print("Intern loaded  :", INTERN_PROFILE["intern_name"], "@", INTERN_PROFILE["current_company"])

print("\nCalling the model ...")
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Reply with exactly these two words: SETUP OK"}],
    temperature=0,
)
print("Model replied  :", response.choices[0].message.content.strip())

print("\nSetup check finished.")
