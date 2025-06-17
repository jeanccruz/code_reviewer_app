# Code Review Assistant

A Flask-based web application that uses Google Gemini AI to review code changes and provide actionable feedback for Python and Apache Spark code.

## Features

- Analyze code changes from URLs or text files
- Generate comprehensive code reviews including:
  - Executive summary
  - Syntax review
  - Code style (PEP8 compliance)
  - Performance analysis (especially for Apache Spark)
- Supports custom reviewer instructions—users can add extra context or requirements to the prompt
- Logs all reviews for future reference
- Secure handling of API keys (uses environment variables; `.env` is gitignored)

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
3. Set up your Gemini API key:
    - Obtain your Gemini API key from Google.
    - Set the environment variable in your shell or create a `.env` file (if using a tool like `python-dotenv`):
      ```
      GEMINI_API_KEY=your_api_key_here
      ```
    - **Do not commit your API key or `.env` file.**
4. Run the application:
    ```bash
    python app.py
    ```
5. Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

## Usage

1. Enter a review name and either a URL or paste the code content.
2. (Optional) Add custom reviewer instructions for the AI.
3. Click "Generate Review".
4. The AI will analyze the code and provide a structured review.
5. Use the copy buttons to easily copy sections to your merge request or documentation.
6. View past reviews in the "Logs" tab.

## Security Note
- Your Gemini API key is never committed to the repository. The `.gitignore` excludes `.env` and similar files by default.
- Never share your API key publicly.

## License
MIT License. See [LICENSE](LICENSE) for more information.

## Author
[jeanccruz](https://github.com/jeanccruz)

---

*This project is not affiliated with Google or OpenAI. For educational and productivity purposes only.*
