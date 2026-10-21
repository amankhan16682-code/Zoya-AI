import os
import re
import asyncio
import subprocess
import edge_tts
from openai import OpenAI

os.environ["NVIDIA_API_KEY"] = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

chat_history = [
    {"role": "system", "content": "Tum Zoya ho, ek pyari aur helpful Indian ladki. Tum apne user se dosti se baat karti ho. Jawab natural rakho."}
]

async def speak_zoya(text):
    # Yahan hum saare symbols, emojis, stars sab hata rahe hain
    clean_text = re.sub(r'[^a-zA-Z0-9\s,.\'?!\u0900-\u097F]', '', text)
    
    print("\n(Zoya bol rahi hai...)")
    voice = "en-IN-NeerjaNeural" 
    communicate = edge_tts.Communicate(clean_text, voice, rate="-5%", pitch="+2Hz")
    await communicate.save("zoya_voice.mp3")
    subprocess.run(["mpv", "--no-video", "zoya_voice.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ask_zoya(prompt):
    global chat_history
    print("\nZoya soch rahi hai...")
    chat_history.append({"role": "user", "content": prompt})
    
    if len(chat_history) > 10:
        chat_history = [chat_history[0]] + chat_history[-8:]

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b",
            messages=chat_history,
            temperature=0.6,
            max_tokens=800 # Yahan limit badha di hai
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error aaya: {e}"

print("--- Zoya AI (Final Version) ---")
while True:
    user_input = input("\nAap: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Zoya: Alvida! Phir milenge.")
        asyncio.run(speak_zoya("Alvida! Phir milenge."))
        break
    
    jawab = ask_zoya(user_input)
    print(f"Zoya: {jawab}")
    asyncio.run(speak_zoya(jawab))
