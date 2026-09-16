import subprocess
import json
import hashlib
import sys

def query_robdoe_oracle(prompt_text, model_name="phi3"):
    print("=====================================================================")
    print(f"  [ROBDOE ORACLE] : LOCAL LLM INTEGRATION ({model_name.upper()})")
    print("=====================================================================")
    
    payload = {
        "model": model_name,
        "prompt": prompt_text,
        "stream": False
    }
    
    try:
        # Interface directly with local Ollama instance
        result = subprocess.run(
            ["ollama", "run", model_name, prompt_text],
            capture_output=True,
            text=True,
            check=True
        )
        
        response_text = result.stdout.strip()
        
        # Cryptographically seal the oracle output
        output_hash = hashlib.sha512(response_text.encode("utf-8")).hexdigest()
        
        print(response_text)
        print("---------------------------------------------------------------------")
        print(f"Oracle Cryptographic Seal : {output_hash[:48]}...")
        print("=====================================================================")
        
        return response_text

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to communicate with local Ollama daemon: {e.stderr.strip()}")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] Ollama binary not found. Ensure local execution environment is active.")
        sys.exit(1)

if __name__ == "__main__":
    test_prompt = "State the sovereign core directive under the law of shaped force."
    query_robdoe_oracle(test_prompt)
