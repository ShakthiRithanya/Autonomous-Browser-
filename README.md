# Autonomous Browser Agent

An AI-powered autonomous browser agent that can open a browser, understand natural language tasks, and autonomously browse, search, click, fill forms, and scrape data.

Built with [Python](https://www.python.org/), [Playwright](https://playwright.dev/), [Browser Use](https://github.com/browser-use/browser-use), and [Google Gemini](https://deepmind.google/technologies/gemini/)/[OpenAI](https://openai.com/).

## Features

- **Natural Language Control**: Describe tasks in plain English.
- **Autonomous Navigation**: Handles clicks, typing, scrolling, and navigation automatically.
- **Multi-Provider Support**: Switch between Google Gemini (default) and OpenAI GPT-4.
- **Data Extraction**: Extract structured data (JSON/CSV) and summaries.
- **Safety**: Configurable limits on steps and actions.
- **Artifacts**: Saves screenshots, logs, and extracted paths for every run.

## Setup

1. **Clone the repository** (if applicable) or download the source.

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Configuration**:
   Create a `.env` file in the root directory with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Run the agent via the CLI:

```bash
python -m src.main
```

You will be prompted to enter a task.

### Command Line Arguments

- `--task "your task here"`: Skip the interactive prompt.
- `--provider openai`: Use OpenAI instead of Gemini.
- `--demo [github|news|table]`: Run a pre-defined demo scenario.

### Examples

**1. GitHub Stars Fetcher**
```bash
python -m src.main --demo github
```
*Goal: Opens the browser-use repo and retrieves the star count.*

**2. News Search**
```bash
python -m src.main --demo news
```
*Goal: Searches for 'Google Antigravity' and summarizes top results.*

**3. Table Scraper**
```bash
python -m src.main --demo table
```
*Goal: Scrapes a sample HTML table into a CSV file.*

**4. Custom Task**
```bash
python -m src.main --task "Go to amazon.com, search for 'gaming laptop', and save the first product title and price to a file."
```

## Project Structure

- `src/main.py`: CLI entry point.
- `src/agent.py`: Wrapper around the `browser-use` Agent.
- `src/workflows.py`: Helper functions for specific workflows.
- `src/config.py`: Environment and LLM configuration.
- `runs/`: Stores output artifacts (logs, screenshots) for each session.

## Safety & Limitations

- **Robots.txt**: The agent attempts to respect standard web usage policies, but you are responsible for the sites you scrape.
- **Credentials**: Never hardcode passwords. Ensure `.env` is git-ignored.
- **Loops**: The agent has a maximum step limit to prevent infinite loops.

## License

Educational use only.
