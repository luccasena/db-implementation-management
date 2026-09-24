try:
    from ..db.client import OpenF1Client
except ImportError:
    from db.client import OpenF1Client

def get_drivers_by_session_id(session_id: str, open_f1_client: OpenF1Client):
    return open_f1_client.get(f"/drivers?session_key={session_id}")