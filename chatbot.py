import tkinter as tk
import json
from datetime import datetime
from PIL import Image, ImageTk

# Load responses from JSON file
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

with open(resource_path("responses.json"), "r") as file:
    responses = json.load(file)

# Create window
window = tk.Tk()

logo = Image.open(resource_path("logo.jpeg"))
logo = logo.resize((70,70))

logo_img = ImageTk.PhotoImage(logo)

logo_label = tk.Label(window, image=logo_img)
logo_label.pack(pady=5)

window.title("College Enquiry Chatbot")
window.geometry("800x500")
window.config(bg="#1e1e1e")

BUTTON_BG = "#0d6efd"
BUTTON_FG = "white"

BUTTON_FONT = ("Arial", 10, "bold")

# Heading
heading = tk.Label(
window,
text="🎓 College Enquiry Chatbot",
font=("Arial",14,"bold"),
bg="#1e1e1e",
fg="white"
)
heading.pack(pady=10)

# Chat area
chat_frame = tk.Frame(
    window,
    width=600,
    height=250,
    bg="#1e1e1e"
)
chat_frame.pack(pady=10)

chat_frame.pack_propagate(False)  # IMPORTANT (size fix pannum)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")

chat_area = tk.Text(
chat_frame,
yscrollcommand=scrollbar.set,
wrap="word",
bg="#2d2d2d",
fg="white",
insertbackground="white"
)
chat_area.pack(side="left", fill="both", expand=True)

scrollbar.config(command=chat_area.yview)

chat_area.insert(tk.END,
"🎓 Welcome to College Enquiry Chatbot!\n")
chat_area.insert(tk.END,
"📌 Ask about Fees, Courses, Admission, Placement...\n\n")

# Input box
user_input = tk.Entry(
    window,
    width=50,
    font=("Arial", 12),
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)
user_input.pack(pady=5)

user_input.bind("<Return>", lambda event: send_message())

# Send function
def faq_response(question):
    user_input.delete(0, tk.END)
    user_input.insert(0, question)
    send_message()
    
def send_message():
    message = user_input.get().lower().strip()

    if message == "":
        return

    time = datetime.now().strftime("%H:%M")

    chat_area.insert(tk.END, f"[{time}] You: {message}\n")

    if message in responses:
        reply = responses[message]
    else:
        reply = (
            "Sorry, I couldn't understand your query.\n"
            "Please ask about:\n"
            "• Fees\n"
            "• Admission\n"
            "• Hostel\n"
            "• Placement\n"
            "• Courses"
        )

    chat_area.insert(tk.END, f"[{time}] Bot: {reply}\n\n")

    chat_area.see(tk.END)

    user_input.delete(0, tk.END)

def clear_chat():
    chat_area.delete("1.0", tk.END)

    chat_area.insert(tk.END,
    "🎓 Welcome to College Enquiry Chatbot!\n")

    chat_area.insert(tk.END,
    "📌 Ask about Fees, Courses...\n\n")

# Send button
send_button = tk.Button(
    window,
    text="Send",
    command=send_message,
    bg="#0d6efd",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
    relief="flat",
    cursor="hand2"
)
send_button.pack(pady=10)

faq_frame = tk.Frame(
window,
bg="#1e1e1e"
)
faq_frame.pack(pady=5)

buttons = [
    ("Fees", "fees"),
    ("Admission", "admission"),
    ("Hostel", "hostel"),
    ("Placement", "placement"),
    ("About", "about"),
    ("Principal", "principal"),
    ("Facilities", "facilities"),
    ("Contact", "contact"),
    ("Courses", "courses"),
    ("Timing", "timing"),
    ("Placement Info", "placement_info")
]

for i, (text, query) in enumerate(buttons):

    row = i // 6
    col = i % 6

    tk.Button(
        faq_frame,
        text=text,
        command=lambda q=query: faq_response(q),
        bg="#0d6efd",
        fg="white",
        font=("Arial", 8, "bold"),
        width=10,
        height=1,
        relief="flat"
    ).grid(
        row=row,
        column=col,
        padx=5,
        pady=5
    )

clear_button = tk.Button(
    window,
    text="Clear Chat",
    command=clear_chat,
    bg="#dc3545",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12,
    relief="flat",
    cursor="hand2"
)
clear_button.pack()

exit_button = tk.Button(
    window,
    text="Exit",
    command=window.destroy,
    bg="#000000",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12,
    relief="flat",
    cursor="hand2"
)

exit_button.pack()

window.bind("<Return>", lambda event: send_message())

window.mainloop()