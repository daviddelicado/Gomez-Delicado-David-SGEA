from odoo import models, fields, api


class F1Piloto(models.Model):
    _name = 'f1.piloto'
    _description = 'Pilotos de Formula 1'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    escuderia_id = fields.Many2one('f1.escuderia', string='Escudería')
    victorias = fields.Integer(string='Victorias Totales', default=0)
    titulos = fields.Integer(string='Campeonatos del Mundo', default=0)

    clasificacion_ids = fields.One2many('f1.clasificacion', 'piloto_id', string='Resultados')

    puntos_totales = fields.Integer(
        string='Puntos en el Mundial',
        compute='_compute_puntos_totales',
        store=True
    )

    @api.depends('clasificacion_ids.puntos_ganados')
    def _compute_puntos_totales(self):
        for piloto in self:
            piloto.puntos_totales = sum(piloto.clasificacion_ids.mapped('puntos_ganados'))