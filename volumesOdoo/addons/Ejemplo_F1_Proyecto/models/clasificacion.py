from odoo import models, fields, api

class F1Clasificacion(models.Model):
    _name = 'f1.clasificacion'
    _description = 'Resultados y Clasificación'

    # Relaciones Many2one: Muchos resultados apuntan a 1 sola carrera y 1 solo piloto.
    carrera_id = fields.Many2one('f1.carrera', string='Gran Premio', required=True)
    piloto_id = fields.Many2one('f1.piloto', string='Piloto', required=True)
    posicion = fields.Integer(string='Posición Final', required=True) # Número entero.

    # Campo calculado (compute). Odoo lo rellena solo ejecutando la función _compute_puntos. store=True lo guarda en BD.
    puntos_ganados = fields.Integer(string='Puntos Conseguidos', compute='_compute_puntos', store=True)

    @api.depends('posicion') # Decorador: Avisa a Odoo que recalcule los puntos si alguien cambia la 'posicion'.
    def _compute_puntos(self):
        # Diccionario con los puntos oficiales de F1 según la posición (1º da 25, 2º da 18...)
        puntos_f1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
        for record in self:
            # Asigna los puntos buscando la posición en el diccionario. Si no está en el top 10, asigna 0.
            record.puntos_ganados = puntos_f1.get(record.posicion, 0)