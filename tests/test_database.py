import pytest
from unittest.mock import MagicMock, patch
from model.database import Database

# Prueba de conexión exitosa
@patch('mysql.connector.connect')
def test_conexion_exitosa(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    db = Database(host='localhost', user='root', password='', database='face_secure')
    
    print(f"Probando conexión exitosa a la base de datos: {db.conn is not None} y {db.cursor is not None}")
    
    assert db.conn is not None
    assert db.cursor is not None
    db.cerrar()

# Prueba de fallo en la conexión con reintentos
@patch('mysql.connector.connect', side_effect=Exception('Error conexión'))
def test_conexion_falla_reintentos(mock_connect):
    print("Probando fallo en la conexión con reintentos...")
    
    with pytest.raises(Exception):
        Database(host='localhost', user='root', password='', database='face_secure', max_retries=2, retry_delay=0)

# Prueba de obtener usuarios
@patch('mysql.connector.connect')
def test_obtener_usuarios(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'id':1, 'nombre':'Test'}]
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    db = Database(host='localhost', user='root', password='', database='face_secure')
    usuarios = db.obtener_usuarios()
    
    print(f"Usuarios obtenidos de la base de datos: {usuarios}")
    
    assert isinstance(usuarios, list)
    assert len(usuarios) >= 1
    db.cerrar()
