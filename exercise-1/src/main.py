try:
    from .db.client import MongoDBClient, OpenF1Client
    from .services.session_service import get_session_by_id
    from .services.driver_service import get_drivers_by_session_id
    from .services.lap_service import get_laps_by_session_id
except ImportError:
    from db.client import MongoDBClient, OpenF1Client
    from services.session_service import get_session_by_id
    from services.driver_service import get_drivers_by_session_id
    from services.lap_service import get_laps_by_session_id
    
def f1_data_collector_by_session_id(session_id: input):
    mongo_client = MongoDBClient()
    open_f1_client = OpenF1Client()

    try:
        print(f"Coletando dados da sessão {session_id} ...")
        print("-="*20)

        session_data = get_session_by_id(session_id, open_f1_client)

        if not session_data:
            raise ValueError(
                f"Sessão {session_id} não encontrada."
            )

        session = session_data[0]
        mongo_client.salvar_na_colecao("sessions", [session], ["session_key"])

        print(f"Dados da sessão {session_id} coletados e salvos com sucesso no MongoDB.")
        print("-"*20)

        drivers_data = get_drivers_by_session_id(session_id, open_f1_client)
        mongo_client.salvar_na_colecao("drivers", drivers_data, ["session_key", "driver_number"])

        print(f"Dados de motoristas da sessão {session_id} coletados e salvos com sucesso no MongoDB.")
        print("-"*20)

        laps_data = get_laps_by_session_id(session_id, open_f1_client)
        mongo_client.salvar_na_colecao("laps", laps_data, ["session_key", "driver_number", "lap_number"])

        print(f"Dados de voltas da sessão {session_id} coletados e salvos com sucesso no MongoDB.")
        print("-"*20)

        print(f"Coleta de dados da sessão {session_id} concluída com sucesso.")
        print("-"*20)
        
    except Exception as e:
        print(f"Erro ao coletar dados da sessão {session_id}: {e}")

    finally:
        mongo_client.fechar_conexao_mongodb()

if __name__ == "__main__":
    session_id = input("Digite o ID da sessão: ")
    f1_data_collector_by_session_id(session_id)