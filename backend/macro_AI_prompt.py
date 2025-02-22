import openai
import os
from dotenv import load_dotenv


load_dotenv()

def generate_macro_outlook():

    # Define the prompt for the macro outlook
    prompt = (
        "Write a comprehensive macro outlook report for the energy sector. "
        "Include discussions of renewable energy, nuclear, solar, wind, hydropower, and geothermal trends, "
        "as well as recent regulatory changes and government policies. "
        "Highlight key market trends, international developments, and potential future challenges and opportunities. Talk about specific regulatory changes and policies that have been passed and how they have effected the sector as a whole"
        "Conclude with a summary and key takeaways."
    )

    # Call the OpenAI API (using the ChatCompletion endpoint)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-3.5-turbo if preferred
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    # Extract the generated content
    outlook = response.choices[0].message["content"]
    return outlook

def main():
    # Set your OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Generate the macro outlook report
    outlook_report = generate_macro_outlook()
    
    # Print the report to the console
    print("Macro Outlook Report:")
    print(outlook_report)
    
    # Save the report to a text file
    output_filename = "./data/macro_outlook_report.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(outlook_report)
    
    print(f"Saved macro outlook report to {output_filename}")

if __name__ == "__main__":
    main()
