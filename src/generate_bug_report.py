import os
from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from vectorizer import find_closest_samples

# Configuration (Load environment variables)
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

def process_user_input(user_steps, expected_results):

    samples = find_closest_samples(user_steps, expected_results)

    # Send custom prompt if similar issue is found
    if len(samples) > 0:

        prompt = """You are a software QA tester. The user reported encountering a bug.
Steps to reproduce:
{user_steps}
Expected Results:
{expected_results}.

Taking reference of the examples below, can you generate a bug report describting the issue, steps to reproduce and expected results?
Use simple and short sentences. Use similar format and punctuations. Wrap your result in code snippet.

Below are some examples of bug report:
""".format(user_steps=user_steps, expected_results=expected_results)

        for sample in samples:
            prompt += f"{sample}"

        # Generate custom bug report using LLM
        response = llm.invoke(prompt)
        
        report = f"\n*Cool Tip💡 If the result is not accurate, try to refine your input with more information.*\n"
        report += response.content
        report += f"\nDon’t forget to include your test environment details, as well as any screenshots or screen recordings, when submitting your issue.🚀\n"
        report += """
Below is a template for test environment information:
```
## Environment:
- Environment: UAT
- Platform: 
- Build version: 
- Browser: 
- Device (OS version): 
- Test account: 
```
  """
        report += f"\nHappy Testing!🌟"
        return report
    else:
        # Send a general prompt if no similar issue is found
        prompt = f"The user reported encountering a bug. Steps to reproduce:\n{user_steps}\nExpected Results:\n{expected_results}\n"
        prompt += "Can you generate a detailed bug report describing the issue and potential solutions?"

         # Generate general bug report using LLM
        response = llm.invoke(prompt)
        
        report = f"\n*Cool Tip💡 If the result is not accurate, try to refine your input with more information.*\n\n"
        report += response.content

        return report
