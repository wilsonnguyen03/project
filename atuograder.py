import ipywidgets as widgets
from tkinter import messagebox
from tkinter import filedialog
from customtkinter import *
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt
import pytesseract
import easyocr
import os
from PIL import Image
from groq import Groq
from paddleocr import PaddleOCR, draw_ocr

# Create the main window
root = CTk()
root.title("AutoGrader")

# Get the dimensions of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the dimensions of the window
window_width = 1200
window_height = 800

# Calculate the position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window geometry to center it
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


def update_image(file_path):
    img = Image.open(file_path)
    # Resize the image
    img = img.resize((600, 400))  # Adjust width and height as needed
    img_tk = ImageTk.PhotoImage(img)
    label.configure(image=img_tk, text="")
    label.place(relx =0.275, rely = 0.55, anchor ="center")
    label.image = img_tk  # Keep reference to avoid garbage collection


    image = cv2.imread(file_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    # Extract text
    extracted_text1 = pytesseract.image_to_string(image)
    #print("Extracted Text 1:\n", extracted_text1)

    # Initialize the OCR reader
    reader = easyocr.Reader(["en"])  # "en" for English
    # Perform OCR
    results = reader.readtext(image)
    # Extract and print only the text
    extracted_text2 = [text for (_, text, _) in results]
    #print("Extracted Text 2:\n", " ".join(extracted_text2))


    ocr = PaddleOCR(use_angle_cls=False, lang='en')
    image = cv2.imread("1.jpg")
    # Perform OCR (text detection and recognition)
    result = ocr.ocr(image, cls=True)
    # Extract text from OCR result
    text = ''
    for line in result[0]:
        text += line[1][0] + '\n'
    # Print the extracted text
    #print("Extracted Text 3:\n", text)

    client = Groq(
    api_key="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",
)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"I have three handwriting recognition texts, 1: {extracted_text1}, 2: {extracted_text2} and 3:{text} . I want you to decypher these two text without changing its meaning or any words. Keep its originality. These two text are hand writing recognition from the same text so I want you to only output the outcome only nothing else, no extra prompts and only output it once",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    #print(chat_completion.choices[0].message.content)
    # Create a frame for the text box
    text_frame = CTkFrame(root, width=600, height=400)
    text_frame.place(relx=0.75, rely=0.55, anchor="center")  # Adjust position

    love_label = CTkLabel(master = text_frame, text=chat_completion.choices[0].message.content, text_color = "#FFFFFF", wraplength=350)
    love_label.pack(expand=True, padx=10, pady=10)   # Adjust position as needed

def upload_file():
    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        # If a file is selected, show the file path
        print(f"File selected: {file_path}")
        # You can process the file here (e.g., open the file, read data, etc.)
        btn.place_forget()
        update_image(file_path)

label = CTkLabel(master =root, text = "No File has been chosen")
label.place(relx =0.5, rely = 0.55, anchor ="center")

btn = CTkButton(master = root, width = 200, height = 50 ,text ="Upload Empty Worksheet", corner_radius=40, fg_color = "#0080FE", hover_color= "#FFFFFF", text_color ="#000000", command=upload_file)
btn.place(relx =0.5, rely = 0.5, anchor ="center")

root.mainloop()