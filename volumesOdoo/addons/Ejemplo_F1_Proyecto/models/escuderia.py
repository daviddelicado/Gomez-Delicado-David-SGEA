from odoo import models, fields

class F1Escuderia(models.Model):
    _name = 'f1.escuderia'
    _description = 'Escuderías de Formula 1'

    name = fields.Char(string='Nombre Escudería', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    jefe_equipo = fields.Char(string='Team Principal')
    presupuesto = fields.Float(string='Presupuesto (M$)')
    piloto_ids = fields.One2many('f1.piloto', 'escuderia_id', string='Pilotos')