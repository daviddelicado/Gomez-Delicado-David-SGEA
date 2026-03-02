from odoo import models, fields, api
from odoo.exceptions import ValidationError


class F1Piloto(models.Model):
    _name = 'f1.piloto'
    _description = 'Pilotos de Formula 1'

    image = fields.Image(string='Foto del Piloto', max_width=1024, max_height=1024)
    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    escuderia_id = fields.Many2one('f1.escuderia', string='Escudería')

    # Requisito: Estados para colores en vistas
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('lesionado', 'Lesionado'),
        ('retirado', 'Retirado')
    ], string='Estado', default='activo')

    clasificacion_ids = fields.One2many('f1.clasificacion', 'piloto_id', string='Resultados')

    puntos_totales = fields.Integer(
        string='Puntos Totales',
        compute='_compute_puntos_totales',
        store=True
    )

    @api.depends('clasificacion_ids.puntos_ganados')
    def _compute_puntos_totales(self):
        for piloto in self:
            piloto.puntos_totales = sum(piloto.clasificacion_ids.mapped('puntos_ganados'))

    @api.constrains('name', 'apellido')
    def _check_nombres(self):
        for record in self:
            if record.name == record.apellido:
                raise ValidationError("El nombre y el apellido no pueden ser iguales.")