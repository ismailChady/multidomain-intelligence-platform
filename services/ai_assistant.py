from typing import Dict, List
from google import genai


class AIAssistant:
    """
    Service class that wraps the Google Gemini API for chat responses.

    This is a service (not an entity): it coordinates AI calls and
    keeps minimal state (conversation history + system prompt).
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        system_prompt: str = "You are a helpful assistant.",
    ):
        self._system_prompt = system_prompt
        self._history: list[dict[str, str]] = []

        # Initialize Gemini client
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt used to guide the assistant."""
        self._system_prompt = prompt

    def send_message(self, user_message: str) -> str:
        """
        Send a user message to the Gemini model and return the reply.

        The method also stores the interaction in an internal history list.
        """
        self._history.append({"role": "user", "content": user_message})

        prompt = f"{self._system_prompt}\n\nUser: {user_message}"

        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
            )
            reply = response.text
        except Exception as e:
            reply = f"[AI error: {e}]"

        self._history.append({"role": "assistant", "content": reply})
        return reply

    def clear_history(self) -> None:
        """Clear the in-memory conversation history."""
        self._history.clear()