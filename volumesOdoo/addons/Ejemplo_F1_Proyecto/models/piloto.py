from odoo import models, fields, api
from odoo.exceptions import ValidationError # Importante para lanzar mensajes de error en pantalla.

class F1Piloto(models.Model):
    _name = 'f1.piloto'
    _description = 'Pilotos de Formula 1'

    image = fields.Image(string='Foto del Piloto', max_width=1024, max_height=1024)
    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    escuderia_id = fields.Many2one('f1.escuderia', string='Escudería') # Enlace a la tabla escudería.

    # Campo de selección desplegable. Default marca por defecto 'activo' al crear uno nuevo.
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('lesionado', 'Lesionado'),
        ('retirado', 'Retirado')
    ], string='Estado', default='activo')

    # Historial de resultados de este piloto.
    clasificacion_ids = fields.One2many('f1.clasificacion', 'piloto_id', string='Resultados')

    # Campo calculado para el campeonato.
    puntos_totales = fields.Integer(
        string='Puntos Totales',
        compute='_compute_puntos_totales',
        store=True
    )

    @api.depends('clasificacion_ids.puntos_ganados') # Se recalcula si cambian los puntos ganados en sus clasificaciones.
    def _compute_puntos_totales(self):
        for piloto in self:
            # Suma total iterando sobre todos sus registros de clasificacion.
            piloto.puntos_totales = sum(piloto.clasificacion_ids.mapped('puntos_ganados'))

    @api.constrains('name', 'apellido') # Restricción o validación en base de datos.
    def _check_nombres(self):
        for record in self:
            # Lanza un pop-up de error bloqueando el guardado si nombre y apellido son idénticos.
            if record.name == record.apellido:
                raise ValidationError("El nombre y el apellido no pueden ser iguales.")