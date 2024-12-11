from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepGProp import brepgprop_LinearProperties, brepgprop_SurfaceProperties, brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

from OCC.Extend.DataExchange import write_iges_file

import os
import boto3
from uuid import uuid4

from dotenv import load_dotenv

# Load environment variables from .env file if not in production
ENV = os.getenv("ENV", "DEV").upper()
if ENV != "PROD":
    load_dotenv()

app = FastAPI()

class CreateBoxBody(BaseModel):
    x: float
    y: float
    z: float

# Fetch S3 configuration from environment variables
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_REGION = os.getenv("S3_REGION")

# Validate that all necessary environment variables are set
if not all([S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_REGION]):
    raise RuntimeError("Missing one or more required AWS environment variables.")


# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=S3_REGION
)

def get_box_statistics(box_shape):
    """
    Calculate statistics for the given box shape.
    """
    props = GProp_GProps()
    
    # Volume
    brepgprop_VolumeProperties(box_shape, props)
    volume = props.Mass()

    # Surface area
    brepgprop_SurfaceProperties(box_shape, props)
    surface_area = props.Mass()

    # Bounding box dimensions
    brepgprop_LinearProperties(box_shape, props)
    length = props.CentreOfMass().X() * 2
    width = props.CentreOfMass().Y() * 2
    height = props.CentreOfMass().Z() * 2
    
    return {
        "volume": volume,
        "surface_area": surface_area,
        "length": length,
        "width": width,
        "height": height,
    }

@app.get("/")
def read_root():
    my_box = BRepPrimAPI_MakeBox(20.0, 20.0, 20.0).Shape()
    box_stats = get_box_statistics(my_box)
    
    return {
        "status": "success",
        "box_statistics": box_stats,
    }

@app.post("/create-box")
async def create_box(box_data: CreateBoxBody):
    
    x = box_data.x
    y = box_data.y
    z = box_data.z

    try:
        my_box = BRepPrimAPI_MakeBox(x, y, z).Shape()
    
        # Save IGES file locally
        local_iges_filename = "{}.iges".format(uuid4())
        write_iges_file(my_box, local_iges_filename)

        s3_key = "iges_files/{}".format(local_iges_filename)
        with open(local_iges_filename, "rb") as file:
            s3_client.upload_fileobj(file, S3_BUCKET_NAME, s3_key, ExtraArgs={"ACL": "public-read"})

        # Construct S3 file URL
        s3_file_url = "https://{}.s3.{}.amazonaws.com/{}".format(S3_BUCKET_NAME, S3_REGION, s3_key)

        # Clean up local file
        os.remove(local_iges_filename)

        return {
            "path_to_iges_file": s3_file_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create the box BREP data: {e}")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
