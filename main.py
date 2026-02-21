import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Candidate

from prompt import system_prompt
from functions.call_function import available_functions, call_function
from create_content import create_content

def main():
    print("Hello from aiagent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    prompt = args.user_prompt

    if args.verbose:
        print(f"User prompt: {prompt}")
    
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    num_iters = os.environ.get("GEMINI_NUM_ITERS")

    if num_iters is None:
        num_iters = 5
    if api_key is None:
        raise RuntimeError("No API key - check your environment variables. Did you create one yet?")
        exit(1)

    client = genai.Client(api_key=api_key)

   # Begins the agent looop here.. I think.
    for _ in range(int(num_iters)):
        try:
            final_response = create_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in create_content: {e}")


    print(f"Maximum iterations ({num_iters}) reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
