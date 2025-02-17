# openai_assistant.py
import openai
import json
from datetime import datetime, timedelta
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def process_command(command: str) -> dict:
    """
    Processes a natural language command and extracts meeting details.

    Expected JSON output format:
    {
      "summary": "Meeting title",
      "start_time": "YYYY-MM-DDTHH:MM:SS",
      "end_time": "YYYY-MM-DDTHH:MM:SS",
      "description": "Meeting description or agenda",
      "attendees": ["email1@example.com", "email2@example.com"]
    }

    If any detail is missing, values should be empty strings (or an empty list for "attendees").
    The times should be expressed in IST.
    """
    # Dynamically compute today's and tomorrow's date
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    prompt = f"""
Given today's date is {today}.
Extract meeting details from the following command:
"{command}"

Return only valid JSON with exactly the following keys:
- "summary": The meeting title.
- "start_time": The start time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) in IST.
- "end_time": The end time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) in IST.
- "description": The meeting description or agenda.
- "attendees": A list of email addresses.

If a detail is not mentioned, set its value to an empty string (or an empty list for "attendees").
If the command includes relative dates (like "tomorrow"), calculate the correct absolute date using today's date ({today}).
Output only the JSON object and nothing else.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured meeting details for scheduling events in Google Calendar."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
        )
        answer = response['choices'][0]['message']['content'].strip()
        print("DEBUG - Raw answer from GPT:", answer)
        
        # Strip out markdown code block formatting if present
        if answer.startswith("```"):
            # Remove the first and last lines which are the code fence markers
            lines = answer.splitlines()
            # Remove the first line (```json or ```), and last line (```)
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            answer = "\n".join(lines).strip()
        
        details = json.loads(answer)
    except Exception as e:
        print("DEBUG - Error parsing JSON:", e)
        details = {}
    return details


