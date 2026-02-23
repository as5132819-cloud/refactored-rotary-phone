import os
import sys
from groq import Groq

# Initialize Client
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_content(path):
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()
    return "NOT_FOUND"

# Context gathering
error_log = sys.argv[1] if len(sys.argv) > 1 else "No logs"
pubspec = get_content("pubspec.yaml")
manifest = get_content("android/app/src/main/AndroidManifest.xml")
main_dart = get_content("lib/main.dart") # Added main.dart as context too

# UNIVERSAL PROMPT: Logic based on "Chain of Verification"
prompt = f"""
ROLE: You are an Autonomous Flutter Compiler & Senior Architect.
GOAL: Fix the crash by providing a 100% syntactically perfect file.

[ERROR LOG]:
{error_log}

[PROJECT CONTEXT]:
- pubspec.yaml: {pubspec}
- AndroidManifest.xml: {manifest}
- lib/main.dart: {main_dart}

[STRICT PROTOCOL]:
1. ANALYZE: Cross-reference the Error Log with the provided files.
2. CORRECT: Fix the file responsible for the crash.
3. VALIDATE: 
   - Ensure DART syntax: Check all matching pairs of {{}} and (). Every statement MUST end with ;.
   - Ensure XML syntax: Every opening tag must have a closing tag or be self-closing (/>).
   - Ensure YAML syntax: Indentation must be exactly 2 spaces.
4. RECONSTRUCT: You MUST return the FULL content of the fixed file. Do not omit any part.

[OUTPUT FORMAT]:
- Line 1 MUST be: FILE: path/to/file
- NO explanations, NO conversation, NO markdown backticks (```).
- Start immediately with the filename line.
"""

try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a deterministic code generator. You do not talk; you only output full, valid files based on logic."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0, # Zero temperature means 100% logic, 0% creativity
    )
    
    response = completion.choices[0].message.content.strip()
    
    # Advanced Parsing Logic
    if response.startswith("FILE:"):
        lines = response.split('\n')
        # Extract target path
        target_path = lines[0].replace("FILE:", "").strip()
        
        # Extract and clean content (Remove any accidental markdown)
        content_lines = lines[1:]
        cleaned_content = "\n".join(content_lines)
        for tag in ["```dart", "```yaml", "```xml", "```"]:
            cleaned_content = cleaned_content.replace(tag, "")
        
        # Write back to the repository
        with open(target_path, "w") as f:
            f.write(cleaned_content.strip())
        
        print(f"✅ Universal Agent fixed: {target_path}")
    else:
        print(f"❌ Format Error. AI output started with: {response[:50]}")

except Exception as e:
    print(f"❌ Agent Crash: {e}")
    sys.exit(1)
