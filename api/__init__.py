from .api_server import APIServer

_api_instance = APIServer()
app = _api_instance.app  # Esta es la variable que uvicorn busca
