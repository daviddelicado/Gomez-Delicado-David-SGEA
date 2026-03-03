from odoo import models, fields, api
from odoo.exceptions import ValidationError # Importante para lanzar mensajes de error en pantalla.

class F1Piloto(models.Model):
    _name = 'f1.piloto'
    _description = 'Pilotos de Formula 1'

    image = fields.Image(string='Foto del Piloto', max_width=1024, max_height=1024)
    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    edad = fields.Integer(string='Edad', required=True)
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

    # para evitar duplicados
    _sql_constraints = [
        (
            'piloto_nombre_apellido_unique',  # Nombre técnico de la restricción
            'UNIQUE (name, apellido)',  # Regla SQL: la combinación de ambos debe ser única
            'Ya existe un piloto con ese nombre y apellido. ¡No puedes duplicarlos!'  # Mensaje de error
        )
    ]

    @api.depends('clasificacion_ids.puntos_ganados') # Se recalcula si cambian los puntos ganados en sus clasificaciones.
    def _compute_puntos_totales(self):
        for piloto in self:
            # Suma total iterando sobre todos sus registros de clasificacion.
            piloto.puntos_totales = sum(piloto.clasificacion_ids.mapped('puntos_ganados'))

    @api.constrains('name', 'apellido')  # Se ejecuta cuando cambia el nombre o apellido
    def _check_nombres(self):
        for record in self:
            # Añadimos comprobación de que no sean None para evitar errores de comparación
            if record.name and record.apellido:
                # Comparamos ignorando mayúsculas/minúsculas y espacios extra
                if record.name.strip().lower() == record.apellido.strip().lower():
                    raise ValidationError("Error: El nombre y el apellido no pueden ser iguales.")