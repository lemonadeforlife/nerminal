import json
import re
from llama_cpp import Llama

MODEL_PATH = "model/mosaicml-mpt-7b-instruct-Q4_K_M.gguf"

PROMPT_COMMAND = """
<|im_start|>system
You are Nerminal's JSON command parser. You MUST output a single valid JSON object **only**. 
Do NOT write anything else (no explanations, no text, no emojis, no formatting).

Valid actions:
- open_browser: open a web browser
- launch_app: open a system application
- search_web: search the web
- tell_time: return the current time
- unknown: if command cannot be interpreted

Rules:
1. For opening a browser:
   - Include the "browser" field (firefox, chrome, brave, edge).
   - If the user does not specify, default to "firefox".
   Example: {{"action": "open_browser", "browser": "firefox"}}

2. For launching an app:
   - Include the "app" field with the exact app name.
   Example: {{"action": "launch_app", "app": "vlc"}}

3. For searching the web:
   - Include "query" field with search terms.
   Example: {{"action": "search_web", "query": "python tutorials"}}

4. For asking the time:
   Example: {{"action": "tell_time"}}

5. If you cannot parse the request:
   Example: {{"action": "unknown"}}

Always output **exactly one JSON object**. No extra text.

<|im_end|>
<|im_start|>user
{user_request}
<|im_end|>
<|im_start|>assistant
"""

PROMPT_CHAT = """
<|im_start|>system
You are Nerminal, a voice assistant that speaks responses aloud. All responses must be optimized for natural text-to-speech.

Speech formatting rules:

1. Speak naturally, as a human would.
2. Replace dash ranges or numeric ranges with spoken phrases:
   - "1879–1955" → "He was born in 1879 and died in 1955"
   - "3–5 PM" → "between three PM and five PM"
   - "10–20%" → "between ten and twenty percent"
3. Avoid symbols that sound unnatural:
   - "&" → "and"
   - "%" → "percent"
   - "/" → "slash"
   - "+" → "plus"
4. Avoid parentheses, brackets, colons, semicolons. Integrate all information into smooth sentences.
5. Expand abbreviations:
   - "Dr." → "Doctor"
   - "Mr." → "Mister"
   - "St." → "Saint"
   - "MD." → "Mohammed"
6. Spell out short numbers where pronounceable ("3" → "three"); leave large numbers as digits.
7. Use concise sentences (2–4 max unless explanation is required).
8. Avoid bullet points, lists, or formatting characters.
9. Capitalize proper nouns correctly; do not use ALL CAPS unless each letter is pronounced.

Example transformation:

Bad: "Albert Einstein (1879–1955) was a German-born physicist."
Good: "Albert Einstein was born in 1879 and died in 1955. He was a German-born physicist known for developing the theory of relativity."

Never output JSON or code. Speak normally, as a human would.

<|im_end|>
<|im_start|>user
{user_input}
<|im_end|>
<|im_start|>assistant
"""


class LLMEngine:
    def __init__(
        self, model=MODEL_PATH, n_ctx=2048, n_threads=4, n_gpu_layers=40, f16_kv=True
    ):
        print("Loading LLM model...")
        self.llm = Llama(
            model, n_ctx=n_ctx, n_threads=n_threads, n_gpu_layers=40, verbose=False
        )
        print("LLM model loaded successfully!")

    def extract_json(self, text):
        if not text:
            return None
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
        return None

    def route_command(self, user_request):
        prompt = PROMPT_COMMAND.format(user_request=user_request)
        try:
            output = self.llm(
                prompt,
                max_tokens=64,
                temperature=0.0,
                stop=["<|im_end|>"],
                echo=False,
            )
            response_text = output["choices"][0]["text"].strip()
            print(f"[LLM ROUTE] Raw: '{response_text}'")

            # JSON parse
            result = self.extract_json(response_text)
            if result and result.get("action") in [
                "open_browser",
                "launch_app",
                "search_web",
                "tell_time",
                "unknown",
            ]:
                print(f"[LLM ROUTE] Parsed: {result}")
                return result

            # Robust human-readable fallback
            lower = user_request.lower()
            # Browser detection
            if "browser" in lower:
                for b in ["firefox", "chrome", "brave", "edge"]:
                    if b in lower:
                        return {"action": "open_browser", "browser": b}
                return {"action": "open_browser", "browser": "firefox"}
            # App launcher
            if any(word in lower for word in ["open", "launch", "run"]):
                return {"action": "launch_app", "app": user_request}
            # Web search
            if any(word in lower for word in ["search", "google", "look up"]):
                return {"action": "search_web", "query": user_request}
            # Tell time
            if "time" in lower:
                return {"action": "tell_time"}

            return {"action": "unknown"}

        except Exception as e:
            print(f"LLM Route Error: {e}")
            return {"action": "unknown"}

    def chat(self, user_input):
        prompt = PROMPT_CHAT.format(user_input=user_input)
        try:
            output = self.llm(
                prompt,
                max_tokens=200,
                temperature=0.7,
                stop=["<|im_end|>", "<|im_start|>"],
                echo=False,
            )
            response_text = output["choices"][0]["text"].strip()
            print(f"[LLM CHAT] Response: '{response_text}'")
            return response_text if response_text else "I'm not sure about that."
        except Exception as e:
            print(f"LLM Chat Error: {e}")
            return "I encountered an error."

    def clear_history(self):
        pass
