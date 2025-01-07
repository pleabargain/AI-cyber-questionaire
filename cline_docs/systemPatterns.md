# System Patterns

## Architecture Overview
The system follows a modular architecture with these key components:
1. Data Collection Layer (JSON-based questionnaire)
2. Processing Layer (Ollama integration)
3. Report Generation Layer

## Key Technical Decisions
1. JSON Format for Questionnaire
   - Provides structured data storage
   - Easy to modify and extend
   - Human-readable format
   - Simple to process programmatically

2. Python Implementation
   - Main application logic in Python
   - JSON processing capabilities
   - Integration with Ollama

3. Ollama Integration
   - AI-powered analysis of responses
   - Generation of personalized recommendations
   - Natural language processing capabilities

## Design Patterns
1. Data Structure
   ```json
   {
     "questions": [
       {
         "id": "string",
         "category": "string",
         "question": "string",
         "type": "string",
         "options": ["string"] // for multiple choice
       }
     ],
     "responses": [
       {
         "question_id": "string",
         "answer": "string"
       }
     ]
   }
   ```

2. Report Structure
   - Assessment summary
   - Detailed analysis by category
   - Specific recommendations
   - Action items for improvement
