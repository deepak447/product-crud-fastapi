import json
from fastapi import Depends, FastAPI , Body , UploadFile , HTTPException
from pydantic import BaseModel
import os 
import uvicorn
import uuid
from typing import Optional , List
from dotenv import load_dotenv

from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
 
load_dotenv()

# Retrieve API Key from environment variables
API_KEY = os.environ['API_KEY']

# Define an API key header that will be required in requests
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Compares the provided API key from the request header with the stored API key.
    If the key is invalid, it raises an HTTP 401 Unauthorized error.
    """
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key
# Create a FastAPI instance and apply the API key verification globally
app = FastAPI(dependencies=[Depends(verify_api_key)])


# Define the upload directory
UPLOAD_DIR = "Upload_picture"
os.makedirs(UPLOAD_DIR, exist_ok=True) # Ensure the directory exists


class Product(BaseModel):
    id : str =None
    Product_Name: Optional[str] = None
    Price: Optional[float] = None
    Description: Optional[str] = None
    Quantity: Optional[int] = None

@app.get("/")
def read_root():
    return {"message" : "Welcome to Fast API project"}

@app.post("/upload_file/")
def upload_picture(files : List[UploadFile]):
    """
    Upload multiple files and save them to the server.
    
    Args:
        files (List[UploadFile]): List of files to upload.
    
    Returns:
        List[dict]: List of response messages with filenames and content types.
    """
    res = []
     # Loop through each file and save it
    for file in  files:
        file_path = os.path.join(UPLOAD_DIR, file.filename) # Create file path
        with open(file_path, "wb") as f:  # Open file in binary write mode
            f.write(file.file.read()) # Write the file contents
        res.append({"filename": file.filename, "content_type": file.content_type, "message": "File uploaded successfully"})
    return res



@app.post("/add_product/")
def add_product(product: Product):
    """
    Add a new product and store it in a JSON file.
    
    Args:
        product (Product): Product data to add.
    
    Returns:
        dict: Success message with added product details.
    """
    product.id = str(uuid.uuid4()) # Generate a unique product ID
    product_data = product.model_dump() # Convert the Pydantic model to a dictionary

    data = {}
    if os.path.exists('product.json'): # Check the json file is exist
        with open("product.json",'r') as file:  # read the json file
            data = json.load(file)  # Load existing data
        data = {}
    data[product.id] = product_data # Add new product to dictionary
    with open("product.json",'w') as file:
         json.dump(data, file, indent=4)  # Save the updated data to file

    return {
        "message" : "Product Saved successfully",
        "product" :product_data
    }

@app.get("/product_spec/")
def product_spec(id):
    """
    Retrieve a product by its ID.
    
    Args:
        id (str): The product ID to retrieve.
    
    Returns:
        dict: Product details if found, otherwise an error message.
    """ 
    with open('product.json','r') as file:
        data_dict = json.load(file)
        product  =  data_dict.get(id) # Get the product by ID
    if product:
        return product
    
@app.put("/update_product/{id}")
def update_product(id:str, update_product : Product):
    """
    Update an existing product entirely.
    
    Args:
        id (str): The product ID.
        update_product (Product): The new product data to update.
    
    Returns:
        dict: Success message with updated product details.
    """
    if os.path.exists("product.json"):
        with open('product.json','r') as file:
            data_dict = json.load(file)
    else: 
        data_dict ={}
    
    data_dict[id].update(update_product.model_dump()) # Replace old data with new

    with open('product.json','w') as file:
        json.dump(data_dict, file, indent=4)
    
    return {
        "message" : 'product update successfully',
        "data" : data_dict[id]
    }
@app.patch("/partial_update/{id}")
def partial_update(id:str, update_product : dict= Body(...)):
    """
    Partially update a product (only provided fields will be updated).
    
    Args:
        id (str): The product ID.
        update_product (dict): The fields to update.
    
    Returns:
        dict: Success message with updated product details.
    """
    if os.path.exists('product.json'):
        with open('product.json','r') as file:
            data_dict = json.load(file)
    else:
       return {"error": "Data not found"}
    
    data_dict[id].update(update_product) # Update only provided fields

    with open('product.json','w') as  file:
        json.dump(data_dict, file , indent= 4)
    return {
        "message" : "product update successfully ",
        "product" : data_dict[id]
    }
@app.delete('/delete_product/')
def delete_product(id : str):
    """
    Delete a product from the JSON file.
    
    Args:
        id (str): The product ID to delete.
    
    Returns:
        dict: Success message with deleted product details.
    """
    if os.path.exists('product.json'):
        with open('product.json','r') as file:
            data_dict = json.load(file)
    else:
        return {"error" : "data file not found"}
    if id not in data_dict:
        return {'error': f"Prodcut with {id} not found"}
    deleted_product = data_dict.pop(id)

    with open('product.json','w') as file:
        json.dump(data_dict, file, indent=4)
    return {
        "message" : "product deleted successfully",
        "product" : deleted_product
    }


if __name__ == "__main__" :
    uvicorn.run("test2:app",host="0.0.0.0",port=8080, reload=True)
