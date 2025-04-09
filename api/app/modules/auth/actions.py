from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()  # Set up HTTPBasic security

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifies the provided username and password.

    Args:
        credentials (HTTPBasicCredentials): The HTTP Basic authentication credentials.

    Returns:
        str: The verified username.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    username = credentials.username
    password = credentials.password

    # Check if the username and password match the expected values
    if username == "irah" and password == "qwerty123":
        return {"message": f"{username} is authenticated"}

    # Raise an HTTP 401 Unauthorized exception if credentials are invalid
    raise HTTPException(status_code=401, detail="Invalid credentials")