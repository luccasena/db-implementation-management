try:
    from ..db.client import OpenF1Client
except ImportError:
    from db.client import OpenF1Client

def get_laps_by_session_id(session_id: str, open_f1_client: OpenF1Client):
    return open_f1_client.get(f"/laps?session_key={session_id}")