import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

credenciales={
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'database': os.getenv('DATABASE'),
    'port': os.getenv('PORT')
}
def conexion(licencias):
    conexion = mysql.connector.connect(**licencias)
    return conexion
def desconectar(conexion):
    if conexion.is_connected():
        return conexion.close()

if '__main__' == __name__:
    print('Conexion a una base de datos')
    db=conexion(credenciales)
    cursor=db.cursor()
    query='SELECT Nombre, Apellidos, CorreoElectronico, Empleo FROM premium'
    cursor.execute(query)
    result=cursor.fetchall()
    titulos=[i[0] for i in cursor.description]
    # print(titulos)
    data={i:[] for i in titulos}
    # print(data)
    for row in result:
        for i,v in enumerate(row):
            data[titulos[i]].append(v)

    df = pd.DataFrame(data)
    ruta=os.path.join('..','DataFrames','Premium.csv')
    df.to_csv(ruta,index=False)

