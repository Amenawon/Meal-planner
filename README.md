# 🍽️ AI Meal Planner

A Streamlit app that generates personalized meal plans using OpenAI's GPT API.

## Features

- 🎯 Personalized meal planning based on dietary preferences
- 🍳 Adjustable cooking skill levels
- 📊 Goal-oriented plans (weight loss, muscle gain, etc.)
- 📥 Downloadable meal plans
- 🛒 Organized grocery lists
- 💡 Helpful meal prep tips

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd meal-prep
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit openai python-dotenv
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## Security Note

⚠️ **Never commit your `.env` file!** It contains sensitive API keys.