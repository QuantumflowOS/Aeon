import os
import logging

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False


class CognitionEngine:
    """
    Handles reasoning over context and deciding how the agent should act.
    Falls back to rule-based reasoning if no LLM is available.
    """

    def __init__(self, model="gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None

        if _OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logging.info("CognitionEngine initialized with OpenAI backend")
        else:
            logging.warning("CognitionEngine running in fallback mode")

    # -------- PUBLIC ENTRY POINT --------
    def think(self, context):
        if self.client:
            return self._llm_think(context)
        return self._fallback_think(context)

    # -------- LLM PATH --------
    def _llm_think(self, context):
        prompt = self._build_prompt(context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are AEON, a conscious context reasoning engine."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            thought = response.choices[0].message.content
            logging.info("LLM cognition executed")
            return thought

        except Exception as e:
            logging.error(f"LLM failure, falling back: {e}")
            return self._fallback_think(context)

    # -------- FALLBACK PATH --------
    def _fallback_think(self, context):
        """
        Deterministic reasoning when no LLM is available.
        """
        emotion = context.emotion.lower()
        intent = context.intent.lower()

        if emotion in ["sad", "angry", "frustrated"]:
            return "User is emotionally distressed. Prioritize emotional support."
        if intent in ["work", "study", "focus"]:
            return "User intends productivity. Reduce distractions and structure tasks."
        if emotion in ["happy", "excited"]:
            return "User has positive energy. Encourage creativity or exploration."

        return "Neutral context detected. Maintain supportive baseline behavior."

    # -------- PROMPT --------
    def _build_prompt(self, context):
        return f"""
Context Snapshot:
- Emotion: {context.emotion}
- Intent: {context.intent}
- Environment: {context.environment}

Tasks:
1. Interpret the user's mental state
2. Decide the most helpful high-level response strategy
3. Explain reasoning briefly

Respond concisely.
"""
