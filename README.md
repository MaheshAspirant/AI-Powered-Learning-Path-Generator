# Learning Path Generator with Model Context Protocol (MCP)

This project is a Streamlit-based web application that generates personalized learning paths using the Model Context Protocol (MCP). It integrates with various services including YouTube, Google Drive, and Notion to create comprehensive learning experiences.

## ✨ Features

- 🎯 **Personalized Learning Paths**: Generate customized day-wise learning paths based on your goals
- 🎥 **YouTube Integration**: Automatically create playlists with curated educational videos
- 📁 **Google Drive Integration**: Store learning paths as organized documents
- 📝 **Notion Integration**: Create structured learning pages in Notion
- 🚀 **Real-time Progress Tracking**: Monitor generation progress with detailed status updates
- 🎨 **User-friendly Interface**: Intuitive Streamlit interface with validation and error handling
- ⚙️ **Configuration Management**: Support for environment variables and UI-based configuration
- 🔒 **Input Validation**: Comprehensive validation for URLs, API keys, and user inputs

## 📋 Prerequisites

- Python 3.10 or higher
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/apikey))
- Pipedream URLs for integrations:
  - YouTube (required)
  - Google Drive or Notion (optional, choose one)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-learning-path-demo-main
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Option 1: Environment Variables (Recommended for Production)

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_PIPEDREAM_URL=https://your-youtube-pipedream-url.com
DRIVE_PIPEDREAM_URL=https://your-drive-pipedream-url.com
NOTION_PIPEDREAM_URL=https://your-notion-pipedream-url.com
```

### Option 2: UI Configuration (Recommended for Development)

Configure all settings directly in the application sidebar when running the app.

## 🏃 Running the Application

To start the application, run:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## 📖 Usage

1. **Configure Settings**: Enter your Google AI Studio API key and Pipedream URLs in the sidebar
2. **Select Tool**: Choose your preferred secondary tool (Drive or Notion)
3. **Enter Goal**: Describe your learning goal in detail (e.g., "I want to learn Python programming basics in 5 days, focusing on data structures and algorithms")
4. **Generate**: Click "Generate Learning Path" to create your personalized learning plan
5. **Review Results**: Access your learning path document and YouTube playlist from the generated links

### Example Learning Goals

- "I want to learn Python basics in 3 days"
- "Create a 7-day web development bootcamp focusing on React and Node.js"
- "I want to learn data science fundamentals in 10 days with hands-on projects"

## 📁 Project Structure

```
mcp-learning-path-demo-main/
├── app.py              # Main Streamlit application with UI
├── utils.py            # Utility functions, agent setup, and async handling
├── prompt.py           # AI agent prompt template
├── config.py           # Configuration management and environment variables
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## 🔧 Key Components

### `app.py`
- Streamlit UI with enhanced error handling
- Input validation for URLs and API keys
- Real-time progress tracking
- Session state management

### `utils.py`
- Agent initialization and tool configuration
- Async/await pattern implementation
- Comprehensive error handling and logging
- URL and API key validation

### `config.py`
- Environment variable management
- Configuration validation
- Default settings

### `prompt.py`
- System prompt for the AI agent
- Step-by-step instructions for learning path generation

## 🛠️ Technical Details

- **Framework**: Streamlit for UI
- **AI Model**: Google Gemini 2.5 Flash (configurable)
- **Protocol**: Model Context Protocol (MCP)
- **Async Support**: Full async/await pattern with proper event loop management
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Logging**: Structured logging for debugging and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your Google API key is valid and has proper permissions
2. **URL Validation Errors**: Check that your Pipedream URLs start with `http://` or `https://`
3. **Generation Failures**: Verify all required URLs are configured and accessible
4. **Import Errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Support

For issues and questions, please [create an issue](link-to-issues) or contact the maintainers.
