# -*- coding: utf-8 -*-
from odoo import models, fields


# ==============================================================
#  MODELO TRANSIENTE (WIZARD) - PARTIDOS
# ==============================================================

class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Asistente para crear nuevos partidos'

    # --------------------------------------------------------------
    # CAMPOS DEL WIZARD
    # --------------------------------------------------------------

    # Equipo Local (Seleccionable)
    equipo_casa = fields.Many2one('liga.equipo', string='Equipo Local', required=True)

    # Goles Local (Por defecto 0)
    goles_casa = fields.Integer(string='Goles Local', default=0)

    # Equipo Visitante (Seleccionable)
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo Visitante', required=True)

    # Goles Visitante (Por defecto 0)
    goles_fuera = fields.Integer(string='Goles Visitante', default=0)

    # --------------------------------------------------------------
    # MÉTODO PRINCIPAL DEL WIZARD
    # --------------------------------------------------------------
    def add_liga_partido(self):
        """
        Método que se ejecuta cuando el usuario pulsa el botón "Añadir partido".
        Crea un nuevo registro en el modelo liga.partido.
        """

        # Obtenemos la referencia al modelo destino (liga.partido)
        liga_partido_model = self.env['liga.partido']

        # Recorremos el wizard (aunque sea un solo registro)
        for wiz in self:
            # Creamos el nuevo partido con los datos introducidos
            liga_partido_model.create({
                'equipo_casa': wiz.equipo_casa.id,
                'goles_casa': wiz.goles_casa,
                'equipo_fuera': wiz.equipo_fuera.id,
                'goles_fuera': wiz.goles_fuera,
            })

        # Odoo cerrará la ventana automáticamente al terminar