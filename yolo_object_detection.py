import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
import shutil


# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("hello valliappan")
    speak("I am Friday, your personal assistant.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query
def create_database():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS database (
                        id INTEGER PRIMARY KEY,
                        class_id TEXT,
                        time TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(class_id, time):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO database (class_id, time) VALUES (?, ?)", (class_id, time))
    conn.commit()
    conn.close()
create_database()

def fetch_data_from_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM database")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def create_pdf(data):
    # Create a PDF document
    pdf_filename = "data_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    # Define the table structure
    table_data = [['S No', 'Class ID', 'Time']]
    for row in data:
        table_data.append(list(row))

    # Create the table
    table = Table(table_data, colWidths=[1 * inch, 1 * inch, 2 * inch])

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    print(f"PDF report generated: {pdf_filename}")
def send_emergency_message(message):
    sender_email = "vvalliappan2004@gmail.com"
    sender_password = "qksg sulw izbh jzzv"
    receiver_email = "manodharshan.k@gmail.com"

    subject = "Emergency Alert!"
    body = message

    message1 = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message1)
    server.quit()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'open yolo' in query:
            speak("Initiating object detection protocol")
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)

            def speak(audio):
                engine.say(audio)
                engine.runAndWait()

            def command():
                r = sr.Recognizer()
                speak('tell me access code to run')
                with sr.Microphone() as source:
                    print("Listening...")
                    r.pause_threshold = 1
                    audio = r.listen(source)

                try:
                    print("Recognizing...")
                    query = r.recognize_google(audio, language='en-in')
                    print(f"User said: {query}\n")

                except Exception as e:
                    print("Say that again please...")
                    return "None"
                return query

            if __name__ == "__main__":
                query = command().lower()
                if 'spider' in query:
                    import cv2
                    import pyttsx3
                    import numpy as np
                    speak('Access code accepted')
                    engine = pyttsx3.init('sapi5')
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id)


                    # Load the pre-trained YOLOv3 model
                    net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

                    # Load the class names
                    classes = []
                    with open('coco.names', 'r') as f:
                        classes = [line.strip() for line in f.readlines()]

                    # Initialize the text-to-speech engine
                    engine = pyttsx3.init()

                    # Start capturing video from the webcam
                    cap = cv2.VideoCapture(0)

                    while True:
                        # Read the current frame from the video stream
                        ret, frame = cap.read()

                        # Check if the frame is None (i.e., if the frame was not read successfully)
                        if frame is None:
                            print("Failed to read frame from video stream")
                            break

                        # Perform object detection on the frame
                        height, width, channels = frame.shape
                        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                        net.setInput(blob)
                        outs = net.forward(net.getUnconnectedOutLayersNames())

                        # Get the bounding boxes, confidence scores, and class IDs
                        class_ids = []
                        confidences = []
                        boxes = []
                        for out in outs:
                            for detection in out:
                                scores = detection[5:]
                                class_id = np.argmax(scores)
                                confidence = scores[class_id]
                                if confidence > 0.5:
                                    center_x = int(detection[0] * width)
                                    center_y = int(detection[1] * height)
                                    w = int(detection[2] * width)
                                    h = int(detection[3] * height)
                                    x = int(center_x - w / 2)
                                    y = int(center_y - h / 2)
                                    class_ids.append(class_id)
                                    confidences.append(float(confidence))
                                    boxes.append([x, y, w, h])

                        # Apply non-maximum suppression to remove overlapping bounding boxes
                        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                        # Loop over the remaining bounding boxes after non-maximum suppression
                        for i in indices:
                            if i < len(class_ids):
                                box = boxes[i]
                                left, top, width, height = box
                                label = f'{classes[class_ids[i]]}: {confidences[i]:.2f}'
                                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                                insert_data(label,strTime)

                                # Convert the label to speech and speak it out
                                engine.say(label)
                                engine.runAndWait()

                                # Print the label and confidence score in text format
                                print(label)

                                # Draw the bounding box on the frame
                                cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)

                        # Display the resulting frame
                        cv2.imshow('Object Detection', frame)

                        # Break the loop if 'q' is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    # Release the video capture and close the windows
                    cap.release()
                    cv2.destroyAllWindows()
                else:
                    speak('Access code denied')
            speak("object detection closed")
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'play music' in query:
            music_dir = 'C:\\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'tell me the time now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        
        elif 'emergency' in query:
                send_emergency_message("Emergency!please help me")
                print("Emergency message sent.")

        elif 'switch off' in query:
            speak("Goodbye!")
             # Fetch data from the database
            data = fetch_data_from_database()
            def download_pdf():
                src_file = "data_report.pdf"
                dst_folder = "D:/blind database"  
                dst_file = f"{dst_folder}/data_report.pdf"
                shutil.copy(src_file, dst_file)
                print(f"PDF downloaded to {dst_file}")

            # Create a PDF document with the fetched data
            create_pdf(data)
            download_pdf()
            break