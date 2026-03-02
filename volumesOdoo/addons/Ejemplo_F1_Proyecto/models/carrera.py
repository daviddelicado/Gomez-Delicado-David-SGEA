from odoo import models, fields

class F1Carrera(models.Model):
    _name = 'f1.carrera'
    _description = 'Grandes Premios'

    name = fields.Char(string='Nombre del GP', required=True)
    circuito = fields.Char(string='Circuito')
    date_start = fields.Datetime(string='Inicio del Evento', required=True)
    date_stop = fields.Datetime(string='Fin del Evento')