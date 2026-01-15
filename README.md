# 📚 LLM Lecture Summarizer & Quiz Generator

A Streamlit-based application that transforms YouTube lectures and documents into concise summaries and interactive practice quizzes using AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0+-green.svg)

## ✨ Features

- **🎬 YouTube Transcript Extraction** - Paste any YouTube URL with captions
- **📄 Document Parsing** - Upload PDF or PowerPoint files
- **🧠 AI Summarization** - Powered by Gemini or DeepSeek with chunking for long content
- **🧪 Interactive Quiz** - Auto-generated multiple choice questions with scoring
- **🤖 Multiple AI Models** - Choose between Gemini and DeepSeek models

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/noahvlone/LLM-Summarizer.git
cd LLM-Summarizer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run the application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Output
![Image](https://github.com/user-attachments/assets/48f2deea-152f-49ba-a2d8-8612889f916f)

![Image](https://github.com/user-attachments/assets/d4974dd8-50b0-4973-bc3a-24b62b984cf1)

![Image](https://github.com/user-attachments/assets/ef7fbf29-2d76-4bba-920a-19f36296b3a0)

## 🔑 API Keys Required

| Provider | Get API Key |
|----------|-------------|
| Google Gemini | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| DeepSeek | [DeepSeek Platform](https://platform.deepseek.com/) |

## 📁 Project Structure

```
LLM-Summarizer/
├── app.py                     # Main Streamlit application
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── modules/
│   ├── youtube_extractor.py   # YouTube transcript extraction
│   ├── document_parser.py     # PDF/PPTX parsing
│   ├── text_processor.py      # Text chunking utilities
│   └── ai_engine.py           # LangChain + AI integration
└── components/
    ├── input_section.py       # Input UI components
    ├── summary_display.py     # Summary rendering
    └── quiz_component.py      # Interactive quiz UI
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: LangChain, Google Gemini, DeepSeek
- **YouTube**: youtube-transcript-api
- **Documents**: PyMuPDF (PDF), python-pptx (PowerPoint)

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
