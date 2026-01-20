# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BibliotecaSocio(models.Model):
    _name = 'biblioteca.socio'
    _description = 'Socio de la Biblioteca'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    identificador = fields.Char(string='ID Socio', required=True)

    _sql_constraints = [
        ('identificador_unique', 'UNIQUE(identificador)', 'El ID de socio debe ser único.')
    ]

class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Registro de Préstamos'

    comic_id = fields.Many2one('biblioteca.comic', string='Cómic', required=True)
    socio_id = fields.Many2one('biblioteca.socio', string='Socio', required=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', default=fields.Date.today, required=True)
    fecha_final = fields.Date(string='Fecha Entrega Prevista', required=True)

    @api.constrains('fecha_inicio')
    def _check_fecha_inicio(self):
        for record in self:
            if record.fecha_inicio and record.fecha_inicio > fields.Date.today():
                raise ValidationError("La fecha de inicio no puede ser posterior a hoy.")

    @api.constrains('fecha_final')
    def _check_fecha_final(self):
        for record in self:
            if record.fecha_final and record.fecha_final < fields.Date.today():
                raise ValidationError("La fecha de entrega no puede ser anterior a hoy.")