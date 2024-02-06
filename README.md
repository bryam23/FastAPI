#                                           Proyecto Individual: Machine Learning Operations (MLOps)


# Descripcion del proyecto - Contexto

Proyecto se realizo en el marco de la carrera Data Science de SoyHenry donde tomamos el papel de Data Scientists en la plataforma multinacional de videojuegos Steam, donde se emprendio la labor de desarrollar un sistema de recomendacion de videojuegos desde cero. pasando por el proceso de tratamiento, recoleccion de datos, analisis exploratorio de estos hasta el entrenamiento y mantenimiento de dicho modelo de recomendacion con el proposito de deployar una API eficiente para ser consultada.



# Datasets

El equipo SoyHenry proporciono los datasets necesarios para este proyecto.

- Los datos estan conformados por 3 archivos json.gz comprimidos: steam_games.json.gz, user_reviews.json.gz, user_items.json.gz

- Como una manera de simplificar la carga y manipulación de los archivos en VS se decide descomprimir los archivos de manera previa a su utilización, quedando los 3 archivos descomprimidos: output_steam_games.json, australian_user_reviews.json y australian_users_items.json.

- Debido a recursos limitados, no se presentan estos archivos en github, pero tienen acceso a ellos en:  https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj



# Desarrollo del Proyecto

- **ETL (Extraccion, Transformacion y Carga):** en primer lugar, se llevo a cabo la limpieza y formateo inicial del conjunto de datos para asegurar su correcta interpretacion. se aplico el analisis de sentimiento generando asi la columna 'sentiment_analysis', lo que permitio mejorar el rendimiento de la API y facilitar el entrenamiento del modelo de recomendacion. 

- **API:** se creo una interfaz de programación de aplicaciones (API) utilizando FastAPI, que permite realizar diversas consultas a los datos disponibles. Esto facilita la obtención de información sobre desarrolladores, usuarios, géeeros y juegos.

- **DEPLOYMENT:** la interfaz grafica de programacion de aplicaciones (API) esta activa y se puede acceder en linea. se implemento el servicio de Render, siguiendo el tutorial disponible en el repositorio.

- **EXPLORACION DE LOS DATOS:** realizamos un analisis de los datos con el objetivo de obtener una comprension mas profunda de las relaciones entre las diferentes variables en el conjunto de datos. durante este proceso se identificaron outliers, patrones de interes que proporcionan la base para un analisis mas destallado

- **MODELO DE RECOMENDACION:** Creamos el modelo de recomendacion por medio de la propuesta  item-item aplicando la similitud de coseno


# funciones solicitadas para nuestra API

- **def developer( desarrollador : str ):** se ingresa un desarrollador  y debe devolver la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

- **def userdata( User_id : str ):** se ingresa un user_id y debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

- **def UserForGenre( genero : str ):** se ingresa un genero y debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

- **def best_developer_year( año : int ):** se ingresa un año y debe devolver el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)

- **def developer_reviews_analysis( desarrolladora : str ):** se ingresa un desarrollador y debe devolver un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

- **def recomendacion_juego( id de producto ):** se ingresa el id del juego y debe devolver una lista con 5 juegos recomendados similares al ingresado.



# Documentacion

Deploy: https://bryam.onrender.com/docs

Fuente de Datos: https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj