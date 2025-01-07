import json
import sys
import os
import datetime
import requests
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

def load_questions():
    """Load questions from JSON file."""
    try:
        with open('questions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: questions.json file not found.{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON format in questions.json{Style.RESET_ALL}")
        sys.exit(1)

def get_formatted_timestamp():
    """Get timestamp in YYYY.MM.DD.SS format."""
    return datetime.datetime.now().strftime("%Y.%m.%d.%H%M")

def save_answers(responses, user_name):
    """Save responses to a timestamped file in the answers directory."""
    timestamp = get_formatted_timestamp()
    filename = f"{user_name}_cyber_security_assessment_{timestamp}.json"
    filepath = os.path.join('answers', filename)
    try:
        with open(filepath, 'w') as f:
            json.dump({
                "user_name": user_name,
                "timestamp": timestamp,
                "responses": responses
            }, f, indent=2)
        return os.path.abspath(filepath)
    except Exception as e:
        print(f"{Fore.RED}Error saving answers: {e}{Style.RESET_ALL}")
        sys.exit(1)

def save_report(report, user_name):
    """Save the generated report."""
    timestamp = get_formatted_timestamp()
    filename = f"cyber_sec_report_for_{user_name}_{timestamp}.json"
    filepath = os.path.join('reports', filename)
    try:
        with open(filepath, 'w') as f:
            json.dump({
                "user_name": user_name,
                "timestamp": timestamp,
                "report": report
            }, f, indent=2)
        return os.path.abspath(filepath)
    except Exception as e:
        print(f"{Fore.RED}Error saving report: {e}{Style.RESET_ALL}")
        sys.exit(1)

def save_markdown_report(report, user_name, timestamp):
    """Save the report in markdown format."""
    filename = f"cyber_sec_report_for_{user_name}_{timestamp}.md"
    filepath = os.path.join('reports', filename)
    
    try:
        with open(filepath, 'w') as f:
            f.write(f"# Cyber Security Assessment Report\n")
            f.write(f"**User:** {user_name}  \n")
            f.write(f"**Date:** {timestamp}\n\n")
            
            # Write assessment
            f.write("## Assessment\n\n")
            f.write(report['assessment']['overall'])
            f.write("\n\n")
            
            # Write recommendations if they exist
            if any(report['recommendations'].values()):
                f.write("## Recommendations\n\n")
                
                if report['recommendations']['critical']:
                    f.write("### Critical\n")
                    for rec in report['recommendations']['critical']:
                        f.write(f"- {rec}\n")
                    f.write("\n")
                
                if report['recommendations']['important']:
                    f.write("### Important\n")
                    for rec in report['recommendations']['important']:
                        f.write(f"- {rec}\n")
                    f.write("\n")
                
                if report['recommendations']['good_practices_to_continue']:
                    f.write("### Good Practices to Continue\n")
                    for practice in report['recommendations']['good_practices_to_continue']:
                        f.write(f"- {practice}\n")
                    f.write("\n")
            
            if report['conclusion']:
                f.write("## Conclusion\n\n")
                f.write(report['conclusion'])
                f.write("\n")
        
        return os.path.abspath(filepath)
    except Exception as e:
        print(f"{Fore.RED}Error saving markdown report: {e}{Style.RESET_ALL}")
        sys.exit(1)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_name():
    """Get the user's name."""
    while True:
        name = input(f"{Fore.CYAN}Please enter your name: {Style.RESET_ALL}").strip()
        if name and all(c.isalnum() or c == '_' for c in name):
            return name
        print(f"{Fore.YELLOW}Please enter a valid name (letters, numbers, and underscores only){Style.RESET_ALL}")

def present_question(question):
    """Present a question and get user response."""
    # Print category in bright blue
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{question['category']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'-' * len(question['category'])}{Style.RESET_ALL}")
    
    # Print question in bright white
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{question['question']}{Style.RESET_ALL}\n")
    
    # Print options in cyan
    for i, option in enumerate(question['options'], 1):
        print(f"{Fore.CYAN}{i}. {option}{Style.RESET_ALL}")
    
    while True:
        try:
            choice = int(input(f"\n{Fore.GREEN}Enter your choice (1-4): {Style.RESET_ALL}"))
            if 1 <= choice <= len(question['options']):
                selected = question['options'][choice - 1]
                print(f"{Fore.YELLOW}Your answer: {selected}{Style.RESET_ALL}")
                return selected
            print(f"{Fore.RED}Please enter a valid option number.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")

def generate_report_with_ollama(responses):
    """Generate a report using Ollama API."""
    # Format responses for analysis
    analysis_text = "Based on the cyber security questionnaire responses:\n\n"
    
    # Group responses by category
    categories = {}
    for response in responses:
        category = response['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'question': response['question'],
            'answer': response['answer']
        })
    
    # Format responses for analysis
    for category, items in categories.items():
        analysis_text += f"\n{category}:\n"
        for item in items:
            analysis_text += f"- Question: {item['question']}\n"
            analysis_text += f"  Answer: {item['answer']}\n"

    # Prepare prompt for Ollama
    prompt = f"""
    As a cybersecurity expert, analyze the following questionnaire responses and provide:
    1. An assessment of the user's current security practices
    2. Specific areas that need improvement
    3. Actionable recommendations for each area
    4. A summary of good practices already in place

    {analysis_text}
    """

    try:
        # Make API request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=30  # 30 second timeout
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                return {
                    "assessment": {
                        "overall": result['response'],
                        "strengths": [],  # Will be filled by Ollama's analysis
                        "areas_for_improvement": []  # Will be filled by Ollama's analysis
                    },
                    "recommendations": {
                        "critical": [],  # Will be filled by Ollama's analysis
                        "important": [],  # Will be filled by Ollama's analysis
                        "good_practices_to_continue": []  # Will be filled by Ollama's analysis
                    },
                    "conclusion": ""  # Will be filled by Ollama's analysis
                }
            else:
                raise Exception("No response field in Ollama result")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}Error connecting to Ollama: {str(e)}")
        print("Please ensure Ollama is running at http://localhost:11434/")
        print(f"You can start Ollama and try again.{Style.RESET_ALL}")
        sys.exit(1)

