from fastapi import APIRouter, Depends
from typing import Dict
from app.irah.router import IRAH_APIRoute
from . import schema, actions

# Create an APIRouter instance with a custom route class
router = APIRouter(route_class=IRAH_APIRoute)

# Define a POST endpoint for user login
@router.post("/login")
def post(item: schema.AuthSchema = Depends(actions.verify_password)):
    """
    Handle POST request for user login.

    Args:
        item (schema.AuthSchema): The authenticated user item which contains username and other details.

    Returns:
        Dict: A dictionary containing the username of the authenticated user.
    """
    # Return a dictionary with the username
    return {"username": item.username}
