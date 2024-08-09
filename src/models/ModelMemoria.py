from .entities.Memoria import Memoria
from flask import flash

class ModelMemoria:
    @classmethod
    def register_memoria(cls, db, memoria):
        try:
            cursor = db.connection.cursor()

            # Obtener la junta directiva vigente (vigencia = 1)
            sql_vigente = "SELECT id FROM junta_directiva WHERE vigencia = 1 LIMIT 1"
            cursor.execute(sql_vigente)
            id_junta_vigente = cursor.fetchone()
            
            if not id_junta_vigente:
                flash("No hay una junta directiva vigente.")
                return False

            memoria.id_directiva = id_junta_vigente[0]
            
            # Verificar si ya existe una memoria para el mismo año y directiva
            sql_check = "SELECT COUNT(*) FROM memoria WHERE año = %s AND id_directiva = %s"
            cursor.execute(sql_check, (memoria.año, memoria.id_directiva))
            count = cursor.fetchone()[0]
            
            if count > 0:
                flash("Ya existe una memoria para este año en esta directiva.")
                return False

            # Registrar la memoria con la junta directiva vigente
            sql = """INSERT INTO memoria (nombre, año, ruta_pdf, id_directiva)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (memoria.nombre, memoria.año, memoria.ruta_pdf, memoria.id_directiva))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return False
        
    @classmethod
    def get_all_memorias(cls, db):
        try:
            cursor = db.connection.cursor()
            
            # Obtener la junta directiva vigente (vigencia = 1)
            sql_vigente = "SELECT id FROM junta_directiva WHERE vigencia = 1 LIMIT 1"
            cursor.execute(sql_vigente)
            id_junta_vigente = cursor.fetchone()
            
            if not id_junta_vigente:
                flash("No hay una junta directiva vigente.")
                return []

            id_junta_vigente = id_junta_vigente[0]
            
            # Obtener solo las memorias que pertenecen a la junta directiva vigente
            sql = """SELECT id, nombre, año, ruta_pdf, id_directiva FROM memoria 
                     WHERE id_directiva = %s"""
            cursor.execute(sql, (id_junta_vigente,))
            results = cursor.fetchall()
            memorias = []
            for row in results:
                memoria = Memoria(row[0], row[1], row[2], row[3], row[4])
                memorias.append(memoria)
            cursor.close()
            return memorias
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return []
        
    @classmethod
    def get_memoria_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM memoria WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row: 
                memoria = Memoria(row[0], row[1], row[2], row[3], row[4])
                return memoria
            return None
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return None

    @classmethod
    def update_memoria(cls, db, memoria):
        try:
            cursor = db.connection.cursor()

            # Obtener la junta directiva vigente (vigencia = 1)
            sql_vigente = "SELECT id FROM junta_directiva WHERE vigencia = 1 LIMIT 1"
            cursor.execute(sql_vigente)
            id_junta_vigente = cursor.fetchone()
            
            if not id_junta_vigente:
                flash("No hay una junta directiva vigente.")
                return False

            memoria.id_directiva = id_junta_vigente[0]
            
            # Verificar si ya existe una memoria para el mismo año y directiva, excluyendo la memoria actual
            sql_check = "SELECT COUNT(*) FROM memoria WHERE año = %s AND id_directiva = %s AND id != %s"
            cursor.execute(sql_check, (memoria.año, memoria.id_directiva, memoria.id))
            count = cursor.fetchone()[0]
            
            if count > 0:
                flash("Ya existe una memoria para este año en esta directiva.")
                return False

            # Actualizar la memoria con la nueva información
            sql = """UPDATE memoria SET nombre = %s, año = %s, ruta_pdf = %s, id_directiva = %s
                     WHERE id = %s"""
            cursor.execute(sql, (memoria.nombre, memoria.año, memoria.ruta_pdf, memoria.id_directiva, memoria.id))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return False

    @classmethod
    def delete_memoria(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM memoria WHERE id = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return False


    @classmethod
    def get_vigente_junta_id(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id FROM junta_directiva WHERE vigencia = 1 LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]  # Retorna el ID de la junta directiva vigente
            else:
                flash("No se encontró ninguna junta directiva vigente.")
                return None
        except Exception as ex:
            flash("ERROR: " + str(ex))
            return None
