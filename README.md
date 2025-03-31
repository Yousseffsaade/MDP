
# Smart Flood Detection & Alert System - Backend

## 🚀 Project Overview

This project is a backend system for a Flood Detection & Alert System. It integrates real-time sensor data and weather forecasts to store, process, and display flood risk information.

---

## ✅ Progress Summary

### 1. Cloud Storage Setup (Azure)

- Created an **Azure Storage Account**: `smartfloodstorage`
- Created a **Blob Container**: `sensor-data`
- Uploaded sensor data files to the container

### 2. Weather API Integration

- Integrated the **OpenWeather API** in the backend
-  Automated retrieval of:
  - Temperature
  - Humidity
  - Rain Forecast
  - Wind Speed

### 3. Data Retrieval & Merging

- Developed a Python script **`fetch_data.py`** to:
  - Fetch Arduino data files from Azure Blob Storage
  - Retrieve weather forecast data via API
  - Merge both datasets
  - Save the merged data to `data/final_data.json`

### 4. Database Setup (MongoDB Atlas)

- Created a **MongoDB Atlas Cluster**
- Created a **Database**: `smart_flood_system`
- Created a **Collection**: `sensor_data`
- Configured secure connection and access

### 5. Data Insertion to MongoDB

- Developed Python script **`insert_to_db.py`** to:
  - Connect to MongoDB Atlas
  - Load data from `data/final_data.json`
  - Insert data into `sensor_data` collection

### 6. API Backend Development (Flask)

- Developed Flask API in **`app.py`**
- Implemented route:
  - `/api/data`: Fetches and returns all sensor & weather data from MongoDB
- Tested locally on: `http://127.0.0.1:5000/api/data`

---

## 📄 Project Structure

```
backend/
├── data/
│   └── final_data.json         # Merged sensor + weather data
├── fetch_data.py               # Data retrieval & merging
├── insert_to_db.py             # Insert data into MongoDB
├── app.py                      # Flask API server
└── venv/                       # Python virtual environment
```

---

## 🚧 Next Possible Steps

- Add a **Machine Learning model** to predict flood risk
- Connect the API to a **Mobile or Web Application**
- Add **Alert System** (Email / SMS)
- Automate data fetching & insertion periodically

---

## 🔗 Useful Links

- [Azure Portal](https://portal.azure.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [OpenWeather API](https://openweathermap.org/api)

---

**This backend is now fully operational for sensor data retrieval, weather integration, and storage in MongoDB.**
