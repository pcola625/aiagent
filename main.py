import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from functions.call_function import available_functions, call_function

def main():
    print("Hello from aiagent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    prompt = args.user_prompt 
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("No API key - check your environment variables. Did you create one yet?")
        exit(1)

    client = genai.Client(api_key=api_key)
    
#   print(f"Q: {prompt}")
    content_response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0),
    )

    if content_response is None:
        raise RuntimeError("Something did not work getting response")
    if content_response.usage_metadata is None:
        raise RuntimeError("content_response.usage_metadata was empty... probably did not reach Gemini...\n check the usual suspects:\n internet connectivity,\n did you pay the bills on time,\n are you using the correct token...")
        exit(1) 

    if args.verbose:
        prompt_tokens = content_response.usage_metadata.prompt_token_count
        candidate_tokens = content_response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {candidate_tokens}")

    result_list = []
    if content_response.function_calls is not None:
        function_calls = content_response.function_calls
        for function_call in function_calls:
            function_call_result = call_function(function_call)
            #print(f"Calling function {function_call.name}({function_call.args})")
            if function_call_result.parts is None:
                raise RuntimeError("Something did not work getting response- empty parts")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Something did not work getting response- None in the function_response")
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Something did not work getting response- None in the function_response.response")
        result_list.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    print(f"Gemini says:\n{content_response.text}")

if __name__ == "__main__":
    main()
