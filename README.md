# 🗓️ OpenAI-Powered Google Calendar Meeting Scheduler

This project is an AI-powered meeting scheduling assistant that integrates OpenAI's speech-to-text (using Whisper) with the Google Calendar API. Users can provide meeting details via text or voice commands, and the assistant will automatically schedule the event in Google Calendar.

## Demo

Check out the demo of the meeting scheduler in action:

![Demo Video](demo.gif)


## 📢 Features

- **Speech-to-Text**: Record a voice command using a file-based recorder and convert it to text using OpenAI's Whisper API.
- **Text-Based Commands**: Alternatively, enter your meeting command manually.
- **Google Calendar Integration**: Automatically schedule meetings on Google Calendar.
- **Relative Date Parsing**: Convert natural language dates like "tomorrow at 2pm" into exact timestamps.
- **Default Duration**: If no end time is provided, the meeting defaults to a 1-hour duration.
- **Interactive Streamlit UI**: A simple web interface to input commands and view results.
- **Secure API Key Handling**: Uses environment variables to manage sensitive credentials.

## 🚀 Tech Stack

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/) (Whisper for Speech-to-Text)
- [Google Calendar API](https://developers.google.com/calendar)
- [audio_recorder_streamlit](https://github.com/jeffheaton/Audio-Recorder-Streamlit) (for voice input)
- [dateparser](https://dateparser.readthedocs.io/)
- [wave](https://docs.python.org/3/library/wave.html) (for processing audio)
- [gTTS](https://pypi.org/project/gTTS/)

## 🔑 Prerequisites

Before running the application, you will need:
- A **Google Cloud Project** with the Google Calendar API enabled.
- A **Google OAuth 2.0 Credentials JSON file** (named `credentials.json`) placed in the project root.
- A valid **OpenAI API key**.
- Python (3.8+) and pip installed.

## 🛠️ Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/google-calendar-openai-assistant.git
``` 
```sh
cd google-calendar-openai-assistant
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set Up Google Calendar API

#### a) Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Create Project**, provide a name, and click **Create**.

#### b) Enable the Google Calendar API

1. Navigate to **APIs & Services > Library**.
2. Search for **Google Calendar API** and click **Enable**.

#### c) Generate OAuth Credentials

1. In **APIs & Services > Credentials**, click **Create Credentials > OAuth client ID**.
2. Choose **Desktop App** as the application type.
3. Click **Create**.
4. Download the JSON file and save it as `credentials.json` in the project root.

#### d) Authenticate with Google

- The first time you run the app, a browser window will open for Google authentication. Follow the prompts to allow access. A `token.json` file will be created for subsequent requests.

### 4. Set Up OpenAI API Key

1. Log in to [OpenAI](https://platform.openai.com/).
2. Navigate to **API Keys** and create a new secret key.
3. Copy the API key and set it in your environment variables:
   - **Windows (PowerShell):**  
     ```sh
     $env:OPENAI_API_KEY="your-api-key-here"
     ```
   - **Mac/Linux (Terminal):**  
     ```sh
     export OPENAI_API_KEY="your-api-key-here"
     ```

### 5. Running the Application

Launch the Streamlit app with:

```sh
streamlit run app.py
```

This will open the web interface in your browser.

## 📋 How to Use

1. **Enter a Meeting Command**  
   Type your meeting command (e.g., "Schedule a meeting with Bob tomorrow at 2pm") into the text box.

2. **Or Record Your Voice Command**  
   Click the record button to capture your voice command. The audio is transcribed using OpenAI's Whisper API, and the resulting text will pre-populate the input field.

3. **Schedule the Meeting**  
   Click **Schedule Meeting**. The app will:
   - Process your command via OpenAI.
   - Parse relative dates into exact timestamps.
   - Apply a default duration of 1 hour if no end time is provided.
   - Schedule the event in Google Calendar.
   - Display a link to view the scheduled event.

## 📂 Project Structure
│── app.py                  # Main Streamlit application
│── utils.py                # Utility functions (speech_to_text, text_to_speech, etc.)
│── google_calendar.py      # Google Calendar API integration functions
│── openai_assistant.py     # Functions to process natural language commands via OpenAI
│── requirements.txt        # Project dependencies
│── credentials.json        # Google API credentials (DO NOT commit this file)
│── token.json              # Google OAuth token (auto-generated on first run)
│── README.md               # This file


## 🔐 Security & Best Practices

- **DO NOT** commit sensitive files (like `credentials.json`, `token.json`, or your `.env` file) to public repositories.
- Use a `.gitignore` file to exclude these files:
```sh
credentials.json
token.json
.env
```

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: / git checkout -b feature-name
3. Commit your changes: / git commit -m "Add new feature"
4. Push the branch: / git push origin feature-name
5. Open a pull request.

## 📜 License

This project is licensed under the MIT License.

## 📞 Support

If you have questions or issues, please open an issue on GitHub or contact [riachoudhari9@gmail.com](mailto:riachoudhari9@gmail.com).

---

⭐ If you like this project, please give it a star on GitHub!

