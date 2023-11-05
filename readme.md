
![python](https://img.shields.io/badge/-python%20-yellow?logo=python) ![docker](https://img.shields.io/badge/-docker%20-black?logo=docker) ![redis](https://img.shields.io/badge/-redis%20-white?logo=redis)
![postgres](https://img.shields.io/badge/-postgres%20-blue?logo=postgresql&logoColor=white)

## Acerca de 

Este es un proyecto para mi tiempo libre en el cual aplico todos los nuevos concimientos que voy  sobre 
- Procesamiento de datos
- Analisis de datos 
- ML
para ser aplicados al juego magic the gathering


## [Algoritmos implementados](/algorithms/)
- a-priori -> Se uso para ver las reglas de asociacion entre la legalidad de las cartas entre formatos
- Dijstra (WIP)
- Knn (WIP)

## Diseño Base de datos
![bd](/doc/BD_design.png)
## [Dieño del ETL (WIP)](/data/ETL/)
## Utilidades

para crear migraciones
```sh
alembic revision --autogenerate -m "mensaje"
```

para aplicar migraciones
```sh
alembic upgrade head
```

para conectarse a redis
```sh
alembic upgrade head
```

## Siguientes pasos
- Organizar los notebooks donde se implementan los algoritmos
- Unificar el ETL
