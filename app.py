import streamlit as st
import cv2
import numpy as np
from pymongo import MongoClient
from ultralytics import YOLO
from streamlit_image_coordinates import streamlit_image_coordinates

# Set Streamlit page layout and tab name
st.set_page_config(page_title="Multimedia", layout="wide")

# Demo Heading
st.title("Demo for Interactive Multimedia")


# Initialize MongoDB connection
@st.cache_resource
def init_mongo():
    client = MongoClient(
        "mongodb+srv://maryambhatti900:Hello123*@cluster0.hw8qz.mongodb.net/"
    )
    db = client["fashion_db"]
    return db["products"]


# Load YOLO model
@st.cache_resource
def load_yolo():
    return YOLO("best.pt")


# Initialize SIFT and Matcher
@st.cache_resource
def init_feature_matcher():
    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher()
    return sift, bf


# Retrieve closest object based on click
def get_closest_box(click_x, click_y, boxes, class_names):
    min_dist = float("inf")
    closest_box = None
    closest_label = None

    for box in boxes:
        x1, y1, x2, y2 = map(int, box[:4])
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        dist = (cx - click_x) ** 2 + (cy - click_y) ** 2

        if dist < min_dist:
            min_dist = dist
            closest_box = (x1, y1, x2, y2)
            closest_label = class_names[int(box[5].item())]

    return closest_box, closest_label


# Fetch images from MongoDB
def fetch_related_images(label):
    print(label)
    category_map = {"dress": "Dresses", "shoes": "Shoes", "bag": "Bags"}
    category = category_map.get(label.lower(), label)

    product_data = collection.find_one({category: {"$exists": True}}, {category: 1})
    if not product_data or category not in product_data:
        return []

    return [
        (product, [f"db/{img}" for img in product["images"]])
        for product in product_data[category]
    ]


# Find best matching image
def find_best_match(target_img, related_images):
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    kp_target, desc_target = sift.detectAndCompute(target_gray, None)

    best_match = None
    max_matches = 0

    for product, img_paths in related_images:
        total_matches = 0
        for path in img_paths:
            db_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if db_img is None:
                continue

            kp_db, desc_db = sift.detectAndCompute(db_img, None)
            if desc_target is None or desc_db is None:
                continue

            matches = bf.knnMatch(desc_target, desc_db, k=2)
            good = [m for m, n in matches if m.distance < 0.65 * n.distance]
            total_matches += len(good)

        if total_matches > max_matches:
            max_matches = total_matches
            best_match = product

    return best_match


# Initialize dependencies
collection = init_mongo()
yolo_model = load_yolo()
sift, bf = init_feature_matcher()

# Sidebar for video upload
with st.sidebar:
    st.header("Upload Video")
    uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi", "mov"])

    if uploaded_file:
        if "frames" not in st.session_state:
            st.session_state.frames = []
            with st.spinner("Processing video..."):
                cap = cv2.VideoCapture(uploaded_file.name)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    st.session_state.frames.append(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    )
                cap.release()

        if "current_frame" not in st.session_state:
            st.session_state.current_frame = 0

        st.session_state.current_frame = st.slider(
            "Select Frame",
            0,
            len(st.session_state.frames) - 1,
            st.session_state.current_frame,
        )

# Main layout with two columns
if "frames" in st.session_state and st.session_state.frames:
    col1, col2 = st.columns([3, 2])  # Adjust column width ratios

    with col1:
        st.subheader("Video Frame")
        frame = st.session_state.frames[st.session_state.current_frame]

        # Resize the frame before displaying
        frame_resized = cv2.resize(frame, (350, 550))  # Adjust dimensions as needed

        coordinates = streamlit_image_coordinates(
            frame_resized, key=f"frame_{st.session_state.current_frame}"
        )

    with col2:
        st.subheader("Retrieved Product Details")

        if coordinates:
            x, y = coordinates["x"], coordinates["y"]
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = yolo_model(frame_bgr)

            boxes = []
            class_names = results[0].names
            for result in results:
                boxes.extend(result.boxes.data)

            if boxes:
                closest_box, label = get_closest_box(x, y, boxes, class_names)
                if closest_box:
                    x1, y1, x2, y2 = closest_box
                    cropped = frame_bgr[y1:y2, x1:x2]

                    with st.spinner(f"Searching for {label} matches..."):
                        related_images = fetch_related_images(label)
                        if related_images:
                            best_product = find_best_match(cropped, related_images)

                            if best_product:
                                st.success("Best match found!")
                                st.subheader(best_product.get("name", "Unknown"))
                                st.metric("Price", best_product.get("price", "Unknown"))

                                cols = st.columns(3)
                                for idx, img_name in enumerate(
                                    best_product.get("images", [])
                                ):
                                    img = cv2.imread(f"db/{img_name}")
                                    if img is not None:
                                        with cols[idx % 3]:
                                            st.image(
                                                cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                                                caption=img_name,
                                                use_container_width=True,
                                            )
                            else:
                                st.warning("No matching product found")
                        else:
                            st.error("No related products in database")
