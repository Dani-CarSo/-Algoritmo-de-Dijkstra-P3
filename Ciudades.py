import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
 
#  Red de ciudades, rutas y posiciones
CIUDADES = [
    "CDMX", "Puebla", "Querétaro", "Morelia",
    "León", "San Luis", "Guadalajara",
    "Aguascalientes", "Zacatecas", "Torreón",
    "Saltillo", "Monterrey",
]
 
RUTAS = [
    ("CDMX",        "Puebla",          135),
    ("CDMX",        "Querétaro",       215),
    ("CDMX",        "Morelia",         302),
    ("Querétaro",   "León",             90),
    ("Querétaro",   "San Luis",        195),
    ("Querétaro",   "Guadalajara",     360),
    ("León",        "Guadalajara",     155),
    ("León",        "Aguascalientes",  103),
    ("León",        "Morelia",         170),
    ("San Luis",    "Zacatecas",       190),
    ("San Luis",    "Monterrey",       500),
    ("San Luis",    "Saltillo",        460),
    ("Guadalajara", "Aguascalientes",  147),
    ("Guadalajara", "Zacatecas",       290),
    ("Aguascalientes","Zacatecas",     120),
    ("Zacatecas",   "Torreón",         280),
    ("Zacatecas",   "Saltillo",        330),
    ("Torreón",     "Monterrey",       330),
    ("Saltillo",    "Monterrey",        86),
]
 
# Posiciones 
POS = {
    "CDMX":           (-99.1,  19.4),
    "Puebla":         (-98.2,  19.0),
    "Querétaro":      (-100.4, 20.6),
    "Morelia":        (-101.2, 19.7),
    "León":           (-101.7, 21.1),
    "San Luis":       (-100.9, 22.1),
    "Guadalajara":    (-103.3, 20.7),
    "Aguascalientes": (-102.3, 21.9),
    "Zacatecas":      (-102.6, 22.8),
    "Torreón":        (-103.4, 25.5),
    "Saltillo":       (-101.0, 25.4),
    "Monterrey":      (-100.3, 25.7),
}