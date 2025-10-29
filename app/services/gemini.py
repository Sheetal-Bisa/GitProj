import os
from typing import List, Dict, Any

try:
	import google.generativeai as genai
	_HAS_GEMINI = True
except Exception:
	_HAS_GEMINI = False


# Global singleton instance
_client_instance = None


def get_client() -> "GeminiClient":
	"""Get or create the global Gemini client instance"""
	global _client_instance
	if _client_instance is None:
		_client_instance = GeminiClient()
	return _client_instance


class GeminiClient:
	def __init__(self, model: str = "gemini-1.5-flash") -> None:
		self.model_name = model
		self.api_key = os.getenv("GEMINI_API_KEY")
		if _HAS_GEMINI and self.api_key:
			try:
				genai.configure(api_key=self.api_key)
				self.model = genai.GenerativeModel(model)
				self._configured = True
				print("[GEMINI] Successfully configured with API key")
			except Exception as e:
				print(f"[GEMINI] Configuration error: {e}")
				self.model = None
				self._configured = False
		else:
			self.model = None
			self._configured = False
			if not self.api_key:
				print("[GEMINI] No API key found in environment")

	async def chat(self, messages: List[Dict[str, str]]) -> str:
		"""Handle chat with conversation history. Messages format: [{role: 'user'|'assistant', content: '...'}]"""
		if self.model is None or not self._configured:
			# Fallback response when Gemini is not available
			last_user_msg = next((m for m in reversed(messages) if m.get("role") == "user"), {"content": ""})
			content = last_user_msg.get("content", "")
			
			# Simple rule-based responses as fallback
			if any(word in content.lower() for word in ["feeling", "feel", "mood", "sad", "happy", "anxious"]):
				return "I understand you're sharing your feelings. Remember, it's okay to feel what you're feeling. Would you like to talk more about it?"
			elif any(word in content.lower() for word in ["help", "support", "need"]):
				return "I'm here to listen and support you. What's on your mind?"
			else:
				return f"I hear you: '{content}'. I'm here to listen and support you. How are you feeling today?"
			
		try:
			# Convert messages to Gemini format
			# For single-turn or simple prompt, use generate_content
			user_msg = next((m for m in reversed(messages) if m.get("role") == "user"), None)
			if user_msg:
				prompt = user_msg.get("content", "")
				
				# Add system context for mood/supportive chatbot
				context = "You are a supportive, empathetic AI assistant for a mood tracking app called MoodMate. Be warm, understanding, and helpful. Keep responses concise but caring."
				
				# Use generate_content for simple requests
				resp = self.model.generate_content(f"{context}\n\nUser: {prompt}")
				result = getattr(resp, "text", "") or str(resp)
				return result if result else "I'm here to listen and support you."
			
			return "I'm here to listen. How can I help you today?"
			
		except Exception as e:
			error_msg = str(e)
			print(f"[GEMINI ERROR] {error_msg}")
			return f"I'm having trouble connecting right now. I'm here to support you though - how are you feeling today?"

	async def generate_content(self, prompt: str, context: str = "") -> str:
		"""Generate content from a single prompt with optional context"""
		if self.model is None or not self._configured:
			return f"[Fallback] {prompt}"
			
		try:
			full_prompt = f"{context}\n\n{prompt}" if context else prompt
			resp = self.model.generate_content(full_prompt)
			return getattr(resp, "text", "") or str(resp)
		except Exception as e:
			return f"Error generating content: {e}"
