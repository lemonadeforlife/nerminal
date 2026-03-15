import json
import re
from llama_cpp import Llama

MODEL_PATH = "model/mosaicml-mpt-7b-instruct-Q4_K_M.gguf"

PROMPT_COMMAND = """<|im_start|>system
You are a JSON-only command parser. Your entire response must be one valid JSON object and nothing else.
No explanation. No preamble. No extra text. Just the JSON object.

Supported actions and their required fields:
- {{"action": "open_browser", "browser": "<firefox|chrome|brave|edge>"}}
- {{"action": "search_web", "query": "<search terms>"}}
- {{"action": "tell_time"}}
- {{"action": "unknown"}}

Rules:
- If the user wants to open a browser (e.g. "open firefox", "launch chrome", "start brave"), output open_browser.
- If the user says "browser" generically without naming one, default to "firefox".
- If the user names something that is NOT in [firefox, chrome, brave, edge], output {{"action": "unknown"}}.
- If the user wants to search something, output search_web with a clean query.
- If the user asks for the time, output tell_time.
- For everything else, output unknown.
<|im_end|>
<|im_start|>user
{user_request}
<|im_end|>
<|im_start|>assistant
{{"""

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

BROWSERS = ["firefox", "chrome", "brave", "edge"]
VALID_ACTIONS = {"open_browser", "search_web", "tell_time", "unknown"}


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
        """Extract and parse the first JSON object found in text."""
        if not text:
            return None
        # The prompt ends with `{` so the model only needs to complete it;
        # prepend the opening brace we already sent before trying to parse.
        candidates = [text, "{" + text]
        for candidate in candidates:
            match = re.search(r"\{[^{}]*\}", candidate, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    continue
        return None

    def _fallback_route(self, user_request: str) -> dict:
        """Rule-based fallback when the LLM doesn't return valid JSON."""
        lower = user_request.lower()

        # Browser detection — check this BEFORE generic "open/launch/run"
        for b in BROWSERS:
            if b in lower:
                return {"action": "open_browser", "browser": b}

        if "browser" in lower:
            return {"action": "open_browser", "browser": "firefox"}

        # Web search
        if any(word in lower for word in ["search", "google", "look up", "find"]):
            # Strip filler words to get a cleaner query
            query = re.sub(
                r"\b(search|google|look up|find|for|me)\b", "", lower
            ).strip()
            return {"action": "search_web", "query": query or user_request}

        # Tell time
        if "time" in lower:
            return {"action": "tell_time"}

        return {"action": "unknown"}

    def route_command(self, user_request: str) -> dict:
        prompt = PROMPT_COMMAND.format(user_request=user_request)
        try:
            output = self.llm(
                prompt,
                max_tokens=64,
                temperature=0.0,
                stop=["<|im_end|>", "<|im_start|>"],
                echo=False,
            )
            response_text = output["choices"][0]["text"].strip()
            print(f"[LLM ROUTE] Raw: '{response_text}'")

            result = self.extract_json(response_text)
            if result and result.get("action") in VALID_ACTIONS:
                if result.get("action") == "open_browser":
                    if result.get("browser") not in BROWSERS:
                        print(
                            f"[LLM ROUTE] Unrecognized browser '{result.get('browser')}' — routing to unknown"
                        )
                        return {"action": "unknown"}
                print(f"[LLM ROUTE] Parsed: {result}")
                return result

            print("[LLM ROUTE] JSON parse failed — using fallback")
            fallback = self._fallback_route(user_request)
            print(f"[LLM ROUTE] Fallback: {fallback}")
            return fallback

        except Exception as e:
            print(f"LLM Route Error: {e}")
            return {"action": "unknown"}

    def chat(self, user_input: str) -> str:
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
