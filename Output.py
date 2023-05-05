from sokobanBFS import resultBFS
from sokobanDFS import resultDFS
from sokobanIDS import resultIDS
import copy

ruta_archivo_entrada = "Entradas/nivel.txt"
ruta_archivo_salida = "Salidas/archivo_salida.txt"

map = []
initialState = []

with open(ruta_archivo_entrada, "r") as archivo_entrada:
  conteo_linea = 0
  for linea in archivo_entrada:
    part = []
    minState = []
    conteo_linea += 1
    for letra in linea.strip():
      if linea[0].isdigit() and int(linea[0]) != 0:
        if(letra != ","):
          minState.append(int(letra))
      else:
          part.append(letra)
    if(minState != []):
      #minState.pop(1)
      #minState1 = [int(x) for x in minState.split(",")]
      initialState.append(minState)

    if(part != []):
     map.append(part)
  initialState.insert(1,[])
  for i in range (2,len(initialState)):
    initialState[i].insert(2,0)
print("Estado inicial",initialState)
print("mapa",map)

initialStateBuffer = copy.deepcopy(initialState)
initialStateBuffer.insert(2,0)

resultSokobanBFS = ''.join(resultBFS(initialState,map)[1])
resultSokobanDFS = ''.join(resultDFS(initialStateBuffer,map)[1])
resultSokobanIDS = ''.join(resultIDS(initialStateBuffer,map)[1])

with open(ruta_archivo_salida, "w") as archivo_salida:
            archivo_salida.write( resultSokobanBFS+"\n"+
                                  resultSokobanDFS+"\n"+
                                  resultSokobanIDS
                                 )