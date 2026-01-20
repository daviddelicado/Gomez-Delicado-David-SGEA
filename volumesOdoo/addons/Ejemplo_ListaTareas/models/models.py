# -*- coding: utf-8 -*-

# Importamos los módulos necesarios de Odoo para definir modelos
from odoo import models, fields, api
from odoo.exceptions import ValidationError


# a.1 Gestión de Socios
class ListaTareasSocio(models.Model):
    _name = 'lista_tareas.socio'
    _description = 'Gestión de Socios'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    identificador = fields.Char(string='ID Socio', required=True)


# a.2.1 El modelo de cómic (usaremos el de tareas como base o uno nuevo)
# Para seguir tu enunciado, creamos el modelo de Cómic referencia
class ListaTareasComic(models.Model):
    _name = 'lista_tareas.comic'
    _description = 'Referencia de Cómic'
    name = fields.Char(string='Título del Cómic', required=True)
    autor = fields.Char(string='Autor')


# a.2.2 Ejemplares de préstamo
class ListaTareasPrestamo(models.Model):
    _name = 'lista_tareas.prestamo'
    _description = 'Ejemplares de préstamo'

    comic_id = fields.Many2one('lista_tareas.comic', string='Cómic', required=True)
    socio_id = fields.Many2one('lista_tareas.socio', string='Prestado a')
    fecha_inicio = fields.Date(string='Fecha de Inicio', default=fields.Date.today)
    fecha_final = fields.Date(string='Fecha Prevista de Vuelta')

    # a.2.2.1 La data de préstec no pot ser posterior al dia de hui.
    @api.constrains('fecha_inicio')
    def _check_fecha_inicio(self):
        for record in self:
            if record.fecha_inicio and record.fecha_inicio > fields.Date.today():
                raise ValidationError("La fecha de préstamo no puede ser posterior a hoy.")

    # a.2.2.2 La data prevista de tornada no pot ser anterior al dia de hui.
    @api.constrains('fecha_final')
    def _check_fecha_final(self):
        for record in self:
            if record.fecha_final and record.fecha_final < fields.Date.today():
                raise ValidationError("La fecha de vuelta no puede ser anterior a hoy.")


# 🏷️ NUEVO MODELO PARA CATEGORÍAS
# Se crea para poder clasificar las tareas
class ListaTareasCategoria(models.Model):
    _name = 'lista_tareas.categoria'
    _description = 'Categorías de tareas'
    name = fields.Char(string='Nombre de Categoría', required=True)

# Creamos nuestro modelo de datos principal.
# Todos los modelos de Odoo deben heredar de models.Model
class ListaTareas(models.Model):  # Buenas prácticas: nombres de clase en PascalCase (MayúsculaInicial)

    # Nombre técnico del modelo. Es como Odoo lo guarda internamente en la base de datos
    _name = 'lista_tareas.lista'

    fecha_asignada = fields.Date(
        string='Fecha Asignada',
        default=fields.Date.context_today
    )

    # Descripción que aparece en la documentación y ayuda
    _description = 'Modelo de la lista de tareas'

    # Indica qué campo se mostrará por defecto como nombre del registro (en vistas y menús desplegables)
    _rec_name = "tarea"

    # Definimos los campos (atributos) que tendrá cada registro de este modelo:

    # Campo de tipo texto (cadena). Será el nombre de la tarea.
    tarea = fields.Char(string="Tarea")

    # Campo de tipo entero. Se usará para indicar la prioridad (ej: 1 a 100)
    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
        ('3', 'Muy Alta')
    ], string="Prioridad", default='0')

    # Campo calculado de tipo booleano. Será True si la prioridad > 10
    # compute indica el método que lo calcula
    # store=True guarda el valor en la base de datos para poder filtrar y ordenar por él
    urgente = fields.Boolean(string="Urgente", compute="_value_urgente", store=True)

    # Campo booleano normal. Será marcado si la tarea ya se realizó.
    realizada = fields.Boolean(string="Realizada")

    # ---------------------------------------------------------
    # NUEVOS CAMPOS AÑADIDOS (Manteniendo lo anterior)
    # ---------------------------------------------------------

    # 🔧 1. Fecha límite y campo computado de vencimiento
    data_limit = fields.Date(string='Fecha Límite')
    vencida = fields.Boolean(string="Vencida", compute="_compute_vencida", store=True)

    # 👤 2. Asignar tareas a usuarios del sistema (Many2one)
    user_id = fields.Many2one(
        'res.users',
        string='Usuario Asignado',
        default=lambda self: self.env.user
    )

    # 🏷️ 3. Relación con categorías
    categoria_id = fields.Many2one('lista_tareas.categoria', string='Categoría')

    # -------------------------------
    # MÉTODO COMPUTADO ORIGINAL
    # -------------------------------
    # Este método se ejecuta cada vez que cambie el campo 'prioridad'
    @api.depends('prioridad')
    def _value_urgente(self):
        for record in self:
            # Convertimos a entero para comparar
            record.urgente = int(record.prioridad) >= 2

    # -------------------------------
    # NUEVOS MÉTODOS COMPUTADOS
    # -------------------------------
    @api.depends('data_limit', 'realizada')
    def _compute_vencida(self):
        # Obtenemos la fecha de hoy desde los campos de Odoo
        today = fields.Date.today()
        for record in self:
            # Si tiene fecha límite, no está hecha y la fecha es anterior a hoy
            if record.data_limit and not record.realizada:
                record.vencida = record.data_limit < today
            else:
                record.vencida = False

# ==========================================================
# ACTIVITAT 03: MODELOS DE INSTITUTO
# ==========================================================

class InstitutoCiclo(models.Model):
    _name = 'instituto.ciclo'
    _description = 'Ciclo Formativo'
    name = fields.Char(string='Nombre del Ciclo', required=True)
    modulo_ids = fields.One2many('instituto.modulo', 'ciclo_id', string='Módulos')

class InstitutoModulo(models.Model):
    _name = 'instituto.modulo'
    _description = 'Módulo Profesional'
    name = fields.Char(string='Nombre del Módulo', required=True)
    ciclo_id = fields.Many2one('instituto.ciclo', string='Ciclo Formativo')
    professor_id = fields.Many2one('instituto.professor', string='Profesor')
    alumne_ids = fields.Many2many('instituto.alumne', string='Alumnos Matriculados')

class InstitutoAlumne(models.Model):
    _name = 'instituto.alumne'
    _description = 'Alumno'
    name = fields.Char(string='Nombre y Apellidos', required=True)
    modulo_ids = fields.Many2many('instituto.modulo', string='Módulos Inscritos')

class InstitutoProfessor(models.Model):
    _name = 'instituto.professor'
    _description = 'Profesor'
    name = fields.Char(string='Nombre', required=True)
    modulo_ids = fields.One2many('instituto.modulo', 'professor_id', string='Módulos impartidos')