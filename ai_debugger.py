import os
import sys
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_content(path):
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()
    return "Not Found"

# Context ikatha karna
error_log = sys.argv[1] if len(sys.argv) > 1 else "No logs"
pubspec = get_content("pubspec.yaml")
manifest = get_content("android/app/src/main/AndroidManifest.xml")

prompt = f"""
Flutter Build Error Analysis:
ERROR: {error_log}

FILES CONTEXT:
1. pubspec.yaml:
{pubspec}

2. AndroidManifest.xml:
{manifest}

TASK:
1. Identify if the fix is needed in pubspec.yaml, AndroidManifest.xml, or a Dart file.
2. Return ONLY the corrected code of the file that needs fixing.
3. Start the response with 'FILE: path/to/file' so I can save it.
"""

try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = completion.choices[0].message.content.strip()
    
    # Logic to extract filename and content
    if response.startswith("FILE:"):
        lines = response.split('\n')
        target_file = lines[0].replace("FILE:", "").strip()
        new_content = "\n".join(lines[1:]).replace("```", "") # Remove code blocks if AI adds them
        
        with open(target_file, "w") as f:
            f.write(new_content)
        print(f"✅ AI fixed: {target_file}")
    else:
        print("❌ AI response format was unexpected.")

except Exception as e:
    print(f"❌ Error: {e}")
