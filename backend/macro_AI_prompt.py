import openai
import os
import csv
import glob
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_entire_csv_folder(folder_path):
    """
    Reads all CSV files in `folder_path` in their entirety
    and returns a combined text summary of *all* contents.
    
    WARNING: This can become *very large* if the CSV files are big,
    potentially leading to prompt size issues.
    """
    summary_lines = []
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    for csv_file in csv_files:
        summary_lines.append(f"--- File: {os.path.basename(csv_file)} ---")
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header:
                    summary_lines.append(f"Header: {header}")
                row_index = 0
                for row in reader:
                    row_index += 1
                    summary_lines.append(f"Row {row_index}: {row}")
        except Exception as e:
            summary_lines.append(f"Error reading {csv_file}: {str(e)}")

    return "\n".join(summary_lines)


def generate_macro_outlook(regulatory_text, macro_news_text):
    """
    Creates a prompt that includes the CSV data at the top, then the main instructions.
    """
    combined_csv_summary = (
        "Recent Regulatory Data (excerpted from CSVs):\n"
        f"{regulatory_text}\n\n"
        "Recent Macro/Energy News (excerpted from CSVs):\n"
        f"{macro_news_text}\n\n"
    )

    instructions = (
        "Use the csv summary I gave you with current news to put an emphasis on relavant current events in the energy sector and talk about quantitiative information"
        "Also use your information on current events to add to this data and give a very current, up to date overview of what is going on with clean and nuclear energy"
        "Be very professional and financial"
        "But emphasis on key takeaways and economic indicators moving foward"
    )

    prompt = combined_csv_summary + instructions

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    outlook = response.choices[0].message["content"]
    return outlook


def main():
    # 1) Read in CSV data for regulatory
    regulatory_text = read_entire_csv_folder("./regulatory_data")

    # 2) If you have a separate folder for macro-outlook news, read that too
    macro_news_text = read_entire_csv_folder("./macro_outlook_news")

    # 3) Generate the macro outlook report
    outlook_report = generate_macro_outlook(regulatory_text, macro_news_text)

    print("Macro Outlook Report:")
    print(outlook_report)

    output_filename = "./data/ai_reports/macro_outlook_report.txt"
    os.makedirs("./data/ai_reports", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(outlook_report)

    print(f"\n✅ Macro outlook report saved to {output_filename}")


if __name__ == "__main__":
    main()
