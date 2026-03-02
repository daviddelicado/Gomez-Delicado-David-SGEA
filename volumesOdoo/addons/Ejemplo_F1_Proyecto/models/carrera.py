from odoo import models, fields

class F1Carrera(models.Model):
    _name = 'f1.carrera' # Nombre técnico de la tabla en PostgreSQL.
    _description = 'Grandes Premios' # Nombre legible para el sistema.

    # Definición de las columnas de la tabla:
    name = fields.Char(string='Nombre del GP', required=True) # Texto (obligatorio).
    circuito = fields.Char(string='Circuito') # Texto.
    date_start = fields.Datetime(string='Inicio del Evento', required=True) # Campo de Fecha y Hora.
    date_stop = fields.Datetime(string='Fin del Evento') # Campo de Fecha y Hora.