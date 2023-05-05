import copy

#este es el arreglo con todas las operaciones posibles
operations = [[-1,0,'U'],[0,-1,'L'],[0,1,'R'],[1,0,'D']]



#Función que determina si hay alguna caja en una coordenada específica
def isBox(y,x, state):
  for boxCollection in state:
    for box in boxCollection:
      if ((y == box[0])and(x == box[1])):
       return True
  return False
  

#Función que determina si una operación es válida (si el jugador no chocaría con una pared, se saldría del mapa o intentaría mover más de una caja a la vez)
def isValid(operation,state,map):
  if ((state[0][0]+operation[0]>=len(map)) or (state[0][1]+operation[1]>=len(map[0]))):
    return False
  if ((map[state[0][0]+operation[0]][state[0][1]+operation[1]])=='W'):
    return False
  if (isBox(operation[0],operation[1],[state[2::]])):
    return False
  return True


#Función que determina si un estado es meta, lo hace evaluando si quedan cajas en el estado que no estén en una meta
def isSolution(state):
  boxes = state[2::]
  for box in boxes:
    if box[2]==0:
      return False
  return True

#Función que devuelve las cajas que no estén en una meta, en un estado.
def unsolvedBoxes(state):
  boxesList = []
  for box in state:
    if (box[2]==0):
      boxesList.append(box)
  return boxesList

#Función que expande un nodo; hace todas las operaciones válidas al mover al jugador y a las cajas si se puede
def expand(state,map):
  #se ejecuta el mismo código para cada una de las posibles operaciones
  for operation in operations:
    #stateBuffer es una copia del estado original, se usa para hacer cambios al estado que se puedan cancelar en medio de la operación
    stateBuffer = copy.deepcopy(state)
    #verifica si la operación a realizar es válida
    if isValid(operation,stateBuffer,map):
      #cancelOperation sirve para abortar la operación si una caja sería movida a un lugar imposible
      cancelOperation = False
      forCounter=0
      #delete se usa para actalizar una caja en el estado en caso de que se mueva a un lugar de meta
      delete = False
      deleteIndex = 0
      #newPos almacena la que sería la posición del jugador al final de la operación
      newPos = [(stateBuffer[0][0]+operation[0]),(stateBuffer[0][1]+operation[1])]
      #boxes separa las cajas sin resolver en un arreglo distinto al del jugador
      boxes = stateBuffer[2::]
      #hace verificaciones para cada caja
      for box in boxes:
        boxBuffer = copy.deepcopy(box)
        #si la nueva posición del jugador sería encima de la caja, se aplica la misma operación a la caja para que se mueva con él
        if ((box[0]==newPos[0])and(box[1]==newPos[1])):
          box = [(box[0]+operation[0]),(box[1]+operation[1]),0]
        ##aquí se levanta la bandera cancelOperation si la caja se movería a un lugar imposible
          if (map[box[0]][box[1]]=='W' or isBox(box[0],box[1],[stateBuffer[2::]])):
            cancelOperation = True
          #aquí se levanta la bandera delete si la caja se movería a una meta
          elif (map[box[0]][box[1]] == 'X'):
            boxes.insert((boxes.index(boxBuffer)),box)
            boxes.remove(boxBuffer)
            stateBuffer[2::] = boxes 
            deleteIndex = forCounter
            delete = True
          #esto es para que la caja no se bugee si entra a un espacio vacio
          elif(map[box[0]][box[1]] == '0'):
            boxes.insert((boxes.index(boxBuffer)), box)
            boxes.remove(boxBuffer)
            stateBuffer[2::] = boxes 
        forCounter+=1

      #aquí se actualiza la caja que se movería a una meta
      if delete:
        boxes[deleteIndex][2]=1
      #aquí se añade el estado hijo a la cola si la operación fue exitosa
      if not cancelOperation: 
        stateBuffer[1]=stateBuffer[1]+[operation[2]]
        queue.append([newPos]+[stateBuffer[1]]+stateBuffer[2::])
  return None

#esta es la función principal, recibe el estado base y el mapa a evaluar
def resultBFS(initialState,map):
  global queue 
  queue = [initialState]
  #este ciclo se encarga de expandir nodos, mientras haya por lo menos 1 en la cola
  while (queue):
      #este condicional se encarga de asegurarse de que no se evalúen más nodos si se llega a la profundidad 64 en el arbol
      #funciona estimando el número de nodos que habrían al llegar a esa profundidad (b^n) y asegurando que hayan menos de esos nodos en la cola
      if (len(queue)>34028237000000000000000000000000000000000):
        return "Maximum depth reached"
      #aquí se evalúa si el primer nodo de la cola es solución
      if (isSolution(queue[0])): 
          print("Solution Found (BFS)!!!: ", queue[0])
          return queue[0]
      #si no es solución, se evalúan las posibles operaciones y se añaden los hijos válidos, posteriormente se elimina este nodo de la cola
      else:
        expand(queue[0],map)
        queue.pop(0)

