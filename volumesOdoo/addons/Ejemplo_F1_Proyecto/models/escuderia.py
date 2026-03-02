from odoo import models, fields


class F1Escuderia(models.Model):
    _name = 'f1.escuderia'
    _description = 'Escuderías de Formula 1'

    logo = fields.Image(string='Logo del Equipo', max_width=1024, max_height=1024)  # Sube imágenes redimensionadas.
    name = fields.Char(string='Nombre Escudería', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    jefe_equipo = fields.Char(string='Team Principal')
    presupuesto = fields.Float(string='Presupuesto (M$)')  # Número con decimales.

    # Relación Inversa (One2many): 1 escudería tiene Muchos pilotos. Se vincula mediante el campo 'escuderia_id' del piloto.
    piloto_ids = fields.One2many('f1.piloto', 'escuderia_id', string='Pilotos')