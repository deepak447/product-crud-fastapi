# 🚀 FastAPI Product Management API with File Upload & API Key Security

This project is a **FastAPI-based RESTful API** for product management that allows users to:
- 🔐 Access API endpoints securely via **API key**
- 📦 Perform **CRUD operations** on product data stored in a JSON file
- 🖼️ Upload multiple files (like product images)
- 💾 Save uploaded files to a local directory

---

## 📦 Features

- ✅ Add, update, delete, and retrieve products
- 🔐 API key security using headers (`X-API-Key`)
- 📂 File upload functionality with support for multiple files
- 💡 Data persistence via `product.json`
- 🔄 Full and partial updates using `PUT` and `PATCH`
- 🧪 Built-in Swagger UI at `/docs`

---

## 📁 Project Structure

  ├── Upload_picture/ # Directory for uploaded images
  ├── product.json # Stores product data in JSON format
  ├── .env # Stores sensitive environment variables like API_KEY
  ├── test2.py # Main FastAPI application
  └── README.md # Project documentation

---

## 🔐 API Security

All endpoints are protected using an **API key** mechanism via a request header:
```http
X-API-Key: your_api_key_here
```

1. **Install dependencies**
   ```pip install -r requirements.txt```
