from odoo import http
from odoo.http import request


class F1Controller(http.Controller):

    # Defensa: @http.route define la URL a la que el usuario debe acceder (ej. http://localhost:8069/f1/estado/1).
    # auth='public' significa que no necesitas estar logueado con contraseña en Odoo para ver esta pantalla.
    # <model("f1.inscripcion"):carrera> es magia de Odoo: coge el ID de la URL y busca automáticamente en la base de datos la carrera con ese ID.
    @http.route('/f1/estado/<model("f1.inscripcion"):carrera>', auth='public', website=True)
    def consultar_estado(self, carrera, **kwargs):
        if not carrera:
            return "Carrera no encontrada."

        # Llama a un template XML y le pasa el objeto 'carrera' para que saque sus datos.
        return http.request.render('Ejemplo_CampeonatoF1.estado_carrera_template', {
            'carrera': carrera
        })