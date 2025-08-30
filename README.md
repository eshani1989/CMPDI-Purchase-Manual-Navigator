# CMPDI – Purchase Manual Navigator 🛠️📖

An **AI-powered desktop knowledge base** developed during my internship at **Central Mine Planning & Design Institute (CMPDI)**.  
The application helps users navigate the Purchase Manual efficiently with chapters, sub-chapters, questions, and answers.  
It also supports opening relevant annexure PDFs directly from the interface.

---

## 🚀 Features
- 📘 Select **Chapters**, **Sub-Chapters**, and **Questions** from dropdowns.  
- 💡 Get **instant answers** with a smooth typing effect.  
- 🔗 **Clickable Annexure links** that open PDFs externally.  
- 🎨 **User-friendly GUI** built with Tkinter.  

---

## 🛠️ Tech Stack
- **Language:** Python  
- **Libraries:**  
  - `tkinter` (GUI framework – built into Python)  
  - `PIL` (Pillow – for handling images like the CMPDI logo)  
  - `json` (to load structured knowledge base)  
  - `os`, `threading`, `time` (for utility functions)  

---

## 📂 Project Structure

CMPDI-Purchase-Manual-Navigator/
│── final.py # Main application (Tkinter app)
│── questions.json # Knowledge base (Q&A in JSON format)
│── cmpdil_logo.png # CMPDI logo (used in the header)
│── Annexure 2.pdf # Sample annexure file
│── Annexure 4.pdf
│── Annexure 12.pdf
│── Annexure 14.pdf
│── Annexure 28.pdf
│── Annexure 29.pdf
│── Annexure 37.pdf
│── README.md # Project documentation
│── requirements.txt # Python dependencies




---

## ⚙️ Installation & Usage
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/CMPDI-Purchase-Manual-Navigator.git
   cd CMPDI-Purchase-Manual-Navigator

*Install dependencies

pip install -r requirements.txt

*Run the application

python final.py

🎯 Future Enhancements

Add NLP-based query understanding.

Enable full-text search across all chapters.

Deploy as a web app for easier access.

👩‍💻 Author

Eshani Ranjan
📍 Ranchi, Jharkhand
📧 eshaniranjan2303@gmail.com

🔗 LinkedIn: linkedin.com/in/eshani-ranjan-750169260 
