import requests
import shared
from datetime import datetime

def get_user_medications(page):
    """
    Fetch the user's medications from the server.
    
    Args:
        page: The Flet page object containing client storage with user ID and token
        
    Returns:
        A list of medication dictionaries or an empty list if the request fails
    """
    # Get user data from client storage
    token = page.client_storage.get("sessionToken")
    user_id = page.client_storage.get("id")
    
    if not token or not user_id:
        print("No session token or user ID found")
        return []
    
    # Make request to server
    try:
        response = requests.post(
            f"http://{shared.SERVER_IP}:8080/getRecetas",
            json={"tokenLogin": token, "id": user_id}
        ).json()
        
        if response.get("correcto") == 1 and "recetas" in response:
            # Transform the data to match the expected format
            medications = []
            for receta in response["recetas"]:
                medications.append({
                    "name": receta["nombre"],
                    "dose": receta["dosificacion"],
                    "interval": receta["intervalosDosificacion"],
                    "start_date": receta["fechaEmision"],
                    "end_date": receta["fechaFin"]
                })
            return medications
        else:
            print(f"Error fetching medications: {response.get('mensaje', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Exception fetching medications: {str(e)}")
        return []

def format_date(iso_date_string):
    """
    Format an ISO date string to a more readable format
    
    Args:
        iso_date_string: ISO format date string
        
    Returns:
        A formatted date string like "02/02/2025"
    """
    if not iso_date_string:
        return "N/A"
    try:
        date_obj = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return iso_date_string
    
def get_otp_key(page):
    
    token = page.client_storage.get("sessionToken")
    user_id = page.client_storage.get("id")
    
    if not token or not user_id:
        print("No session token or user ID found")
        return None
    
    try:
        response = requests.post(
            f"http://{shared.SERVER_IP}:8080/crearTokenEditar",
            json={"tokenLogin": token, "id": user_id}
        ).json()
        
        if response.get("correcto") == 1:
            return response.get("token")
        else:
            return "Error generando token"
    except Exception as e:
        return None
    