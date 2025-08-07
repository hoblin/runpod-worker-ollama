import json
import os
import aiohttp

from dotenv import load_dotenv

class OllamaEngine:
    def __init__(self):
        load_dotenv()
        print("OllamaEngine initialized")

    async def generate(self, job_input):
        print("Generating response for job_input:", job_input)

        # Handle models request separately
        if job_input.get('route') == "/v1/models":
            async for response in self._handle_models():
                yield response
        else:
            # Use route from job_input for all other requests
            async for response in self._handle_request(job_input):
                yield response

    async def _handle_models(self):
        """Get available models from Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:11434/api/tags') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Return everything from Ollama
                        yield data
                    else:
                        yield {"error": f"HTTP {resp.status}"}
        except Exception as e:
            yield {"error": str(e)}

    async def _handle_request(self, job_input):
        """Handle requests using Ollama's native API"""
        try:
            # Get route and the actual input data
            route = job_input.get('route', '/api/chat')

            # The actual data to send to Ollama is in the nested "input" field
            ollama_body = job_input.get('input', {})

            print(f"Ollama request to {route}: {ollama_body}")

            # Map route to Ollama endpoint
            ollama_endpoint = route.replace('/v1/chat/completions', '/api/chat').replace('/v1/completions', '/api/generate')

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'http://localhost:11434{ollama_endpoint}',
                    json=ollama_body,
                    headers={'Content-Type': 'application/json'}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Return everything from Ollama
                        yield data
                    else:
                        error_text = await resp.text()
                        yield {"error": f"HTTP {resp.status}: {error_text}"}
        except Exception as e:
            yield {"error": str(e)}
