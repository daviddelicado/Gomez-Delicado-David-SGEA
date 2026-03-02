from odoo import models, fields, api

class F1Clasificacion(models.Model):
    _name = 'f1.clasificacion'
    _description = 'Resultados y Clasificación'

    carrera_id = fields.Many2one('f1.carrera', string='Gran Premio', required=True)
    piloto_id = fields.Many2one('f1.piloto', string='Piloto', required=True)
    posicion = fields.Integer(string='Posición Final', required=True)

    puntos_ganados = fields.Integer(string='Puntos Conseguidos', compute='_compute_puntos', store=True)

    @api.depends('posicion')
    def _compute_puntos(self):
        # Sistema clásico de F1
        puntos_f1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
        for record in self:
            record.puntos_ganados = puntos_f1.get(record.posicion, 0)