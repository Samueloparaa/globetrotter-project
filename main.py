from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import json
import os
import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "globetrotter-secret-key-change-this-later"
ALGORITHM = "HS256"

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "destinations": [], "itineraries": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ItineraryRequest(BaseModel):
    destination_id: int
    title: str
    notes: str = ""

@app.get("/")
def read_root():
    return {"message": "GlobeTrotter API is running"}

@app.post("/register")
def register(req: RegisterRequest):
    data = load_data()
    for user in data["users"]:
        if user["email"] == req.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(req.password)
    data["users"].append({"email": req.email, "password": hashed_password})
    save_data(data)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(req: LoginRequest):
    data = load_data()
    for user in data["users"]:
        if user["email"] == req.email:
            if verify_password(req.password, user["password"]):
                token = jwt.encode(
                    {"sub": user["email"], "exp": datetime.utcnow() + timedelta(hours=1)},
                    SECRET_KEY,
                    algorithm=ALGORITHM
                )
                return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/destinations")
def get_destinations():
    data = load_data()
    return data["destinations"]

@app.get("/recommendations")
def get_recommendations(current_user: str = Depends(get_current_user)):
    data = load_data()
    return {"recommended_for": current_user, "destinations": data["destinations"]}

@app.post("/itineraries")
def create_itinerary(req: ItineraryRequest, current_user: str = Depends(get_current_user)):
    data = load_data()
    new_itinerary = {
        "id": len(data["itineraries"]) + 1,
        "owner": current_user,
        "destination_id": req.destination_id,
        "title": req.title,
        "notes": req.notes
    }
    data["itineraries"].append(new_itinerary)
    save_data(data)
    return new_itinerary

@app.get("/itineraries")
def get_itineraries(current_user: str = Depends(get_current_user)):
    data = load_data()
    user_itineraries = [i for i in data["itineraries"] if i["owner"] == current_user]
    return user_itineraries
    