from fastapi import FastAPI
import pandas as pd 
app= FastAPI()

'http://127.0.0.1:8000'

funcion2= pd.read_parquet('data/userdata.parquet')

@app.get('/userdata/{user_id}')
def userdata(user_id:str):
    # filtramos el dataframe para obtener solo la informacion del usuario dado 
    df_filtrado = funcion2.loc[funcion2["user_id"]== user_id]
    # contamos la cantidad de items unicos por usuario
    total_items= df_filtrado['item_id'].nunique()
    # calculamos el porcentaje de recomendacion
    porcentaje_recomendacion= round((df_filtrado['recommend'].sum() / total_items) * 100, 2)
    # calculamos la cantidad de dinero que el usuario ha gastado en items
    cantidad_dinero= round((df_filtrado['price'].sum()), 4)
    return {f'usuario':user_id, 'dinero gastado':f'{cantidad_dinero} USD', 'porcentaje de recomendacion':f'{porcentaje_recomendacion}%', 'cantidad de items':total_items}