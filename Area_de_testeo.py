from Laberinto_Seba import *

def resolver_laberinto(algoritmo):
    laberinto = Laberinto(algoritmo)
    laberinto.resolver()

resolver_laberinto("DFS")
resolver_laberinto("BFS")
resolver_laberinto("GBFS")
resolver_laberinto("A*")

