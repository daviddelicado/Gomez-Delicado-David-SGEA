from odoo import http
from odoo.http import request  # Necesario para acceder a la base de datos desde fuera


class F1Controller(http.Controller):

    # Ruta web que espera recibir un número entero (<int:piloto_id>) al final de la URL
    @http.route('/f1/piloto/<int:piloto_id>', auth='public', type='http')
    def estado_piloto(self, piloto_id, **kw):
        # Usamos request.env para entrar al modelo de pilotos.
        # sudo() se usa porque el usuario es 'public' (no ha iniciado sesión) y necesita permisos de lectura.
        piloto = request.env['f1.piloto'].sudo().browse(piloto_id)

        # Comprobamos si el piloto existe en la base de datos
        if not piloto.exists():
            return "<h1>Error: No se ha encontrado ningún piloto con ese ID.</h1>"

        # Si existe, extraemos su nombre, apellido y estado, y lo devolvemos maquetado en HTML simple
        html_result = f"""
            <h2>Consulta de Estado - Fórmula 1</h2>
            <p><strong>Piloto:</strong> {piloto.name} {piloto.apellido}</p>
            <p><strong>Estado actual:</strong> <span style="color: blue;">{piloto.estado.upper()}</span></p>
        """

        return html_result