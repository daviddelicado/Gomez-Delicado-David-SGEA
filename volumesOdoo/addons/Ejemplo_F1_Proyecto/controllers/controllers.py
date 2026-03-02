from odoo import http  # Importa el módulo http de Odoo para crear rutas (URLs)
from odoo.http import request  # 'request' permite interactuar con la base de datos desde la web
import json  # Librería estándar de Python para formatear los datos a formato JSON


class F1Controller(http.Controller):  # Clase controladora que hereda de http.Controller

    # @http.route crea la URL '/f1/pilotos'.
    # auth='public' significa que cualquiera puede entrar sin estar logueado.
    # type='http' y methods=['GET'] indica que es una petición web normal de solo lectura.
    @http.route('/f1/pilotos', auth='public', type='http', methods=['GET'])
    def get_pilotos(self, **kw):
        # request.env[...] accede al modelo.
        # .sudo() da permisos de administrador para saltar posibles restricciones de seguridad.
        # .search([]) busca y devuelve TODOS los registros de pilotos.
        pilotos = request.env['f1.piloto'].sudo().search([])
        data = []  # Lista vacía que guardará los datos finales

        for p in pilotos:
            # Añadimos a la lista un diccionario (JSON) con los datos clave de cada piloto
            data.append({
                'nombre': f"{p.name} {p.apellido}",
                'escuderia': p.escuderia_id.name if p.escuderia_id else "Sin equipo",  # Comprueba si tiene escudería
                'puntos': p.puntos_totales
            })

        # Genera la respuesta HTTP enviando la lista 'data' convertida a texto JSON
        # Configura las cabeceras (headers) para avisar al navegador de que es un archivo JSON.
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )