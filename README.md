# Zabiverse

# Zabiverse

**Zabiverse** is your all-in-one smart campus companion: a React front-end & Flask back-end application that lets students and faculty:

- **Chat with an AI assistant** powered by a FAISS-indexed vector database and Google Gemini  
- **Log in via facial recognition** (non-student users)  
- **Speak and listen** to bot replies with built-in text-to-speech

---

## 🔍 Features

- **Conversational QA**  
  – Ask questions in natural language, backed by FAISS vector search over your documents  
  – Responses generated via Google’s Gemini API  
- **Facial Recognition Login**  
  – Faculty/Management can log in by scanning their face  
  – Powered by the `face_recognition` Python library + OpenCV  
- **Text-to-Speech**  
  – Browser-based TTS reads AI replies out loud with the Web Speech API  
- **Role-based Flow**  
  – Students log in with username/password  
  – Faculty and higher roles use camera login  
- **React UI**  
  – Clean, responsive interface built with React & Tailwind CSS (or custom CSS)  
- **Flask API**  
  – `/api/query` for chat  
  – `/api/login` for credentials  
  – `/api/facial-recognition` for face login  

---

## 🛠️ Tech Stack

- **Front-end**  
  – React, React Hooks, `react-webcam`, `axios`  
  – Web Speech API for TTS  
- **Back-end**  
  – Python 3.8+, Flask, Flask-CORS  
  – FAISS (vector index), `sentence-transformers`  
  – Google Generative AI (`google-generativeai`)  
  – `face_recognition`, OpenCV, NumPy  
- **Dev Tools**  
  – Node.js & npm  
  – pip & virtualenv  

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Zabiverse.git
cd Zabiverse
```

### 2. Back-end Setup

1. Create and activate a Python virtual environment:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   - Copy `.env.example` to `.env`
   - Set your Gemini API key:
     ```env
     GEMINI_API_KEY=your_google_gemini_api_key
     ```

4. Prepare your vector index & metadata:

   ```bash
   # ensure these files exist:
   backend/final_vector_database.index
   backend/final_vector_metadata.json
   ```

5. Populate your face library:

   ```bash
   mkdir -p backend/model/Faculty_images
   # copy JPEG/PNG images of authorized faculty into that folder
   ```

6. Run the Flask server:

   ```bash
   flask run
   # or
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000/`.

### 3. Front-end Setup

1. In a new terminal, install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the React development server:

   ```bash
   npm start
   ```

   Your UI will open at `http://localhost:3000/`.

---

## 📂 Project Structure

```
Zabiverse/
├── backend/
│   ├── app.py
│   ├── model/
│   │   ├── model.py
│   │   ├── face_recognition_utils.py
│   │   ├── Faculty_images/      # put faculty .jpeg/.png here
│   │   └── __init__.py
│   ├── final_vector_database.index
│   ├── final_vector_metadata.json
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.js
    │   ├── index.js
    │   └── app.css
    ├── package.json
    └── public/
```

---

## 🎯 Usage

1. **Select your user type** on the landing page.  
2. **Faculty/Staff**: grant camera access → click **Start Recognition** → proceed on success.  
3. **Student**: enter username & password → click **Login**.  
4. **Chat Interface**: type questions in the input, hit **Send**. Zabiverse will reply and read the answer aloud.

---

## 🤝 Contributing

1. Fork this repo  
2. Create a feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -m "Add your feature"`)  
4. Push to the branch (`git push origin feature/YourFeature`)  
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Happy coding! 🚀  
```
