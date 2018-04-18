
[![Build Status](https://travis-ci.org/finiteautomata/contrastes.svg?branch=master)](https://travis-ci.org/finiteautomata/contrastes)

# Contrastes

Detección de palabras contrastivas en Español Argentino utilizando Twitter. Proyecto en colaboración con la Academia Argentina de Letras


## Instalación

1. Clonar proyecto

2. Instalar dependencias

```
$ pip install -r requirements
```


## Uso

1. Generar matriz de ocurrencias

```
$ python bin/01_generate_matrices.py
```

Si queremos generar una matriz de "juguete"


```
$ python bin/01_generate_matrices.py --num-files 4 --output-path "output/test.csv"
```


## Tests

Para correr los tests, ejecutar:

```
$ nosetests
```
