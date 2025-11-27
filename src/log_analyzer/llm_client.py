import os
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY and OpenAI else None

def analyze_with_llm(summary):
    """
    If OPENAI_API_KEY is set, calls OpenAI API to enrich logs.
    Otherwise, uses a placeholder recommended_action.
    """
    for entry in summary.get("log_summary", []):
        if client:
            try:
                prompt = f"Analyze the following log entry and add a recommended action in one sentence:\n{entry['message']}"
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                )
                # Safely extract content and avoid calling strip() on None
                content = None
                try:
                    # Prefer attribute access for SDK-like objects
                    content = getattr(response.choices[0].message, "content", None)
                except Exception:
                    # Fallback for dict-like responses
                    try:
                        choice = response.choices[0]
                        if isinstance(choice, dict):
                            content = choice.get("message", {}).get("content")
                    except Exception:
                        content = None
                entry["recommended_action"] = content.strip() if content else "LLM returned no content"
            except Exception as e:
                entry["recommended_action"] = f"LLM error: {e}"
        else:
            entry["recommended_action"] = "No API key: placeholder action"
    return summary