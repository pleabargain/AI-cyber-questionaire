# Cyber Security Knowledge Assessment System


# repo
https://github.com/pleabargain/AI-cyber-questionaire

#what
This system assesses personal cyber security knowledge through a questionnaire and provides AI-generated recommendations for improvement.

#how
I built this using cursor and cline. I used a variety of API calls to openrouter and anthropic. I chose Ollama for the report generation because it is cheap and cyber security is a big topic and everyone should know about it.

#why
I built this because I want to help people understand cyber security and how to protect themselves. I believe that everyone should know about cyber security and how to protect themselves. 

#where to use this
This can be used by anyone who wants to know about cyber security and how to protect themselves. Take a cyber security course to know more about it.

#caveats
This is a simple system and it is not perfect. It is a good starting point and it is a good way to understand cyber security. It is not a comprehensive system and it is not a good way to get a job in cyber security. It is a good way to understand cyber security and how to protect yourself.


## Features

- Interactive questionnaire covering key cyber security areas
- Colored console interface for better readability
- AI-powered analysis using Ollama
- Detailed reports in both JSON and Markdown formats
- Timestamped storage of answers and reports

## Requirements

- Python 3.x
- Ollama running locally
- Required Python packages (install using `pip install -r requirements.txt`):
  - colorama
  - requests

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Ollama is running at http://localhost:11434/

## Usage

1. Run the assessment:
   ```bash
   python main.py
   ```

2. Follow the prompts:
   - Enter your name
   - Answer each question honestly
   - Review your assessment report

3. Files generated:
   - Answers: `answers/{NAME}_cyber_security_assessment_{YYYY.MM.DD.SS}.json`
   - Report (JSON): `reports/cyber_sec_report_for_{NAME}_{YYYY.MM.DD.SS}.json`
   - Report (Markdown): `reports/cyber_sec_report_for_{NAME}_{YYYY.MM.DD.SS}.md`

## Question Categories

- Password Security
- Multi-Factor Authentication
- Network Security
- System Updates
- Data Backup
- Phishing Awareness
- Device Security
- Social Media
- Data Encryption

## Report Format

The assessment report includes:
- Overall assessment of security practices
- Specific areas needing improvement
- Actionable recommendations
- Summary of good practices
- Additional recommendations

## File Structure

```
.
├── main.py                 # Main application
├── questions.json          # Question database
├── requirements.txt        # Python dependencies
├── answers/               # Stored user responses
├── reports/               # Generated reports
└── README.md              # This file
```

## Notes

- All answers and reports are saved with timestamps
- Reports are generated in both JSON and Markdown formats
- Console output uses colors for better readability
- Full file paths are displayed after assessment completion
