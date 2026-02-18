# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json  # <--- Faltaba esto para que funcione json.dumps


class Main(http.Controller):

    # ------------------------------------------------------
    # TU CÓDIGO EXISTENTE (Corregido)
    # ------------------------------------------------------
    @http.route('/ligafutbol/equipo/json', type='http', auth='public', csrf=False)
    def obtenerDatosEquiposJSON(self):
        equipos = request.env['liga.equipo'].sudo().search([])
        listaDatosEquipos = []
        for equipo in equipos:
            listaDatosEquipos.append([
                equipo.nombre,
                str(equipo.fecha_fundacion),
                equipo.jugados,
                equipo.puntos,
                equipo.victorias,
                equipo.empates,
                equipo.derrotas,
            ])
        return json.dumps(listaDatosEquipos)

    # ------------------------------------------------------
    # NUEVA FUNCIONALIDAD: ELIMINAR EMPATES
    # ------------------------------------------------------
    @http.route('/eliminarempates', type='http', auth='public', csrf=False)
    def eliminar_empates(self, **kw):
        """
        Recorre todos los partidos. Si hay empate, lo borra y cuenta uno más.
        Devuelve el total de partidos eliminados.
        """
        # 1. Buscamos TODOS los partidos con permisos de superusuario (sudo)
        partidos = request.env['liga.partido'].sudo().search([])

        contador = 0

        # 2. Recorremos buscando empates
        for partido in partidos:
            if partido.goles_casa == partido.goles_fuera:
                partido.unlink()  # Borramos el partido
                contador += 1

        # 3. Devolvemos el mensaje
        return f"Se han eliminado {contador} partidos que estaban empatados."