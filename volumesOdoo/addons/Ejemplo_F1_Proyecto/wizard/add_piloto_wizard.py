from odoo import models, fields

class AddPilotoWizard(models.TransientModel):
    _name = 'f1.add.piloto.wizard'
    _description = 'Asistente para añadir pilotos'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    escuderia_id = fields.Many2one('f1.escuderia', string='Escudería')

    # Requisito: Método 4 (Acción de Wizard)
    def action_create_piloto(self):
        self.env['f1.piloto'].create({
            'name': self.name,
            'apellido': self.apellido,
            'escuderia_id': self.escuderia_id.id,
        })