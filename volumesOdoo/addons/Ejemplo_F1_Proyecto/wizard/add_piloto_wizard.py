from odoo import models, fields

# TransientModel a diferencia de Model, indica que los datos introducidos aquí se borrarán tras usarse, no son fijos.
class AddPilotoWizard(models.TransientModel):
    _name = 'f1.add.piloto.wizard'
    _description = 'Asistente para añadir pilotos'

    # Campos que el usuario rellenará en la ventana emergente.
    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    escuderia_id = fields.Many2one('f1.escuderia', string='Escudería')

    # Función Python que se ejecutará al pulsar el botón "Guardar" del popup.
    def action_create_piloto(self):
        # Llama a self.env para buscar el modelo real de piloto y crear uno nuevo con los datos tecleados aquí.
        self.env['f1.piloto'].create({
            'name': self.name,
            'apellido': self.apellido,
            'escuderia_id': self.escuderia_id.id,
        })