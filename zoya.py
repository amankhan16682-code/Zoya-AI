import os
from openai import OpenAI

# Apni NVIDIA API Key yahan set kar di hai
os.environ["NVIDIA_API_KEY"] = "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"

# NVIDIA ke server se connect karein
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

def ask_zoya(prompt):
    print("\nZoya soch rahi hai...")
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b", # Fast aur free model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error aaya: {e}"

# Chat shuru karein
print("--- Zoya AI Started ---")
while True:
    user_input = input("\nAap: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Zoya: Alvida! Phir milenge.")
        break
    
    jawab = ask_zoya(user_input)
    print(f"Zoya: {jawab}")

