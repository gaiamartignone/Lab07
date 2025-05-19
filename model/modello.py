import copy
from database import meteo_dao
from model.situazione import Situazione


class Model:
    def __init__(self):
        self._meteo_dao = meteo_dao.MeteoDao()
        self.listapossibili = []
        self.soluzione = []
        self.bestcosto = -1
    def getumidita(self,mese):
        tomedia =0
        tocount=0
        gemedia=0
        gecount=0
        mimedia=0
        micount=0
        self.listapossibili = self._meteo_dao.get_all_situazioni(mese)
        for situa in self.listapossibili:
                if situa.localita == "Torino":
                    tomedia += situa.umidita
                    tocount +=1
                elif situa.localita == "Genova":
                    gemedia += situa.umidita
                    gecount += 1
                elif situa.localita == "Milano":
                    mimedia += situa.umidita
                    micount += 1
        return (
            tomedia / tocount if tocount > 0 else 0,
            gemedia / gecount if gecount > 0 else 0,
            mimedia / micount if micount > 0 else 0
        )

    def getsequenza(self,mese):
        self.listapossibili = self._meteo_dao.get_all_situazioni(mese)
        self.ricorsione([],0,1)
        return self.soluzione, self.bestcosto

    def ricorsione(self,parziale,count,livello):
        if len(parziale)==15:
            strin = ""
            for p in parziale:
                strin += p.localita +" "+ str(p.umidita)+"   "
            print(f"{strin}   {self.calcolacosto(parziale)}")
            #se è la prima sicuramente è la migliore
            if self.bestcosto == -1:
                self.soluzione =  copy.deepcopy(parziale)
                self.bestcosto =  self.calcolacosto(parziale)
        #sennò verifico se è la migliore
            else:
                costotemp = self.calcolacosto(parziale)
                if self.bestcosto > costotemp:
                    self.bestcosto = costotemp
                    self.soluzione = copy.deepcopy(parziale)
        for meta in self.listapossibili:
            if livello == meta.data.day:
                if self.controllalunghtot(parziale, meta):
                    if len(parziale)==0 :
                        parziale.append(meta)
                        self.ricorsione(parziale, count+1,livello+1)
                        parziale.pop()
                    #se conta non è a tre devo sicuramente aggiungere la città di prima
                    elif  count <3:
                        #aggiungo solo se la città è uguale
                        if parziale[-1].localita ==meta.localita:
                            parziale.append(meta)
                            self.ricorsione(parziale,count +1,livello+1)
                            parziale.pop()
                    #se conta è > 3 posso aggiungere qualsiasi, ma
                    elif parziale[-1].localita ==meta.localita:
                        parziale.append(meta)
                        self.ricorsione( parziale, count+1,livello+1) #se sono uguali mantengo il conto
                        parziale.pop()
                    else: #se non sono uguali azzero il conto
                        parziale.append(meta)
                        self.ricorsione( parziale, 1,livello+1)
                        parziale.pop()



    def calcolacosto(self,parziale): #parziale = situazione(
        costo =0
        for counter in range(len(parziale)):
            #primo giro conto 100 + umidità sicuro
                costo += parziale[counter].umidita
            # se quella precedente è diversa aggiungo anche il costo dello spostamento

        return costo



    def controllalunghtot(self, parziale, meta):
        conta=0
        for citta in parziale:
            if meta.localita==citta.localita:
                conta+=1
        return conta < 6

if __name__ == "__main__":
    m = Model()
    mese = "02"  # ad esempio Gennaio
    soluzione, costo = m.getsequenza(mese)

    print(f"Soluzione trovata per il mese {mese}:")
    for situazione in soluzione:
        print(situazione)
    print(f"Costo totale: {costo}")
