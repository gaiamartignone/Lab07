from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:

    @staticmethod
    def get_all_situazioni(mese):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connessione fallita")
            return result

        try:
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT s.Localita, s.Data, s.Umidita
                FROM situazione s
                WHERE MONTH(s.data) = %s
                ORDER BY s.Data ASC
            """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
        except Exception as e:
            print(f"Errore durante l'esecuzione query: {e}")
        finally:
            if cursor:
                cursor.close()
            if cnx.is_connected():
                cnx.close()

        return result


