import streamlit as st
from openai import OpenAI
import os

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("🔑 OpenAI API key not found!")
    st.info("Please set your OPENAI_API_KEY environment variable to use this app.")
    st.code("export OPENAI_API_KEY='your-api-key-here'")
    st.stop()

client = OpenAI(api_key=api_key)

# App title
st.title("🍽️ AI Meal Planner")
st.write("Generate a personalized meal plan based on your preferences and budget")

# User inputs
st.header("Tell me about your preferences")

col1, col2 = st.columns(2)

with col1:
    dietary_prefs= st.selectbox(
        "Select a meal theme",
        options=["Balanced", "Low Carb", "High Protein", "Vegetarian", "Vegan", "Keto"]
    )  
    num_meals = st.number_input("Number of meals", min_value=1, max_value=21, value=3)

with col2:
    cuisine = st.selectbox(
        "Preferred cuisine",
        options=["Any","Asian", "Nigerian", "European", "Americas","Caribbean"]
    )
    goal=st.selectbox(
        "What is your primary goal?",
        options=["Lose Weight", "Maintain Weight", "Gain Muscle", "Improve Energy"]
    )
    cooking_skill = st.select_slider(
        "Cooking skill level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )

# Generate button
if st.button("🎯 Generate Meal Plan", type="primary"):
    if not dietary_prefs:
        dietary_prefs = "No restrictions"
    
    try:
        with st.spinner("Creating your personalized meal plan..."):
            # Create the prompt
            prompt = f"""Create a practical meal timetable and a weekly meal plan with these details:
            - Dietary preferences: {dietary_prefs} 
            - Number of meals: {num_meals}
            - Cooking skill: {cooking_skill}
            - Preferred cuisine: {cuisine}
            - Goal: {goal}

            Format your response with clear sections:
            ## 🍽️ Food Timetable
            (Put it in a table format for each day. Include breakfast, lunch, dinner, and snacks according to the number of meals {num_meals} selected. For each row, add recommended serving sizes. For instance, "2 eggs (140 calories)"  and their total calories.
            Each meal should have all the food classes)
            
            ## 🍽️ MEALS
            (List each meal with name, key ingredients, and prep time)
            
            ## 🛒 GROCERY LIST
            (Organized by category: Produce, Proteins, Pantry, etc.)
             
            ## 💡 TIPS
            (Meal prep suggestions, storage tips, money-saving ideas)
            
            Keep it realistic and achievable for a {cooking_skill.lower()} cook."""
            
            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert meal planning assistant who creates practical meal plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Get and display the result
            meal_plan = response.choices[0].message.content
            st.success("✅ Your meal plan is ready!")
            st.markdown(meal_plan)
            
            # Download button
            st.download_button(
                label="📥 Download Meal Plan",
                data=meal_plan,
                file_name=f"meal_plan_{num_meals}_meals.txt",
                mime="text/plain"
            )
            
    except (ConnectionError, TimeoutError) as e:
        st.error("🌐 Network Error: Unable to connect to OpenAI")
        st.info("Please check your internet connection and try again.")
    except PermissionError as e:
        st.error("🔑 API Key Error: Please check your OpenAI API key")
    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg:
            st.error("🔑 API Key Error: Please check your OpenAI API key")
        elif "rate" in error_msg or "quota" in error_msg:
            st.error("⏱️ Rate Limit: You've exceeded your API usage limit")
            st.info("Please wait a moment and try again, or check your OpenAI billing.")
        elif "network" in error_msg or "connection" in error_msg:
            st.error("🌐 Network Error: Unable to connect to OpenAI")
            st.info("Please check your internet connection and try again.")
        else:
            st.error(f"❌ Something went wrong: {str(e)}")
        
        st.info("💡 Need help? Make sure you have:")
        st.write("• A valid OpenAI API key set as environment variable")
        st.write("• Sufficient API credits in your OpenAI account")
        st.write("• A stable internet connection")
        