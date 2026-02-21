from google import genai
from google.genai import types
from google.genai.types import Candidate

from prompt import system_prompt
from functions.call_function import available_functions, call_function

def create_content(client, messages, verbose):
    content_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,
                                           temperature=0),
    )
    if not content_response:
        raise RuntimeError("Something did not work getting response")
    if not content_response.usage_metadata:
        raise RuntimeError(
            "content_response.usage_metadata was empty... probably did not reach Gemini...\n check the usual suspects:\n internet connectivity,\n did you pay the bills on time,\n are you using the correct token...\n")
        exit(1)
    if verbose:
        prompt_tokens = content_response.usage_metadata.prompt_token_count
        candidate_tokens = content_response.usage_metadata.candidates_token_count
        print(f"\nPrompt tokens: {prompt_tokens}\nResponse tokens: {candidate_tokens}")
    if content_response.candidates:
        for candidates in content_response.candidates:
            messages.append(candidates.content)
    if not content_response.function_calls:
        return content_response.text

    function_responses = []
    for function_call in content_response.function_calls:
        function_call_result = call_function(function_call)
        if function_call_result.parts is None:
            raise RuntimeError("Something did not work getting response- empty parts")
        if function_call_result.parts[0].function_response is None:
            raise RuntimeError("Something did not work getting response- None in the function_response")
        if function_call_result.parts[0].function_response.response is None:
            raise RuntimeError("Something did not work getting response- None in the function_response.response")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    messages.append(types.Content(role="user", parts=function_responses))
