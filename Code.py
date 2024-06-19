import customtkinter as ctk
import tkinter as tk
import google.generativeai as genai
import threading
from datetime import datetime

# Replace with your actual API key
API_KEY = 'USE_YOUR_OWN_API_KEY' 

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("My Chatbot")
        self.geometry("500x450")

        # Chat area (Frame for holding messages)
        self.chat_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color="ivory2")
        self.chat_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # Date Label in the center of the chat area
        self.date_label = ctk.CTkLabel(self.chat_frame, text=self.get_current_date(), font=("Arial", 12))
        self.date_label.pack(pady=10)

        # Input field (Entry widget)
        self.input_field = ctk.CTkEntry(self, placeholder_text="Type your message...")
        self.input_field.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.input_field.bind("<Return>", self.send_message)

        # Send button (Button widget)
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(side="left", padx=10, pady=10)

        # Configure Generative AI
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-pro') #Replace with your model if you don't use gemini api
        self.chat = self.model.start_chat(history=[])

    def get_current_date(self):
        return datetime.now().strftime("%d/%m/%Y")

    def send_message(self, event=None):
        user_input = self.input_field.get()
        self.input_field.delete(0, tk.END)

        if user_input:
            self.append_message(user_input, "lightblue3", "e")
            typing_label = self.append_message("typing...", "lightgrey", "w", typing=True)
            threading.Thread(target=self.generate_chatbot_response, args=(user_input, typing_label)).start()

    def append_message(self, message, color, anchor, typing=False):
        frame = ctk.CTkFrame(self.chat_frame, fg_color=color, corner_radius=10)
        
        label = ctk.CTkLabel(frame, text=message, wraplength=380, anchor="w")
        label.pack(padx=5, pady=(5, 1))  # Reduce space between message and timestamp
        
        if not typing:
            timestamp = datetime.now().strftime("%H:%M")
            time_label = ctk.CTkLabel(frame, text=timestamp, font=("Arial", 8), text_color="gray")
            time_label.pack(padx=5, pady=(0, 5), anchor="e")  # Adjust padding values

        # Set alignment for the message frame
        if anchor == "e":
            frame.pack(anchor="e", pady=(5, 0), padx=(50, 10))  # User message
        else:
            frame.pack(anchor="w", pady=(5, 0), padx=(10, 50))  # Bot message

        self.chat_frame.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1)

        if typing:
            return label

    def generate_chatbot_response(self, user_input, typing_label):
        try:
            response = self.chat.send_message(user_input)
            chatbot_response = response.text
        except Exception as e:
            chatbot_response = f"Error: {str(e)}"

        self.after(1000, self.display_bot_response, chatbot_response, typing_label)

    def display_bot_response(self, response, typing_label):
        typing_label.master.destroy()  # Remove the typing label
        self.append_message(response, "lightgrey", "w")

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
