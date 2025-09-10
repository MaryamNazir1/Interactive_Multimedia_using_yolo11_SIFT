# 🖼️ Interactive Multimedia using YOLOv11 + SIFT

This project demonstrates an **interactive multimedia system** that allows users to click on objects (bags, dresses, and shoes) in a video to retrieve **product details** such as name, price, and related images from a **MongoDB database**.

It combines **YOLOv11 (for object detection)** and **SIFT (for image similarity matching)** to provide an intelligent search and retrieval system.

---

## 🚀 Features

- Train a YOLOv11 model on a custom dataset of **bags, dresses, and shoes**.
- Detect these objects in video frames in real time.
- Click on any detected object to:
  - Identify the closest bounding box.
  - Retrieve related product records from MongoDB.
  - Match the cropped object with stored dataset images using **SIFT feature matching**.
  - Display product **name, price, and multiple images** to the user.
- Built with **Streamlit** for an interactive user interface.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **YOLOv11 (Ultralytics)** – Object detection
- **OpenCV (SIFT, BFMatcher)** – Image feature matching
- **MongoDB (Atlas)** – Product database
- **Streamlit** – Web-based interactive dashboard

---

## 📂 Project Structure

Interactive_Multimedia_using_yolo11_SIFT/
│── db/ # Product images (bags, dresses, shoes)
│── src/ # Source code files
│── best.pt # Trained YOLOv11 model weights
│── app.py # Main Streamlit application
│── requirements.txt # Python dependencies
│── README.md # Documentation

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Interactive_Multimedia_using_yolo11_SIFT.git
   cd Interactive_Multimedia_using_yolo11_SIFT
   ```
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place your trained YOLO model (best.pt) inside the project root.

5. Add product images to the db/ folder and make sure MongoDB is populated with product metadata:

```bash
{
  "Dresses": [
    {
      "name": "Red Dress",
      "price": "$50",
      "images": ["d1_1.jpg", "d1_2.jpg", "d1_3.jpg"]
    }
  ],
  "Shoes": [
    {
      "name": "Nike Sneakers",
      "price": "$80",
      "images": ["s1_1.jpg", "s1_2.jpg"]
    }
  ]
}
```

6. Running the App

```bash

streamlit run app.py

```
