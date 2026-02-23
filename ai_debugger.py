import os
import sys
from groq import Groq

# Initialize Groq
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_content(path):
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()
    return "Not Found"

# Collecting Context
error_log = sys.argv[1] if len(sys.argv) > 1 else "No logs found"
pubspec = get_content("pubspec.yaml")
manifest = get_content("android/app/src/main/AndroidManifest.xml")

prompt = f"""
Flutter Build Error Analysis:
ERROR LOG:
{error_log}

CONTEXT FILES:
1. pubspec.yaml:
{pubspec}

2. AndroidManifest.xml:
{manifest}

TASK:
Identify the file causing the error (Dart code, pubspec, or AndroidManifest).
Return ONLY the corrected code of that file.
The first line MUST be: 'FILE: path/to/file'
Example:
FILE: pubspec.yaml
name: my_app
...
"""

try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = completion.choices[0].message.content.strip()
    
    # Extracting file path and new content
    if response.startswith("FILE:"):
        lines = response.split('\n')
        target_file = lines[0].replace("FILE:", "").strip()
        # Clean up code blocks if AI added them
        new_content = "\n".join(lines[1:]).replace("```yaml", "").replace("```dart", "").replace("```xml", "").replace("```", "")
        
        with open(target_file, "w") as f:
            f.write(new_content.strip())
        print(f"✅ AI successfully updated: {target_file}")
    else:
        print("❌ AI response was not in the correct format (Missing FILE: tag).")

except Exception as e:
    print(f"❌ Critical Error in AI Debugger: {e}")
    sys.exit(1)
