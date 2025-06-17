# Code Review Assistant

A web application that helps review code merge requests using AI.

## Features

- Analyze code changes from URLs or text files
- Generate comprehensive code reviews including:
  - Executive summary
  - Syntax review
  - Code style (PEP8 compliance)
  - Performance analysis (especially for Apache Spark)
- Copy-to-clipboard functionality for easy MR updates

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up OpenAI API key:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter either a URL or paste the code content
2. Click "Generate Review"
3. The AI will analyze the code and provide a comprehensive review
4. Use the copy buttons to easily copy sections to your MR

## Note

This application uses OpenAI's GPT-3.5 model for code review. Make sure you have a valid OpenAI API key and sufficient credits.
