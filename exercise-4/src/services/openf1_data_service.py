from db.clients import obter_banco_mongodb

class OpenF1DataService:
    def __init__(self):
        self.mongo_db = obter_banco_mongodb()

    def listar_anos_disponiveis(self) -> list[int]:
        anos = self.mongo_db.sessions.distinct("year")
        return sorted(anos, reverse=True)

    def listar_sessoes_por_ano(self, ano: int) -> list[dict]:
        return list(
            self.mongo_db.sessions.find(
                {"year": ano},
                {
                    "session_key": 1,
                    "session_name": 1,
                    "session_type": 1,
                    "location": 1,
                    "country_name": 1,
                    "circuit_short_name": 1,
                    "date_start": 1,
                },
            ).sort("date_start", 1)
        )

    def obter_detalhes_sessao(self, session_key: int) -> dict | None:
        return self.mongo_db.sessions.find_one({"session_key": session_key})

    def contar_voltas_por_sessao(self, session_key: int) -> int:
        return self.mongo_db.laps.count_documents({"session_key": session_key})

    def listar_pilotos_por_sessao(self, session_key: int) -> list[dict]:
        return list(
            self.mongo_db.drivers.find(
                {"session_key": session_key},
                {
                    "driver_number": 1,
                    "full_name": 1,
                    "name_acronym": 1,
                    "team_name": 1,
                    "team_colour": 1,
                    "headshot_url": 1,
                },
            ).sort("driver_number", 1)
        )

    def obter_voltas_por_sessao_e_pilotos(
        self, session_key: int, numeros_pilotos: list[int]
    ) -> list[dict]:
        return list(
            self.mongo_db.laps.find(
                {
                    "session_key": session_key,
                    "driver_number": {"$in": numeros_pilotos},
                },
                {
                    "driver_number": 1,
                    "lap_number": 1,
                    "lap_duration": 1,
                    "duration_sector_1": 1,
                    "duration_sector_2": 1,
                    "duration_sector_3": 1,
                    "segments_sector_1": 1,
                    "segments_sector_2": 1,
                    "segments_sector_3": 1,
                    "st_speed": 1,
                    "is_pit_out_lap": 1,
                },
            ).sort("lap_number", 1)
        )
