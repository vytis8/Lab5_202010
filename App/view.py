"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller 
import csv
from ADT import list as lt
from ADT import orderedmap as map
from DataStructures import listiterator as it

import sys


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Laboratorio 5")
    print("1- Cargar información")
    print("2- Buscar libro por llave (titulo) ")
    print("3- Consultar cuantos libros hay alfabeticamente menores a una llave (titulo) - (rank)")
    print("4- Buscar un libro por posición de la llave (titulo) - (select)")
    print("5- Consultar la cantidad de libros por rating para un año (YYYY) dado")
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)


"""
Menu principal 
""" 
def main():
    while True: 
        printMenu() 
        inputs =input('Seleccione una opción para continuar\n')
        if int(inputs[0])==1:
            print("Cargando información de los archivos ....")
            print("Recursion Limit:",sys.getrecursionlimit())
            catalog = initCatalog ()
            loadData (catalog)
            print ('Tamaño Lista libros cargados: ' + str(lt.size(catalog['booksList'])))
            print ('Tamaño árbol Libros por titulo: ' + str(map.size(catalog['booksTitleTree'])))
            print ('Tamaño árbol Libros por año : ' + str(map.size(catalog['yearsTree'])))
            print ('Altura árbol por titulo: ' + str(map.height(catalog['booksTitleTree'])))
            print ('Altura árbol por año: ' + str(map.height(catalog['yearsTree'])))
            print(catalog)
            
        elif int(inputs[0])==2:
            title = input("Nombre del titulo a buscar: ")
            book = controller.getBookTree(catalog,title)
            if book:
                print("Libro encontrado:",book['title'],book['average_rating'])
            else:
                print("Libro No encontrado")
        elif int(inputs[0])==3:
            title = input("Nombre del titulo a buscar (rank): ")
            rank = controller.rankBookTree(catalog,title) 
            print("Hay ",rank," titulos menores (rank) que "+title)
        elif int(inputs[0])==4:
            pos = int(input("Posición del k-esimo titulo del libro (select) a obtener: "))
            book = controller.selectBookTree(catalog, pos)
            if book:
                print("Libro en posición:",pos,":",book['value']['title'],book['value']['average_rating'])
            else:
                print("Libro no encotrado en posicion: ",pos)
        elif int(inputs[0])==5:
            year = input("Ingrese el año a consultar:")
            response = controller.getBookByYearRating(catalog, year) 
            if response:
                print(response)
            else:
                print("No se encontraron libro para el año",year)   
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    #sys.setrecursionlimit(11000)
    main()