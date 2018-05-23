
[![Build Status](https://travis-ci.org/finiteautomata/contrastes.svg?branch=master)](https://travis-ci.org/finiteautomata/contrastes)

# Contrastes

Detección de palabras contrastivas en Español Argentino utilizando Twitter. Proyecto en colaboración con la Academia Argentina de Letras


## Instalación

1. Clonar proyecto

2. Instalar dependencias

```
$ sudo apt install libhunspell-dev hunspell-es
$ pip install -r requirements
```

3. Bajarse datos:


* [Listado definitivo](https://docs.google.com/spreadsheets/d/1ApWSm2dxU1-AXiN3HiYP_pLCaUhKRciUNm4e_RguGwg/edit#gid=1227749228) Guardar en `data/listado_definitivo.csv`.



## Uso

1. Generar matriz de ocurrencias

```
$ python bin/01_generate_matrices.py
```

Si queremos generar una matriz de "juguete"


```
$ python bin/01_generate_matrices.py --num-files 4 --output-path "output/test.csv"
```

2. Generar listados

```
$ python bin/02_generate_lists.py
```


3. Generar base de datos de contextos

```
$ python bin/03_generate_contexts.py --path-to-tweets /path/to/tweets/
```




## Tests

Para correr los tests, ejecutar:

```
$ nosetests
```
