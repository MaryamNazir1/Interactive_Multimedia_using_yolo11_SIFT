from pymongo import MongoClient

# ✅ Connect to MongoDB
client = MongoClient(
    "mongodb+srv://maryambhatti900:Hello123*@cluster0.hw8qz.mongodb.net/"
)
db = client["fashion_db"]
collection = db["products"]


# Define the structured product data
products_data = {
    "Bags": [
        {
            "name": "Elegant Leather Bag",
            "price": 49.99,
            "images": ["p1_1.PNG", "p1_2.PNG", "p1_3.PNG"],
        },
        {
            "name": "Casual Tote Bag",
            "price": 39.99,
            "images": ["p2_1.PNG", "p2_2.PNG", "p2_3.PNG"],
        },
        {
            "name": "Casual Bag ",
            "price": 39.99,
            "images": ["p3_1.PNG", "p3_2.PNG", "p3_3.PNG"],
        },
    ],
    "Dresses": [
        {
            "name": "Floral Summer Dress",
            "price": 79.99,
            "images": [
                "d1_1.PNG",
                "d1_2.PNG",
                "d1_3.PNG",
                "d1_4.PNG",
                "d1_5.PNG",
                "d1_6.PNG",
            ],
        },
        {
            "name": "Evening Gown",
            "price": 129.99,
            "images": [
                "d2_1.PNG",
                "d2_2.PNG",
                "d2_3.PNG",
                "d2_4.PNG",
                "d2_5.PNG",
                "d2_6.PNG",
            ],
        },
        {
            "name": "Evening dress",
            "price": 129.99,
            "images": [
                "d3_1.PNG",
                "d3_2.PNG",
                "d3_3.PNG",
                "d3_4.PNG",
                "d3_5.PNG",
            ],
        },
    ],
    "Shoes": [
        {
            "name": "Girls school shoes",
            "price": 59.99,
            "images": ["s1_1.PNG", "s1_2.PNG", "s1_3.PNG,s1_4.PNG"],
        },
        {
            "name": "boys Leather Shoes",
            "price": 89.99,
            "images": ["s2_1.PNG", "s2_2.PNG", "s2_3.PNG,S2_4.PNG"],
        },
    ],
}

# Insert the data as a single document
result = collection.insert_one(products_data)

# Print the inserted document ID
print("Inserted Document ID:", result.inserted_id)
