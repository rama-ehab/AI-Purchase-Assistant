# 🚀 Tips Hindawi Internship (August–October 2026)

> 🎓 This project was built during the **Tips Hindawi Internship (August–October 2026)**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Rama Ehab Ahmed                      |
| Project Name     | AI Purchase Assistant                |
| GitHub Username  | rama-ehab                            |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | **Edrak for AI**                     |

---

# 📖 Project Overview

**AI Purchase Assistant** is an AI-powered laptop recommendation system that helps users choose the most suitable laptop based on their requirements.

The user provides their laptop needs, such as budget, usage, minimum RAM, and preferred features, along with product URLs. The system scrapes product information, extracts the user's requirements using an LLM, retrieves relevant product information using RAG, evaluates the available products, and recommends the most suitable option.

The project uses **Qwen3-4B** for natural-language requirement extraction and **ChromaDB with sentence-transformer embeddings** for product retrieval.

---

# ✨ Features

* 📝 Extracts laptop requirements from natural-language user input.
* 🛒 Scrapes product information directly from provided product URLs.
* 🔎 Uses RAG with ChromaDB and embeddings to retrieve product information.
* 🤖 Uses Qwen3-4B for requirement extraction.
* 📊 Evaluates products based on budget, RAM, usage, and priorities.
* 🏆 Selects and recommends the most suitable laptop.
* 📋 Provides a product comparison through the Streamlit interface.
* 🌐 Uses FastAPI as the backend and Streamlit as the frontend.

---

# 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **FastAPI**
* **LangChain**
* **Qwen3-4B**
* **Hugging Face Transformers**
* **Hugging Face Sentence Transformers**
* **ChromaDB**
* **Pydantic**
* **BeautifulSoup**
* **Requests**
* **PyTorch**
* **ngrok**
* **Kaggle**

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/rama-ehab/AI-Purchase-Assistant.git
cd AI-Purchase-Assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Backend

The Qwen3-4B model requires GPU resources, so the backend is designed to run on **Kaggle**.

The Kaggle setup and execution steps are available in:

```text
kaggle-backend-setup.ipynb
```

The notebook starts the FastAPI backend and exposes it through ngrok.

### Frontend

After starting the backend, update the API URL in `app.py` with the current ngrok URL and run:

```bash
streamlit run app.py
```

---

# 🚀 Usage

1. Start the backend on Kaggle using the provided notebook.
2. Copy the generated ngrok public URL.
3. Set the API URL in `app.py`.
4. Run the Streamlit application.
5. Enter your laptop requirements.
6. Provide the URLs of the laptops you want to compare.
7. Click **Recommend**.
8. The system analyzes the products and displays the recommended laptop.
9. Use the comparison section to compare the available products.

Example requirement:

```text
I need a laptop under 50000 EGP for programming and gaming,
with at least 16GB RAM and a good GPU.
```

---

# 📸 Demo

Add screenshots or a demo video of the Streamlit application here.

Recommended screenshots:

* Main application interface
* User requirements and product URLs
* Recommended laptop result
* Product comparison section

---

# 📈 Results

The project successfully implements an end-to-end AI-powered product recommendation workflow:

* Natural-language requirements are extracted using **Qwen3-4B**.
* Product data is collected from real product pages.
* Product information is stored and retrieved using **ChromaDB and embeddings**.
* Products are evaluated against the user's requirements.
* A suitable product is selected and presented through a **Streamlit interface**.
* The FastAPI backend successfully runs on a GPU-enabled Kaggle environment and communicates with the local Streamlit application through ngrok.

---

# 🔮 Future Improvements

* Support more product categories beyond laptops.
* Improve product ranking using more advanced recommendation logic.
* Add support for more e-commerce websites.
* Add price-history tracking and price alerts.
* Improve the recommendation explanation using an LLM.
* Deploy the backend and frontend to a permanent cloud environment.

---

# 📚 About the Internship

This project was developed as part of the **Tips Hindawi Internship (August–October 2026)**.

Tips Hindawi is the internships department of **Edrak for AI**. The internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

The project was developed as part of the **Large Language Models (LLMs) Program**, applying concepts such as **RAG, embeddings, LangChain, output parsing, LLMs, FastAPI, and Streamlit** in a practical application.

For more information about the internship, training programs, and upcoming batches, visit the official Tips Hindawi website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
