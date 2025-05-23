import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        if mese is None:
            self._view.create_alert("Attenzione, selezionare un mese!")
            self._view.update_page()
            return
        tomedia,gemedia,mimedia = self._model.getumidita(mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel "
        f"mese selezionato è:\n Genova:{gemedia}\n Milano:{mimedia}\n Torino:{tomedia}"))
        self._view.update_page()
        pass



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        if mese is None:
            self._view.create_alert("Attenzione, selezionare un mese!")
            self._view.update_page()
            return
        sequenza,costo = self._model.getsequenza(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo: {costo} ed è:"))
        for meta in sequenza:
            self._view.lst_result.controls.append(ft.Text(meta.__str__()))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

