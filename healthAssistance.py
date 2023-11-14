
from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import sqlite3

import spacy

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)
def determine_intent(preprocessed_input): # type: ignore
    # Implement intent detection using spaCy
    doc = nlp(preprocessed_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    if any(label in ["SYMPTOM", "DISEASE"] for _, label in entities):
        return "symptoms"
    elif any(label in ["DIAGNOSIS", "ISSUE"] for _, label in entities):
        return "diagnosis"
    elif any(label in ["MEDICATION", "MEDICINE"] for _, label in entities):
        return "medication"
    else:
        return "unknown"
# Create a chatbot instance
chatbot = ChatBot('Health Assistant')
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on health-related data from ChatterBot's corpus
trainer.train('chatterbot.corpus.english.health')

custom_data = [
    "What is diabetes?",
    "Diabetes is a chronic condition that affects how your body processes glucose."

]

list_trainer = ListTrainer(chatbot)
list_trainer.train(custom_data)

# Set up the database connection and create a table to store chat history
conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE chat_history (
        id INTEGER PRIMARY KEY,
        user_input TEXT,
        response TEXT
    )
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_input(user_input):
    # Implement input preprocessing logic, e.g., text cleaning, lowercasing, etc.
    # Return the preprocessed input
    preprocessed_input = user_input.lower()  # For demonstration purposes
    return preprocessed_input

def determine_intent(preprocessed_input):
    # Implement intent detection logic based on preprocessed input
    # You can use natural language processing techniques or a library like spaCy
    # Return the detected intent
    intent = "symptoms"  # For demonstration purposes
    return intent

def retrieve_symptom_information(preprocessed_input):
    # Implement logic to retrieve information about symptoms
    # You can query a database or use other data sources
    # Return the symptom information
    symptom_info = "Here's some information about the symptoms..."  # For demonstration purposes
    return symptom_info

def retrieve_diagnosis_information(preprocessed_input):
    # Implement logic to retrieve diagnosis information
    # You can query a database or use other data sources
    # Return the diagnosis information
    diagnosis_info = "Here's some information about the diagnosis..."  # For demonstration purposes
    return diagnosis_info
def process_health_issue(user_input):
    # Preprocess input (You can implement this function)
    preprocessed_input = preprocess_input(user_input)

    # Determine user intent (You can implement this function)
    intent = determine_intent(preprocessed_input)

    if intent == "symptoms":
        # Retrieve information about symptoms (You can implement this function)
        response = retrieve_symptom_information(preprocessed_input)
    elif intent == "diagnosis":
        # Retrieve diagnosis information (You can implement this function)
        response = retrieve_diagnosis_information(preprocessed_input)
    elif intent == "medication":
        # Determine medication based on user input (You can implement this function)

        medication = determine_medication(preprocessed_input)
        response = f"The suggested medication for {user_input} is {medication}."
    else:
        response = "I'm sorry, I couldn't understand your request."

    return response
def determine_medication(preprocessed_input):
    # Implement logic to determine medication based on user input
    # You can use rules, databases, or external APIs to fetch medication data
    # For this example, let's assume a simple dictionary to map user input to medications
    medication_data = {
        "headache": "Aspirin",
        "fever": "Paracetamol",
        # Add more mappings...
    }

    # Default medication if not found in the dictionary
    default_medication = "Unknown"

    # Look up medication based on the preprocessed input
    medication = medication_data.get(preprocessed_input, default_medication)

    return medication

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']

    # Store user input in the database
    cursor.execute('INSERT INTO chat_history (user_input, response) VALUES (?, ?)', (user_input, ''))
    conn.commit()

    intent, entities = analyze_input(user_input) # type: ignore

    if intent == "medication":
        response = process_health_issue(user_input)
    else:
        response = generate_response(intent, entities)

    cursor.execute('UPDATE chat_history SET response = ? WHERE user_input = ?', (response, user_input))
    conn.commit()

    return response
def analyze_input(user_input):
    # Implement advanced NLP techniques to analyze intent, entities, and sentiment
    # You can use spaCy for entity recognition and NLTK or another library for sentiment analysis
    # For now, let's simulate values

    if "creator" in user_input.lower():
        intent = "creator_info"
    else:
        intent = "ask_about_condition"

    entities = []  # No specific entities for this intent
    sentiment = "neutral"  # Placeholder
    return intent, entities, sentiment

def generate_response(intent, entities):
    if intent == "ask_about_condition":
        #logic to fetch related medicines from your database
        related_medicines = fetch_related_medicine(entities)
        if related_medicines:
            response = "Based on your question, here are some related medicines:\n"
            response += "\n".join(related_medicines)
        else:
            response = "Sorry, I couldn't find specific medicines for this health issue. Please call the health line at 0548211310 or contact Jobel Teaching Hospital for personal health assistance at 0548211310."
        return response

    # "Who is your creator?" intent
    if intent == "creator_info":
        return "I was created by Professor Dr. Joseph Nhyira K. Mensah from Jobel Teaching Hospital together with Omega software engineering company ltd. founded by Professor Prince Mawuko(CEO) and Professor Jseph Nhyira K. Mensah(M.D.) to provide information and assistance related to health and medical topics. If you have any health-related questions, feel free to ask, and I'll do my best to assist you."

    return "A generic response for other intents goes here."

def fetch_related_medicine(entities):
    # Implement logic to search your database for related medicines based on the health issue entities
    # You can use entities to search for relevant medicines in your database

    # For demonstration purposes, let's assume a simple database structure
    # with health issues and their related medicines
    medicine_database = {
        "type 1 diabetes": ["Insulin", "Humulin R U-100", "Novolin R FlexPen", "insulin lispro protamine/insulin lispro 75/25", "", ""],
         "type 2 diabetes":["Metformin", "Sulfonylureas", "Glitazones", "Gliptins (dipeptidyl peptidase-4 inhibitors)", "Gliflozins (SGLT2 inhibitors)", "Glinides"],
        "hypertension": ["", ""],
        "headache": ["paracetamol", "ibuprofen", "Aspirin" "naproxen sodium"],
        "influenza": ["Tamiflu", "Xofluza", "LAIV or nasal spray, CDC and ACIP for pregnant woman"],
        "allergy": ["Is better to seek Doctor for solution or other mean from doctor","Benadryl",  "Claritin", ""],
        "asthma": ["Medicine A", "Medicine T"],
        "arthritis": ["Medicine Q", "Medicine R"],
        "back pain": ["Medicine K", "Medicine L"],
        "common cold": ["Medicine U", "Medicine V"]
    }

    related_medicines = medicine_database.get(entities[0].lower())

    if related_medicines:
        # If related medicines are found, add the caution message to each medicine
        caution_message = "Please consult Professor Dr. Joseph Nhyira K. Mensah for further medical laboratory guidance or ask for guidelines for taking the medicine from Jobel Teaching Hospital."
        cautioned_medicines = [medicine + " (" + caution_message + ")" for medicine in related_medicines]
        return cautioned_medicines
    else:
        # If no related medicines are found, provide a more professional and empathetic message
        return [
            "I regret to inform you that I couldn't find specific medicines for your current health issue. For immediate assistance, please contact the health line at 0548211310, or consider reaching out to Jobel Teaching Hospital for personalized health guidance.",
            "It is advisable to consult with Professor Dr. Joseph Nhyira K. Mensah for comprehensive medical laboratory tests and further professional advice."
        ]
        

if __name__ == '__main__':
    app.run(debug=True)

 

