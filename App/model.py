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
from ADT import list as lt
from ADT import orderedmap as tree
from ADT import map as map
from DataStructures import listiterator as it
from datetime import datetime

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    """
    catalog = {'booksTitleTree':None,'yearsTree':None,'booksList':None}
    #implementación de Black-Red Tree (brt) por default
    catalog['booksTitleTree'] = tree.newMap ()
    catalog['booksIdTree'] = tree.newMap ()
    catalog['yearsTree'] = tree.newMap ()
    catalog['booksList'] = lt.newList("ARRAY_LIST")

    return catalog


def newBook (row):
    """
    Crea una nueva estructura para almacenar un libro 
    """
    book = {"book_id": row['book_id'], "title":row['title'], "average_rating":row['average_rating'], "ratings_count":row['ratings_count']}
    return book

def addBookList (catalog, row):
    """
    Adiciona libro a la lista
    """
    books = catalog['booksList']
    book = newBook(row)
    lt.addLast(books, book)

def addBookTree (catalog, row):
    """
    Adiciona libro al tree con key=title
    """
    book = newBook(row)
    catalog['booksTitleTree']  = tree.put(catalog['booksTitleTree'] , book['title'], book, greater)

def newYear (row):
    """
    Crea una nueva estructura para almacenar los libros por año 
    """
    year = strToDate(row['original_publication_year'],'%Y')
    yearNode = {"year": year, "ratingMap":None,}
    yearNode ['ratingMap'] = map.newMap(11,maptype='CHAINING')
    intRating = round(float(row['average_rating']))
    map.put(yearNode['ratingMap'],intRating, 1, compareByKey)
    return yearNode

def addYearTree (catalog, row):
    """
    Adiciona el libro al arbol anual key=original_publication_year
    """
    yearsTree = catalog['yearsTree'] 
    year = strToDate(row['original_publication_year'],'%Y')
    yearNode = tree.get(yearsTree, year, greater)
    if yearNode:
        intRating = round(float(row['average_rating']))
        ratingCount = map.get(yearNode['ratingMap'], intRating, compareByKey)
        if  ratingCount:
            print(ratingCount)
            ratingCount['value']+=1
            map.put(yearNode['ratingMap'], intRating, ratingCount, compareByKey)
        else:
            map.put(yearNode['ratingMap'], intRating, 1, compareByKey)
    else:
        yearNode = newYear(row)
        yearsTree = tree.put(yearsTree, year, yearNode, greater)

# Funciones de consulta


def getBookTree (catalog, bookTitle):
    """
    Retorna el libro desde el mapa a partir del titulo (key)
    """
    return tree.get(catalog['booksTitleTree'], bookTitle, greater)

def rankBookTree (catalog, bookTitle):
    """
    Retorna la cantidad de llaves menores (titulos) dentro del arbol
    """
    return tree.rank(catalog['booksTitleTree'], bookTitle, greater)

def selectBookTree (catalog, pos):
    """
    Retorna la operación select (titulos) dentro del arbol
    """
    return tree.select(catalog['booksTitleTree'], pos) 


# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1

def strToDate(date_string, format):

    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')

