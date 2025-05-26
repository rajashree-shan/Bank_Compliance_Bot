# 🛡️ Clara: Your AI Compliance Companion for Banks

**Clara the Compliance Bot** is a secure, MPC-enhanced chatbot designed for financial institutions to query encrypted audit logs, policies, and regulatory documents using natural language.

![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-orange?logo=streamlit)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Features

- 🔐 Query encrypted audit logs & policies securely
- 🧠 Uses LangChain + OpenAI for accurate retrieval
- ☁️ Loads documents from AWS S3
- ⚙️ Built with Streamlit for a responsive UI
- 🛡️ MPC-secured query flow for privacy

---

## 🧩 Project Structure

```
├── app.py                    # Streamlit frontend
├── config.py                 # Keys and config values
├── utils/
│   ├── s3_loader.py          # AWS S3 document loading
│   ├── retriever.py          # LangChain retriever builder
│   ├── encryptor.py          # Dummy encryption layer
│   └── mpc_layer.py          # MPC-secured processing
├── data/                     # Local FAISS vectorstore
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 Setup

1. **Clone the Repo**

```bash
git clone https://github.com/rajashree-shan/Bank_Compliance_Bot.git
cd compliance-bot
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Environment Variables**

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

---

## 💻 Run Locally

```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push the project to GitHub.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and link your GitHub repo.
3. Add your environment variables securely in the **Secrets Manager**.
4. Click **Deploy**!

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](./LICENSE) for details.
