import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import threading
import time
import os  # For opening PDFs

# Load structured Q&A data
with open("questions.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Organize data: chapter → sub_chapter → question → answer
data = {}
for entry in raw_data:
    chapter = entry["chapter"]
    sub_chapter = entry["sub_chapter"]
    if chapter not in data:
        data[chapter] = {}
    if sub_chapter not in data[chapter]:
        data[chapter][sub_chapter] = {}
    for q in entry["questions"]:
        data[chapter][sub_chapter][q["question"]] = q["answer"]

# --- Annexure links map ---
annexure_links = {
    "Annexure-2": "Annexure 2.pdf",
    "Annexure-4": "Annexure 4.pdf",
    "Annexure-12": "Annexure 12.pdf",
    "Annexure-14": "Annexure 14.pdf",
    "Annexure-28": "Annexure 28.pdf",
    "Annexure-29": "Annexure 29.pdf",
    "Annexure-37": "Annexure 37.pdf",
}

# --- Window Setup ---
root = tk.Tk()
root.title("CMPDIL – Purchase Manual Navigator")
root.geometry("1100x750")
root.configure(bg="#f4f6f9")

# --- Fonts ---
FONT_HEADER = ("Calibri", 22, "bold")
FONT_LABEL = ("Calibri", 16, "bold")
FONT_TEXT = ("Calibri", 14)

# --- Header ---
header = tk.Frame(root, bg="#002244", height=80)
header.pack(fill="x")

try:
    logo_img = Image.open("cmpdil_logo.png").resize((60, 60))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header, image=logo, bg="#002244")
    logo_label.image = logo
    logo_label.pack(side="left", padx=(20, 10), pady=10)
except Exception as e:
    print("⚠️ Logo not loaded:", e)

tk.Label(
    header,
    text="CMPDIL – Purchase Manual Navigator",
    font=FONT_HEADER,
    fg="white",
    bg="#002244"
).pack(side="left", pady=20)

# --- Content Area ---
content = tk.Frame(root, bg="#f4f6f9")
content.pack(fill="both", expand=True, padx=30, pady=(20, 10))

def add_dropdown(label, variable, row, width=60):
    tk.Label(content, text=label, font=FONT_LABEL, bg="#f4f6f9").grid(row=row, column=0, sticky="w", pady=5)
    box = ttk.Combobox(content, textvariable=variable, font=FONT_TEXT, state="readonly", width=width)
    box.grid(row=row, column=1, sticky="w", pady=5)
    return box

chapter_var = tk.StringVar()
chapter_dropdown = add_dropdown("📘 Select Chapter", chapter_var, row=0)
chapter_dropdown["values"] = list(data.keys())

subchapter_var = tk.StringVar()
subchapter_dropdown = add_dropdown("📂 Select Sub-Chapter", subchapter_var, row=1)

question_var = tk.StringVar()
question_dropdown = add_dropdown("❓ Select Question", question_var, row=2, width=80)

tk.Button(
    content, text="🔄 Reset", font=FONT_TEXT, command=lambda: reset_fields(),
    bg="#dbe9ff", relief="groove", width=20
).grid(row=3, column=1, sticky="w", pady=10)

tk.Label(root, text="Answer", font=FONT_LABEL, bg="#f4f6f9").pack(anchor="w", padx=30, pady=(5, 5))

answer_frame = tk.Frame(root, bg="#f4f6f9")
answer_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

scrollbar = tk.Scrollbar(answer_frame)
scrollbar.pack(side="right", fill="y")

answer_text = tk.Text(
    answer_frame, wrap="word", font=FONT_TEXT,
    yscrollcommand=scrollbar.set, bg="white",
    bd=1, relief="solid", padx=12, pady=12
)
answer_text.pack(fill="both", expand=True)
scrollbar.config(command=answer_text.yview)
answer_text.config(state="disabled")

# --- Open Annexure Externally ---
def open_annexure_pdf(annexure_name):
    filepath = annexure_links.get(annexure_name)
    if filepath and os.path.exists(filepath):
        os.startfile(filepath)
    else:
        print(f"❌ PDF for '{annexure_name}' not found.")

# --- Typing Answer Function with Clickable Annexures ---
def type_answer(text):
    answer_text.config(state="normal")
    answer_text.delete("1.0", tk.END)

    idx = 0
    while idx < len(text):
        matched = False
        for keyword in annexure_links:
            if text[idx:].startswith(keyword):
                end_idx = idx + len(keyword)
                tag = keyword.replace("-", "_")

                answer_text.insert(tk.END, keyword)
                answer_text.tag_add(tag, f"1.0+{idx}c", f"1.0+{end_idx}c")
                answer_text.tag_config(tag, foreground="blue", underline=True)
                answer_text.tag_bind(tag, "<Button-1>", lambda e, k=keyword: open_annexure_pdf(k))
                answer_text.tag_bind(tag, "<Enter>", lambda e: answer_text.config(cursor="hand2"))
                answer_text.tag_bind(tag, "<Leave>", lambda e: answer_text.config(cursor=""))
                idx = end_idx
                matched = True
                break
        if not matched:
            answer_text.insert(tk.END, text[idx])
            idx += 1

        answer_text.see(tk.END)
        root.update_idletasks()
        time.sleep(0.003)

    answer_text.config(state="disabled")

def show_answer_threaded():
    chapter = chapter_var.get()
    subchapter = subchapter_var.get()
    question = question_var.get()
    if chapter and subchapter and question:
        answer = data[chapter][subchapter].get(question, "Answer not found.")
        threading.Thread(target=type_answer, args=(answer,), daemon=True).start()

# --- Dropdown Handlers ---
def update_subchapters(event=None):
    chapter = chapter_var.get()
    if chapter:
        subchapter_dropdown["values"] = list(data[chapter].keys())
        subchapter_var.set("")
        question_dropdown["values"] = []
        question_var.set("")
        show_message("🛈 Please select a sub-chapter.")

def update_questions(event=None):
    chapter = chapter_var.get()
    subchapter = subchapter_var.get()
    if chapter and subchapter:
        question_dropdown["values"] = list(data[chapter][subchapter].keys())
        question_var.set("")
        show_message("🛈 Please select a question.")

def show_message(msg):
    answer_text.config(state="normal")
    answer_text.delete("1.0", tk.END)
    answer_text.insert(tk.END, msg)
    answer_text.config(state="disabled")

def reset_fields():
    chapter_var.set("")
    subchapter_var.set("")
    question_var.set("")
    subchapter_dropdown["values"] = []
    question_dropdown["values"] = []
    show_message("🛈 Start by selecting a chapter.")

# --- Bind Dropdowns ---
chapter_dropdown.bind("<<ComboboxSelected>>", update_subchapters)
subchapter_dropdown.bind("<<ComboboxSelected>>", update_questions)
question_dropdown.bind("<<ComboboxSelected>>", lambda e: show_answer_threaded())

# --- Run App ---
reset_fields()
root.mainloop()
