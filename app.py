import streamlit as st
import joblib
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import google.generativeai as genai
def apply_custom_theme():
    st.markdown(
        """
        <style>
        :root {
            --primary-color: #BD5E8E;  /* Raspberry/Rose */
            --secondary-color: #5D2A6D; /* Medium purple */
            --accent-color: #D4AF37;    /* Gold accent */
            --background-color: #F8F5FA; /* Very light purple-tinted background */
            --card-color: #FFFFFF;      /* White for cards */
            --text-color: #333333;      /* Dark text for contrast */
            --font: 'Montserrat', sans-serif;
        }
        body {
            font-family: var(--font);
            color: var(--text-color);
            background-color: var(--background-color);
        }
        .stApp {
            background-color: var(--background-color);
            background-image: linear-gradient(135deg, #F8F5FA 25%, #F0EBF7 100%);
        }
        h1 {
            color: var(--primary-color);
            font-weight: 600;
        }
        h2, h3, h4, h5, h6 {
            color: var(--secondary-color);
            font-weight: 500;
        }
        .sidebar .sidebar-content {
            background-image: linear-gradient(180deg, #F0EBF7 0%, #E8E1F2 100%);
            border-right: 1px solid rgba(189, 94, 142, 0.2);
        }
        .css-1lcbmhc {
            background-image: linear-gradient(180deg, #F0EBF7 0%, #E8E1F2 100%);
        }
        /* Main content area */
        .css-ke7pzk {
            background-color: transparent;
        }
        /* Container styling with subtle rose border */
        .css-1r6slb0, .css-12w0qpk, .stAlert {
            background-color: var(--card-color);
            border: 1px solid rgba(189, 94, 142, 0.25);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        /* Button styling */
        .stButton>button {
            background: linear-gradient(45deg, #BD5E8E, #CB648F);
            color: white;
            border: none;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(189, 94, 142, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #CB648F, #DA6A96);
            box-shadow: 0 4px 12px rgba(189, 94, 142, 0.4);
            transform: translateY(-2px);
        }
        /* Input fields with rose accent */
        input, select, textarea {
            background-color: #FFFFFF !important;
            color: #333333 !important;
            border: 1px solid rgba(189, 94, 142, 0.3) !important;
            border-radius: 6px !important;
        }
        input:focus, select:focus, textarea:focus {
            border: 1px solid rgba(189, 94, 142, 0.8) !important;
            box-shadow: 0 0 0 2px rgba(189, 94, 142, 0.2) !important;
        }
        /* Slider color */
        .stSlider div[data-baseweb="slider"] div {
            background-color: var(--primary-color) !important;
        }
        /* Progress bar */
        .stProgress div {
            background-color: var(--primary-color) !important;
        }
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #F0EBF7;
            border-radius: 8px;
            padding: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: var(--text-color);
            border-radius: 6px;
        }
        .stTabs [aria-selected="true"] {
            background-color: white;
            border-bottom: 2px solid var(--primary-color) !important;
        }
        /* Dropdown menu */
        div[data-baseweb="select"] > div {
            background-color: white !important;
            border: 1px solid rgba(189, 94, 142, 0.3) !important;
        }
        /* Gold accents for certain elements */
        .stCheckbox label span p {
            color: var(--secondary-color) !important;
        }
        .stExpander {
            border-left: 1px solid var(--accent-color) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

 # Load and display the image
image = Image.open("/content/h1.jpg")
st.image(image, caption="Your Image",use_container_width=True)
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.0-pro")  # Replace with an available model if necessary
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
# Load Gemini AI API Key
GEMINI_API_KEY = "AIzaSyDksYfC5E_CukbN7ajfwiFREQrrzI9p5-o"
genai.configure(api_key=GEMINI_API_KEY)

# Emergency Contact Details
TWILIO_ACCOUNT_SID = "AC8e3795d546f72c37c9f619daa0755ce0"
TWILIO_AUTH_TOKEN = "1887dcd36a846c4fd053ce742c520e50"
TWILIO_PHONE_NUMBER = "+19788296514"  # Replace with Twilio number
EMERGENCY_PHONE = " +918208697027"  # Replace with actual emergency contact number

 

def send_sms_alert(name, risk_level):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = f"🚨 Emergency Alert: {name} has a  lots of love for you ma ({risk_level})! Immediate help needed!"

    try:
        client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=EMERGENCY_PHONE)
        st.success("📲 Emergency SMS sent successfully!")
    except Exception as e:
        st.error(f"⚠️ Error sending SMS: {e}")

st.title("🚑 Heart Attack Prediction with SOS Alert")

# Input fields
name = st.text_input("Enter Patient Name")
risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])

# SOS Button
if st.button("🚨 Send Emergency Alert"):
    if risk_level == "High":
        send_sms_alert(name, risk_level)
    else:
        st.warning("⚠️ Alert only triggers for High Risk cases.")



# Load the trained Random Forest model and scaler
def load_model_and_scaler():
    try:
        rf_model = joblib.load('/content/heart_risk_model.pkl')
        scaler = joblib.load('/content/scaler.pkl')
        return rf_model, scaler
    except FileNotFoundError as e:
        st.error(f"Error: Model or scaler file not found. Please ensure 'random_forest_model.pkl' and 'scaler.pkl' are in the correct directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model or scaler: {e}")
        st.stop()

# Function for heart attack risk prediction
def predict_heart_attack_risk(user_input, scaler, model):
    """Predict heart attack risk and provide detailed advice."""

    # Scale the user input
    try:
        scaled_input = scaler.transform(np.array(user_input).reshape(1, -1))
    except Exception as e:
        st.error(f"Error scaling input data: {e}. Please check your input values.")
        return None, None, None, None, None, None, None  # Return None values to prevent further errors

    # Make prediction
    try:
        prediction = model.predict(scaled_input)[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}. Please ensure the model is compatible with the input data.")
        return None, None, None, None, None, None, None  # Return None values to prevent further errors

    # Define messages based on prediction
    if prediction == 1:
        risk_level = "High"
        message = (
            "You are at high risk of a heart attack. Immediate consultation with a cardiologist is strongly advised. "
            "It is crucial to take this seriously and act promptly to mitigate potential health risks. 🚨"
        )

        precautions = [
            "1. Consult a Cardiologist Immediately: Schedule an appointment for a thorough evaluation. 👩‍⚕",
            "2. Modify Diet: Switch to a heart-healthy diet, reducing saturated and trans fats 🍔 and increasing fiber 🥦.",
            "3. Start Light Exercise: If cleared by a doctor, begin with low-impact activities. 🚶‍♀",
            "4. Strictly Adhere to Medications: Take all prescribed medications exactly as directed. 💊",
            "5. Monitor Symptoms Closely: Keep a close watch on any chest pain 💔, shortness of breath 😮‍💨, or unusual fatigue 😴."
        ]

        guidance = [
            "1. Follow Medication Plan: Adhere to your prescribed medication schedule without alterations. ⏰",
            "2. Adopt a Balanced Lifestyle: Focus on diet 🥗, stress management 🧘‍♀, and regular moderate activity 🚴.",
            "3. Schedule Regular Check-ups: Frequent check-ups help in monitoring your condition effectively. 📅",
            "4. Manage Stress Levels: Employ techniques like meditation 🧘 or yoga to lower stress. 😌",
            "5. Involve a Support System: Engage family and friends for emotional and practical support. 🫂"
        ]

        exercise = [
            "1. Consult Your Doctor: Get a tailored exercise plan from your healthcare provider. 👨‍⚕",
            "2. Start Slowly: Begin with very gentle activities such as walking 🚶 or light stretching.",
            "3. Build Gradually: Incrementally increase exercise intensity and duration over time. 📈",
            "4. Choose Enjoyable Activities: Opt for exercises you find pleasurable and motivating. 😄",
            "5. Listen To Your Body: Do not ignore any pain or discomfort; adjust accordingly. 🙏"
        ]

        diet = [
            "1. Prioritize Heart-Healthy Foods: Emphasize fruits 🍎, vegetables 🥦, lean proteins 🍗, and whole grains 🌾.",
            "2. Limit Unhealthy Fats: Minimize saturated and trans fats to protect your arteries. 🍟",
            "3. Reduce Sodium Intake: Lower sodium to manage blood pressure effectively. 🧂",
            "4. Stay Hydrated: Drink plenty of water to support overall cardiovascular function. 💧",
            "5. Avoid Processed Foods: Reduce or eliminate processed foods high in sugars and fats. 🍩"
        ]

        medications = [
            "1. Stick to Prescriptions: Strictly follow prescribed medication dosages and timings. 💊",
            "2. Understand Each Medication: Know the purpose and potential side effects of each medicine. ℹ",
            "3. Regular Review: Review all medications with your healthcare provider regularly. 👩‍⚕",
            "4. Do Not Self-Medicate: Avoid taking any other medications without consulting your doctor. 🚫",
            "5. Report Side Effects: Promptly report any side effects to your doctor. 🗣"
        ]

    else:
        risk_level = "Low"
        message = (
            "Your heart attack risk appears to be low. ✅ However, it is essential to maintain a healthy lifestyle 🏃‍♀ to ensure long-term cardiovascular health. ❤️"
        )

        precautions = [
            "1. Continue Regular Check-ups: Maintain routine appointments with your primary care physician. 👩‍⚕",
            "2. Monitor Health Metrics: Keep track of blood pressure, cholesterol, and blood sugar levels. 📊",
            "3. Maintain a Healthy Lifestyle: Continue with a balanced diet 🥗 and regular exercise routine 🏋‍♀.",
            "4. Stay Informed: Be proactive in learning about heart health and risk factors. 📚",
            "5. Plan for Emergencies: Have a plan in place in case of any sudden health issues. 📅"
        ]

        guidance = [
            "1. Maintain Balanced Diet: Ensure a diverse intake of fruits 🍎, vegetables 🥦, and whole grains 🌾.",
            "2. Stay Active Daily: Engage in at least 150 minutes of moderate aerobic exercise per week. 🏃",
            "3. Practice Stress Reduction: Use techniques like mindfulness 🧘 or yoga to manage stress. 😌",
            "4. Moderate Alcohol Intake: Adhere to recommended limits for alcohol consumption. 🍺",
            "5. Avoid Smoking: Refrain from smoking 🚭 to maintain optimal heart health. ❤️"
        ]

        exercise = [
            "1. Mix Up Activities: Include cardio 🏃, strength training 💪, and flexibility exercises.",
            "2. Be Consistent: Make physical activity a regular part of your daily routine. 📅",
            "3. Enjoy Your Workouts: Select activities that you find enjoyable and motivating. 😄",
            "4. Set Achievable Goals: Establish realistic fitness goals tailored to your ability. 🎯",
            "5. Listen to Your Body's Signals: Adjust your activity level based on how you feel. 🙏"
        ]

        diet = [
            "1. Focus on Whole Foods: Limit processed foods, emphasizing fruits 🍎, vegetables 🥦, and whole grains 🌾.",
            "2. Stay Hydrated: Drink plenty of water throughout the day. 💧",
            "3. Control Portions: Practice mindful eating to maintain a healthy weight. ⚖",
            "4. Plan Your Meals: Prepare meals in advance to make healthier choices. 🍱",
            "5. Seek Nutritional Advice: Consult a nutritionist for personalized guidance if needed. 👩‍⚕"
        ]

        medications = [
            "1. Consult Your Doctor Regularly: Discuss any health concerns or medication questions with them. 👩‍⚕",
            "2. Prioritize Prevention: Focus on lifestyle changes that can prevent heart issues. 💪",
            "3. Review Annually: Review your medications and health status annually with your doctor. 📅",
            "4. Stay Aware of Changes: Note any changes in how you feel after starting or stopping medications and report them promptly. 📝",
            "5. Be Informed: Educate yourself about your health conditions and medications. 📚"
        ]

    return risk_level, message, precautions, guidance, exercise, diet, medications

# Set up Streamlit app


# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Power BI Dashboard", "About App & Modules", "Symptoms Information"]
)


if page == "Home":

    # Load model and scaler
    rf_model, scaler = load_model_and_scaler()

    # Check if model and scaler loaded successfully
    if not rf_model or not scaler:
        st.error("Model and scaler could not be loaded.")
        st.stop()
        # Load model and scaler
model = joblib.load("heart_risk_model.pkl")
scaler = joblib.load("scaler.pkl")

    # Collect input features from the user through Streamlit widgets
st.sidebar.header("Patient Information")


# Inputs
age = st.sidebar.number_input("Age", 20, 90)
sex = st.sidebar.selectbox("Sex (0 = Female, 1 = Male)", [0, 1])
cp = st.sidebar.number_input("Chest Pain Type (cp)", 0, 3)
trestbps = st.sidebar.number_input("Resting Blood Pressure", 80, 200)
chol = st.sidebar.number_input("Cholesterol", 100, 400)
fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
restecg = st.sidebar.number_input("Resting ECG (restecg)", 0, 2)
thalach = st.sidebar.number_input("Max Heart Rate", 60, 220)
exang = st.sidebar.selectbox("Exercise Induced Angina", [0, 1])
oldpeak = st.sidebar.number_input("Oldpeak", 0.0, 6.0)
slope = st.sidebar.number_input("Slope", 0, 2)
ca = st.sidebar.number_input("Number of Major Vessels (ca)", 0, 4)
thal = st.sidebar.number_input("Thal", 0, 3)

# Prediction
if st.sidebar.button("Predict Risk"):
    data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs,
                          restecg, thalach, exang, oldpeak,
                          slope, ca, thal]],
                        columns=['age','sex','cp','trestbps','chol','fbs',
                                 'restecg','thalach','exang','oldpeak',
                                 'slope','ca','thal'])

    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)

    if prediction[0] == 1:
        st.error("⚠ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")
        user_input = [
        age, sex, cp, trestbps, chol, fbs,
        restecg, thalach, exang, oldpeak,
        slope, ca, thal
    ]



        # Call the prediction function
        risk_level , message , precautions , guidance , exercise , diet , medications = predict_heart_attack_risk( user_input , scaler , rf_model)

        # Check if the prediction was successful
        if risk_level is not None:
            # Display the prediction results
             # Correcting the Heading Here
            st.subheader("Prediction Results")

            # Using Markdown to make Risk Level more attractive
            if risk_level == "High":
                st.markdown(f"<h3 style='color:red;'>Risk Level: <span style='font-weight: bold; color: red;'>{risk_level}</span></h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:green;'>Risk Level: <span style='font-weight: bold; color: green;'>{risk_level}</span></h3>", unsafe_allow_html=True)

            st.write(message)

            st.subheader("RECOMMENDATIONS:")

            st.markdown("PRECAUTIONS-")
            for rec in precautions:
                st.write(rec)

            st.markdown("---")

            st.markdown("GUIDANCE-")
            for rec in guidance:
                st.write(rec)

            st.markdown("---")

            st.markdown("EXERCISE-")
            for rec in exercise:
                st.write(rec)

            st.markdown("---")

            st.markdown("DIET-")
            for rec in diet:
                st.write(rec)

            st.markdown("---")

            st.markdown("MEDICATIONS")
            for rec in medications:
                st.write(rec)
elif page == "Power BI Dashboard":
    st.title("📊 Heart Attack Analytics Dashboard")

    st.markdown(
        """
        This dashboard provides real-time visual insights into:
        - Patient risk distribution
        - Feature-wise impact analysis
        - Prediction trends
        - Health parameter correlations
        """
    )

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNTFiNzAxZjAtOTc5MS00NmNmLTgzZWEtOTVhZDljODBmNTU4IiwidCI6Ijk4MDA5ZTA5LTM5ZTktNGRkNi05OTdjLWQ3MDdlMTRmNGZiYyJ9"
    st.components.v1.iframe(
        powerbi_url,
        width=1200,
        height=700,
        scrolling=True
    )

elif page == "About App & Modules":
    # About App Section
    st.header("About This Application")
    image = Image.open("/content/hq720.jpg")
    st.image(image, caption="Your Image",use_container_width=True)
    st.write("""
     HEARTLY is an AI-based healthcare support system designed to predict the risk of heart disease using clinical and lifestyle parameters.
The application helps in early risk detection, enabling preventive action before emergencies occur.
It integrates Machine Learning, Data Analytics, Visualization, and Real-time Alert Systems into a single platform.
The system is designed for patients, doctors, and caregivers to support data-driven healthcare decisions.
    
  Dataset & Parameters (ML Module)

The model uses 13 clinically important parameters, including:
Age, Sex, Chest Pain Type
Resting Blood Pressure, Cholesterol
Fasting Blood Sugar
ECG Results, Maximum Heart Rate
Exercise-Induced Angina
ST Depression (Oldpeak)
Slope, Major Vessels (ca), Thalassemia
These parameters are standard features used in real-world cardiac risk assessment, ensuring medical relevance.
The dataset was collected through a combination of manual curation and publicly available medical datasets, with validation from open-source repositories.  
    
    """)

    # About Modules Section
    st.subheader("Modules Used")
    image = Image.open("/content/istockphoto-1515913422-612x612.jpg")
    st.image(image, caption="Your Image",use_container_width=True)
    st.write("""
    - RMultiple ML algorithms were tested and compared.

Random Forest Classifier achieved the highest accuracy (~90%) due to:
Use of all 13 relevant parameters
Better handling of feature interactions
Reduced overfitting
Proper train-test splitting, scaling, and evaluation metrics were applied.

The model is capable of real-time predictions through a deployed web interface.
    """)

elif page == "Symptoms Information":
    # Symptoms Information Section
    st.header("Heart Attack Symptoms")
    image = Image.open("/content/190206-heart-attack-warning-signs-infographic-aha.webp")
    st.image(image, caption="Your Image",use_container_width=True)
    
    st.write("""
    Recognizing the symptoms of a heart attack is crucial for timely intervention.

    Common symptoms include:

    - Chest Pain or Discomfort: Often described as pressure or squeezing sensation.

    - Shortness of Breath: May occur with or without chest discomfort.

    - Pain or Discomfort in Other Areas: Such as arms (especially left arm), shoulder blades,
      neck jaw back stomach.

    - Nausea/Vomiting: Some individuals may experience stomach upset along with other symptoms.

    - Lightheadedness/Fainting: Feeling dizzy or faint can also indicate an issue related to heart health.

    If you experience any of these symptoms especially if they last more than few minutes seek immediate medical attention!

    Remember that symptoms can vary between individuals especially between men & women!
    """
)


# Gemini AI Integration Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("HEARTLY ❤️")
ai_prompt = st.sidebar.text_area("Ask HEARTLY about WHAT DO YOU WANT TO ASK:")

if st.sidebar.button("🔍 ASK ME"):
    if ai_prompt:
        response = get_gemini_response(ai_prompt)
        st.sidebar.write("* HEARTLY Response:*")
        st.sidebar.write(response)
    else:
        st.sidebar.warning("⚠ Please enter a question.")
# Add a disclaimer at the bottom of each page
st.markdown(
    "<hr style='border:2px solid gray'>", unsafe_allow_html=True)  # Adding horizontal line before disclaimer
st.markdown(
    "<strong>Disclaimer:</strong> This app provides general predictions based on user input but should not be used as substitute for professional medical advice."
    + "<br>Consult with qualified healthcare provider regarding any health concerns.", unsafe_allow_html=True)
