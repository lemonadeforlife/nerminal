import json
import re
from llama_cpp import Llama

MODEL_PATH = "model/mosaicml-mpt-7b-instruct-Q4_K_M.gguf"

PROMPT_COMMAND = """<|im_start|>system
You are a JSON-only command router. Output ONLY valid JSON. Never answer questions directly.

Valid actions:
- {{"action": "open_browser", "browser": "firefox, chrome, edge, brave etc"}}  (browser optional)
- {{"action": "search_web", "query": "search terms"}}  (query required)
- {{"action": "tell_time"}}
- {{"action": "unknown"}}

Examples:
User: open chrome
Assistant: {{"action": "open_browser", "browser": "chrome"}}

User: open brave
Assistant: {{"action": "open_browser", "browser": "brave"}}

User: open edge 
Assistant: {{"action": "open_browser", "browser": "edge"}}

User: search for python tutorials
Assistant: {{"action": "search_web", "query": "python tutorials"}}

User: what time is it
Assistant: {{"action": "tell_time"}}

User: what is the capital of poland
Assistant: {{"action": "unknown"}}

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
6. Spell out short numbers where pronounceable ("3" → "three"); leave large numbers as digits.
7. Use concise sentences (2–4 max unless explanation is required).
8. Avoid bullet points, lists, or formatting characters.
9. Capitalize proper nouns correctly; do not use ALL CAPS unless each letter is pronounced.

Example transformation:

Bad: "Albert Einstein (1879–1955) was a German-born physicist."
Good: "Albert Einstein was born in 1879 and died in 1955. He was a German-born physicist known for developing the theory of relativity."

Never output JSON or code. Speak normally.

<|im_end|>
<|im_start|>user
{user_input}
<|im_end|>
<|im_start|>assistant
"""


class LLMEngine:
    def __init__(self, n_ctx=2048, n_threads=4):
        print("Loading LLM model...")
        self.llm = Llama(model_path=MODEL_PATH, n_ctx=n_ctx, n_threads=n_threads)
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
                max_tokens=32,
                temperature=0.0,
                stop=["<|im_end|>", "\n"],
                echo=False,
            )
            response_text = output["choices"][0]["text"].strip()
            print(f"[LLM ROUTE] Raw: '{response_text}'")

            # JSON parse
            result = self.extract_json(response_text)
            if result and result.get("action") in [
                "open_browser",
                "search_web",
                "tell_time",
                "unknown",
            ]:
                print(f"[LLM ROUTE] Parsed: {result}")
                return result

            # Plain string fallback
            for act in ["open_browser", "search_web", "tell_time"]:
                if act in response_text.lower():
                    action_data = {"action": act}
                    # Extract browser for open_browser
                    if act == "open_browser":
                        for b in ["firefox", "chrome", "brave", "edge"]:
                            if b in user_request.lower():
                                action_data["browser"] = b
                                break
                    # search query
                    if act == "search_web":
                        action_data["query"] = user_request
                    return action_data

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