def create_test_answer_file():
    """Create a test answer file with sample answers for each question."""
    test_responses = [
        {
            "question_id": "pass_1",
            "category": "Password Security",
            "question": "How often do you change your passwords?",
            "answer": "Every few months"
        },
        {
            "question_id": "pass_2",
            "category": "Password Security",
            "question": "Do you use different passwords for different accounts?",
            "answer": "Most accounts have unique passwords"
        },
        {
            "question_id": "mfa_1",
            "category": "Multi-Factor Authentication",
            "question": "Do you use two-factor authentication when available?",
            "answer": "On some important accounts"
        },
        {
            "question_id": "net_1",
            "category": "Network Security",
            "question": "How do you handle public Wi-Fi networks?",
            "answer": "I use them but avoid sensitive transactions"
        },
        {
            "question_id": "upd_1",
            "category": "System Updates",
            "question": "How do you manage software updates?",
            "answer": "I install them within a few days"
        },
        {
            "question_id": "bkp_1",
            "category": "Data Backup",
            "question": "How often do you backup your important data?",
            "answer": "Regular manual backups"
        },
        {
            "question_id": "phi_1",
            "category": "Phishing Awareness",
            "question": "How do you handle unexpected emails with links?",
            "answer": "I verify the sender's email carefully"
        },
        {
            "question_id": "dev_1",
            "category": "Device Security",
            "question": "How do you secure your mobile devices?",
            "answer": "Biometric authentication"
        },
        {
            "question_id": "soc_1",
            "category": "Social Media",
            "question": "What information do you share on social media?",
            "answer": "Limited personal information"
        },
        {
            "question_id": "enc_1",
            "category": "Data Encryption",
            "question": "Do you encrypt sensitive files or communications?",
            "answer": "For some sensitive data"
        }
    ]
    save_answers(test_responses, "test")
    
    # Generate and save a test report
    report = generate_report_with_ollama(test_responses)
    save_report(report, "test")

def main():
    """Main function to run the questionnaire."""
    # Ensure directories exist
    os.makedirs('answers', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    # Create test answer file
    create_test_answer_file()

    clear_screen()
    print(f"{Fore.CYAN}{Style.BRIGHT}Cyber Security Knowledge Assessment{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=================================={Style.RESET_ALL}")
    
    # Get user's name
    user_name = get_user_name()
    
    print(f"\n{Fore.GREEN}Welcome, {user_name}!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This questionnaire will assess your cyber security practices.")
    print(f"Please answer each question honestly for the most accurate assessment.{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to begin...{Style.RESET_ALL}")

    data = load_questions()
    responses = []

    for question in data['questions']:
        clear_screen()
        answer = present_question(question)
        responses.append({
            'question_id': question['id'],
            'category': question['category'],
            'question': question['question'],
            'answer': answer
        })

    # Save answers
    answers_file = save_answers(responses, user_name)
    
    # Generate and save report
    clear_screen()
    print(f"\n{Fore.YELLOW}Generating your cyber security assessment report...{Style.RESET_ALL}")
    report = generate_report_with_ollama(responses)
    timestamp = get_formatted_timestamp()
    report_file = save_report(report, user_name)
    markdown_file = save_markdown_report(report, user_name, timestamp)
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Your Cyber Security Assessment Report{Style.RESET_ALL}")
    print(f"{Fore.CYAN}====================================={Style.RESET_ALL}")
    print(json.dumps(report, indent=2))
    
    print(f"\n{Fore.GREEN}Thank you for completing the assessment!{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}Files saved:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Answers: {answers_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}JSON Report: {report_file}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Markdown Report: {markdown_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
