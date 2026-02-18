import xmlrpc.client

# --- 1. DATOS DE CONEXIÓN ---
URL = 'http://localhost:8069'
DB = 'segundo-intento'
USER = 'davgomdel.alu@iesbenigaslo.es'
PASS = 'vK1fvSi9'

# --- 2. CONEXIÓN ---
try:
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASS, {})
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print(f"✅ Conectado (UID: {uid}). Escribe 'sortir' para acabar.")
except:
    print("❌ Error al conectar. Revisa DB, Usuario o si Docker está encendido.")
    exit()

# --- 3. BUCLE PRINCIPAL ---
while True:
    try:
        texto = input("\nOrdre > ").strip()
        if texto.lower() == 'sortir': break

        partes = texto.split(',')
        cmd = partes[0].capitalize().strip()
        datos = {}

        for p in partes[1:]:
            if '=' in p:
                key, val = p.split('=', 1)
                val_clean = val.replace('"', '').replace("'", '').replace('”', '').strip()
                if 'nombre' in key: datos['name'] = val_clean
                if 'num_socio' in key: datos['ref'] = val_clean

        # Lógica de comandos
        if cmd == 'Crear' and 'name' in datos:
            id_new = models.execute_kw(DB, uid, PASS, 'res.partner', 'create', [datos])
            print(f"Respuesta: Soci creat amb èxit en Odoo (ID: {id_new}).")

        elif cmd in ['Consultar', 'Borrar'] and 'ref' in datos:
            ids = models.execute_kw(DB, uid, PASS, 'res.partner', 'search', [[['ref', '=', datos['ref']]]])

            if not ids:
                print("Respuesta: No s'ha trobat cap soci amb eixa referència.")
            elif cmd == 'Consultar':
                res = models.execute_kw(DB, uid, PASS, 'res.partner', 'read', [ids], {'fields': ['name', 'ref']})
                print(f"Respuesta: Dades -> Nom: {res[0]['name']} | Referència: {res[0]['ref']}")
            elif cmd == 'Borrar':
                models.execute_kw(DB, uid, PASS, 'res.partner', 'unlink', [ids])
                print(f"Respuesta: Soci {datos['ref']} esborrat correctament.")

        else:
            print("Respuesta: Orden no soportada o faltan datos.")

    except Exception as e:
        print(f"Error: {e}")