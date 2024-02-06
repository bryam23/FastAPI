from fastapi import FastAPI
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

app= FastAPI()


# cargamos los archivos parquet
funcion1=pd.read_parquet('data/developer.parquet')
funcion2=pd.read_parquet('data/userdata.parquet')
funcion3=pd.read_parquet('data/UserForGenre.parquet')
funcion4=pd.read_parquet('data/best_developer_year.parquet')
funcion5=pd.read_parquet('data/developer_reviews_analysis.parquet')
modelo_recomendacion=pd.read_parquet('data/modelo_render.parquet')




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



# tercera funcion
@app.get('/UserForGenre/{genero}')
def UserForGenre(genero:str):
  # filtramos dataframe para obtener la informacion del genero especificado
  generos = funcion3[funcion3['genres'].str.contains(genero)]

  # encontramos al usuario con mas horas jugadas aplicando funcion lambda
  usuario_max_horas = generos.assign(
    total_horas=lambda x: x['playtime_forever'].groupby(x['user_id']).transform('sum')
  ).sort_values('total_horas', ascending=False).iloc[0]['user_id']

  # Obtenemos las horas jugadas por año
  horas_por_año = generos.groupby('release_year')['playtime_forever'].sum().reset_index(name='Horas')
  horas_por_año= horas_por_año.rename(columns={'release_year':'Año'})
  # Convertir a una lista de diccionarios
  horas_lista = horas_por_año.to_dict('records')

  
  return {
    "Usuario con más horas jugadas para Género " + genero: usuario_max_horas,
    "Horas jugadas": horas_lista
  }



# cuarta funcion
@app.get('/best_developer_year/{year}')
def best_developer_year(year: int):
    # filtramos dataframe para obtener solo las recomendaciones del año dado
    df_filtrado= funcion4[(funcion4['release_year']== year) & (funcion4['recommend']==True)]
    # contamos las recomendaciones por desarrollador
    conteo_recomendaciones= df_filtrado['developer'].value_counts()
    # obtenemos top 3 de los desarrolladores
    top_3_best_developers= conteo_recomendaciones.nlargest(3).index.tolist()
    return [{'Puesto 1':top_3_best_developers[0], 'Puesto 2':top_3_best_developers[1], 'Puesto 3':top_3_best_developers[2]}]




# quinta funcion
@app.get('/developer_reviews_analysis/{desarrolladora}')
def developer_reviews_analysis(desarrolladora:str):
    # filtramos dataframe para obtener solo la informacion del desarrollador dado
    df_filtrado= funcion5[funcion5['developer']==desarrolladora]
    # contamos la cantidad de reseñas para cada tipo de sentimiento 
    sentiment_count = df_filtrado['sentiment_analysis'].value_counts().to_dict()
    # resultado a devolver
    resultado= {desarrolladora: ['Negativo: ' + str(sentiment_count.get(0,0)), 'Positivo:' + str(sentiment_count.get(2,0))]}
    return resultado




# sexta funcion
@app.get('/recomendacion_juego/{id}')
def recomendacion_juego(id: int):
    
    # verificamos si el juego con game_id existe en el dataframe
    game = modelo_recomendacion[modelo_recomendacion['item_id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # obtenemos el indice del juego dado
    idx = game.index[0]

    # tomamos una muestra aleatoria del dataframe
    sample_size= 2000  # definimos el tamaño de la muestra (ajusta según sea necesario)
    df_sample = modelo_recomendacion.sample(n=sample_size, random_state=42)  # ajustamos la semilla aleatoria segun sea necesario

    # calculamos la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_recomendacion.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # obtenemos las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # ordenamos los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # obtenemos los 5 juegos mas similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # lista de los juegos similares (solo nombres)
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}