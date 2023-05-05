import copy
import sys
#Arreglo de la parte iterativa
iterativeQueue = []
#este es el arreglo con todas las operaciones posibles
operations = [[-1,0,'U'],[0,-1,'L'],[0,1,'R'],[1,0,'D']]
#estos son los datos del mapa, 'w' representa las paredes, 'g' representa las metas, 'b' representa las cajas y 'p' representa al jugador


#Función que determina si una coordenada le corresponde a una caja
def isBox(y,x, state):
  for boxCollection in state:
    for box in boxCollection:
      if ((y == box[0])and(x == box[1])):
       return True
  return False
  

#Función que determina si una operación es válida si el jugador no chocaría con una pared
def isValid(operation,state,map):
  if ((state[0][0]+operation[0]>=len(map)) or (state[0][1]+operation[1]>=len(map[0]))):
    return False
  if ((map[state[0][0]+operation[0]][state[0][1]+operation[1]])=='W'):
    return False
  return True

#Función que determina si un estado es meta, lo hace evaluando si quedan cajas en el estado
def isSolution(state):  
  boxes = state[3::]
  for box in boxes:
    if box[2]==0:
      return False
  return True

def unsolvedBoxes(state):
  boxesList = []
  for box in state:
    if (box[2]==0):
      boxesList.append(box)
  return boxesList

#Función que expande un nodo; hace todas las operaciones válidas al mover al jugador y a las cajas si se puede
def expand(state,map):
  for operation in operations:
    stateBuffer = copy.deepcopy(state)
    if isValid(operation,stateBuffer,map):
      #cancelOperation sirve para abortar la operación si una caja sería movida a un lugar imposible
      cancelOperation = False
      forCounter=0
      #delete se usa para quitar una caja del estado en caso de que se mueva a un lugar de meta
      delete = False
      deleteIndex = 0

      #newPos almacena la que sería la posición del jugador al final de la operación
      newPos = [(stateBuffer[0][0]+operation[0]),(stateBuffer[0][1]+operation[1])]
      #boxes separa las cajas en un arreglo distinto al del jugador
      boxes = stateBuffer[3::]
      for box in boxes:
        boxBuffer = copy.deepcopy(box)
        #si la nueva posición del jugador sería encima de la caja, se aplica la misma operación a la caja para que se mueva con él
        if ((box[0]==newPos[0])and(box[1]==newPos[1])):
          box = [(box[0]+operation[0]),(box[1]+operation[1]),0]
        ##aquí se levanta la bandera cancelOperation si la caja se movería a un lugar imposible
          if (map[box[0]][box[1]]=='W' or isBox(box[0],box[1],[stateBuffer[3::]])):
            cancelOperation = True
        ##las siguientes dos condiciones manejan los casos en que el jugador mueve la caja y la posicion a la que es movida es una meta o un espacio vacio
          elif (map[box[0]][box[1]] == 'X'): 
            boxes.insert((boxes.index(boxBuffer)),box)
            boxes.remove(boxBuffer)
            stateBuffer[3::] = boxes           
            deleteIndex = forCounter
            delete = True
          elif(map[box[0]][box[1]] == '0'):
            boxes.insert((boxes.index(boxBuffer)), box)
            boxes.remove(boxBuffer)
            stateBuffer[3::] = boxes
        forCounter+=1
        

      #aquí se borra la caja que se movería a una meta y se convierte esa meta en una pared
      if delete:
        boxes[deleteIndex][2]=1
      if not cancelOperation:
        stateBuffer[1]=stateBuffer[1]+[operation[2]]
        #Se hace busqueda por profundidad hasta que llegue al inicial 10
        if(stateBuffer[2]+1<10):        
          stack.insert(0,[newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
        elif(stateBuffer[2]+1>54):
          break
        #Una vez llegue a 10 empieza la parte iterativa
        else:
          try:
            iterativeQueue[stateBuffer[2]-9].append([newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
          except:
            iterativeQueue.append([])
            iterativeQueue[stateBuffer[2]-9].append([newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
  return None

# Esta es la funcion principal, recibe el estado inicial y el mapa
def resultIDS(initialState,map):
  global stack
  global mapa
  stack = [initialState]
  mapa = map
  while (stack):
      if (isSolution(stack[0])):
          print("Solution Found (IDS-result)!!!: ", stack[0])
          return stack[0]
      else:
        stackBuffer = copy.deepcopy(stack[0])
        expand(stack[0],map)
        stack.remove(stackBuffer)
  
  #Una vez que el while anterior acabe empieza la parte iterativa donde va aumentando el limite de 1 en 1
  i = 0
  
  for j in range(54):
    k = 0

    while(iterativeQueue):
      
      try:
        if(isSolution(iterativeQueue[i][k])):   
          print("Solution Found!!! (IDS-iterativequeue): ", iterativeQueue[i][k]) 
          return iterativeQueue[i][k]
        else:
          expand(iterativeQueue[i].pop(k),mapa)
      except:
        break       
      k+=1
    i+=1










  
