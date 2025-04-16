from database import meteo_dao

class Model:
    def __init__(self):
        self._meteo_dao = meteo_dao.MeteoDao()

    def getumidita(self,mese):
        tomedia =0
        tocount=0
        gemedia=0
        gecount=0
        mimedia=0
        micount=0
        for situa in self._meteo_dao.get_all_situazioni():
            if situa.data.month==int(mese):
                if situa.localita == "Torino":
                    tomedia += situa.umidita
                    tocount +=1
                elif situa.localita == "Genova":
                    gemedia += situa.umidita
                    gecount += 1
                elif situa.localita == "Milano":
                    mimedia += situa.umidita
                    micount += 1
        return tomedia/tocount,gemedia/gecount,mimedia/micount

