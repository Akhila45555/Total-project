from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Day 38 Ticketing REST API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

tickets = []

class Ticket(BaseModel):
    title: str
    description: str
    priority: str = "Medium"
    status: str = "Open"

@app.get("/")
def home():
    return {"message": "Ticketing REST API is running"}

@app.post("/tickets")
def create_ticket(ticket: Ticket):
    new_ticket = {
        "id": str(uuid4())[:8],
        **ticket.model_dump()
    }
    tickets.append(new_ticket)
    return {"message": "Ticket created successfully",
            "ticket": new_ticket}

@app.get("/tickets")
def get_tickets():
    return {"total": len(tickets), "tickets": tickets}

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404,
                        detail="Ticket not found")

@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, status: str):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = status
            return {"message": "Ticket updated",
                    "ticket": ticket}
    raise HTTPException(status_code=404,
                        detail="Ticket not found")