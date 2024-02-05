from fastapi import FastAPI
import pandas as pd 

app= FastAPI()


# cargamos los archivos parquet
funcion1=pd.read_parquet('data/developer.parquet')
funcion2=pd.read_parquet('data/userdata.parquet')
funcion3=pd.read_parquet('data/UserForGenre.parquet')
funcion4=pd.read_parquet('data/best_developer_year.parquet')
funcion5=pd.read_parquet('data/developer_reviews_analysis.parquet')



# primera funcion
@app.get('/developer/{desarrollador}')
def developer(desarrollador:str):
    # filtramos dataframe para que solo devuelva la informacion del desarrollador dado
    df_filtrado = funcion1[funcion1['developer'] == desarrollador].copy()

    # agrupamos los datos
    agrupado = df_filtrado.groupby('release_year').agg(
        Cantidad_de_Items=pd.NamedAgg(column='item_id', aggfunc='count'),
        Contenido_Free=pd.NamedAgg(column='price', aggfunc=lambda x: (x == 0).sum())
    )

    # calculamos el porcentaje de los juegos de contenido gratuito
    agrupado['Porcentaje_Contenido_Free'] = (agrupado['Contenido_Free'] / agrupado['Cantidad_de_Items']) * 100

    # formateamos el dataFrame 
    agrupado.reset_index(inplace=True)
    agrupado.rename(columns={'release_year': 'Año'}, inplace=True)
    agrupado['Porcentaje_Contenido_Free'] = agrupado['Porcentaje_Contenido_Free'].map('{:.2f}%'.format)
    return agrupado[['Año', 'Cantidad_de_Items', 'Porcentaje_Contenido_Free']].to_dict(orient='records')




# segunda funcion
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
