import os
import asyncio
import subprocess
import edge_tts
from openai import OpenAI

# Aapki NVIDIA API Key yahan set kar di hai
os.environ["NVIDIA_API_KEY"] = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

async def speak_zoya(text):
    voice = "en-IN-NeerjaNeural" # Indian Hindi Female
    print("\n(Zoya bol rahi hai...)")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("zoya_voice.mp3")
    subprocess.run(["mpv", "--no-video", "zoya_voice.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ask_zoya(prompt):
    print("\nZoya soch rahi hai...")
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b", # Is model ko update kiya hai kyunki nemotron-3 purana/deprecated ho chuka hai
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error aaya: {e}"

print("--- Zoya AI (Voice Mode Started) ---")
while True:
    user_input = input("\nAap: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Zoya: Alvida! Phir milenge.")
        asyncio.run(speak_zoya("Alvida! Phir milenge."))
        break
    
    jawab = ask_zoya(user_input)
    print(f"Zoya: {jawab}")
    asyncio.run(speak_zoya(jawab))
