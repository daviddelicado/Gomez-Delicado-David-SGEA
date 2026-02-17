# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Modelo abstracto de archivo'

    activo = fields.Boolean(default=True, string="Activo")

    def archivar(self):
        for record in self:
            record.activo = not record.activo


class BibliotecaComic(models.Model):
    _name = 'biblioteca.comic'
    _description = 'Cómic de la biblioteca'
    _inherit = ['base.archive']
    _order = 'fecha_publicacion desc, nombre'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Título', required=True, index=True)
    estado = fields.Selection([
        ('borrador', 'No disponible'),
        ('disponible', 'Disponible'),
        ('perdido', 'Perdido'),
    ], string='Estado', default='borrador')

    descripcion = fields.Html(string='Descripción', sanitize=True)
    portada = fields.Binary(string='Portada del cómic')
    fecha_publicacion = fields.Date(string='Fecha de publicación')
    precio = fields.Float(string='Precio')
    paginas = fields.Integer(string='Número de páginas')
    valoracion_lector = fields.Float(string='Valoración media', digits=(14, 4))

    autor_ids = fields.Many2many('res.partner', string='Autores')
    editorial_id = fields.Many2one('res.partner', string='Editorial')
    categoria_id = fields.Many2one('biblioteca.comic.categoria', string='Categoría')

    dias_lanzamiento = fields.Integer(
        string='Días desde lanzamiento',
            compute='_compute_dias_lanzamiento',
        inverse='_inverse_dias_lanzamiento',
        search='_search_dias_lanzamiento'
    )

    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Referencia a documento'
    )

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.depends('fecha_publicacion')
    def _compute_dias_lanzamiento(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.fecha_publicacion:
                delta = hoy - comic.fecha_publicacion
                comic.dias_lanzamiento = delta.days
            else:
                comic.dias_lanzamiento = 0

    def _inverse_dias_lanzamiento(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.dias_lanzamiento:
                comic.fecha_publicacion = hoy - timedelta(days=comic.dias_lanzamiento)

    def _search_dias_lanzamiento(self, operator, value):
        hoy = fields.Date.today()
        fecha_limite = hoy - timedelta(days=value)
        operator_map = {'>': '<', '>=': '<=', '<': '>', '<=': '>='}
        new_op = operator_map.get(operator, operator)
        return [('fecha_publicacion', new_op, fecha_limite)]

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El título del cómic debe ser único.'),
        ('positive_page', 'CHECK(paginas > 0)', 'El cómic debe tener al menos una página.')
    ]


# MODELOS DE SOCIOS Y PRÉSTAMOS
class BibliotecaSocio(models.Model):
    _name = 'biblioteca.socio'
    _description = 'Socio de la biblioteca'
    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    identificador = fields.Char(string='ID Socio', required=True)


class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Préstamo de cómic'
    comic_id = fields.Many2one('biblioteca.comic', string='Cómic', required=True)
    socio_id = fields.Many2one('biblioteca.socio', string='Socio', required=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', default=fields.Date.today)
    fecha_final = fields.Date(string='Fecha Entrega')

    @api.constrains('fecha_inicio', 'fecha_final')
    def _check_fechas(self):
        hoy = fields.Date.today()
        for record in self:
            if record.fecha_inicio and record.fecha_inicio > hoy:
                raise ValidationError("La fecha de inicio no puede ser futura.")
            if record.fecha_final and record.fecha_final < hoy:
                raise ValidationError("La fecha de entrega no puede ser anterior a hoy.")