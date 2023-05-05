import copy
#este es el estado inicial, la posición 0 del arreglo almacena las coordenadas del jugador, el resto de posiciones almacenan las coordenadas de las cajas
startingState = [[3,3],[],0,[1,4,0],[3,2,0],[3,4,0],[4,3,0]]
#este es el arreglo con todas las operaciones posibles
operations = [[-1,0,'U'],[0,-1,'L'],[0,1,'R'],[1,0,'D']]
#Se define el arreglo para los casos ya visitados y así no caer en bucles
closed = {}
#estos son los datos del mapa, 'w' representa las paredes, 'g' representa las metas, 'b' representa las cajas y 'p' representa al jugador
# map=[
#     ['w','w','w','x','x','g','w'],
#     ['w','w','w','x','b','w','w'],
#     ['w','w','w','x','x','w','w'],
#     ['w','g','b','p','b','g','w'],
#     ['w','w','w','b','w','w','w'],
#     ['w','w','w','g','w','w','w'],
#     ['w','w','w','w','w','w','w']
#     ]


#Función que determina si una coordenada le corresponde a una caja
def isBox(y,x, state):
  for boxCollection in state:
    for box in boxCollection:
      #print("Caja a evaluar:",box,"Argumentos Y, X: ",y,", ",x)
      if ((y == box[0])and(x == box[1])):
       return True
  return False

#Función que determina si una operación es válida si el jugador no chocaría con una pared
def isValid(operation,state,map):
  #print(state)
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
    #boxes = []
    if isValid(operation,stateBuffer,map):
      #Python me la chupa me la soba, malparida piroba+
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
      #print("Las cajas sin resolver son: ",boxes)
      #print("Player ",newPos)
      for box in boxes:
        boxBuffer = copy.deepcopy(box)
        #si la nueva posición del jugador sería encima de la caja, se aplica la misma operación a la caja para que se mueva con él
        if ((box[0]==newPos[0])and(box[1]==newPos[1])):
          #print([box[0],box[1]])
          #print(operation[1])
          #print([(box[0]+operation[0]),(box[1]+operation[1])])
          box = [(box[0]+operation[0]),(box[1]+operation[1]),0]
          #print("Player ", newPos)
          #print("box ",box)
          #print("box before: ",box)
        ##aquí se levanta la bandera cancelOperation si la caja se movería a un lugar imposible
          if (map[box[0]][box[1]]=='W' or isBox(box[0],box[1],[stateBuffer[3::]])):
            #print([box[0],box[1]])
            cancelOperation = True
            #box = [box[0] - operation[0],box[1] - operation[1],0]
          #aquí se levanta la bandera delete si la caja se movería a una meta
          elif (map[box[0]][box[1]] == 'X'):
            boxes.insert((boxes.index(boxBuffer)),box)
            boxes.remove(boxBuffer)
            stateBuffer[3::] = boxes
            deleteIndex = forCounter
            delete = True
          elif(map[box[0]][box[1]] == '0'):
            stateBuffer[2::boxes.insert((boxes.index(boxBuffer))+1, box)]
            stateBuffer[2::boxes.remove(boxBuffer)]
            ##print(stateBuffer)
        forCounter+=1

      #aquí se borra la caja que se movería a una meta y se convierte esa meta en una pared
      if delete:
        #print("LAS CAJAS SON: ", boxes)
        boxes[deleteIndex][2]=1
        #print(tempgameMap)
        #print(state)
      #print(newPos)a
      #print(state)
      #print([newPos]+state)
      #aquí se añade el estado hijo si la operación fue exitosa
      if not cancelOperation:
        #print("estado", state[1])
        #print("operacion", [operation[2]])
        stateBuffer[1]=stateBuffer[1]+[operation[2]]
        #print ("EL ESTADO ORIGINAL ES: ",state,"EL ESTADO ACTUAL ES:",stateBuffer)
        # ####################################################
        # # Verificar si el estado actual ya está en la lista cerrada
        # state_key = tuple(map(tuple, queue))
        # if state_key in closed:
        #   return None
        
        # # Agregar el estado a la lista cerrada
        # closed[state_key] = True 
        # ####################################################    
        queue.insert(0,[newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
        #print(queue)
  #print("Expanded!")
  return None

#queue = [startingState]
def resultDFS(initialState,map):
  global queue
  queue = [initialState]
  
  while (queue):
      if (isSolution(queue[0])):
          print("Solution Found (DFS)!!!: ", queue[0])
          return queue[0]
          #break
      elif (queue[0][2] > 5):
          queue.pop(0)
      else:
        #print("starting queue: ",queue)
        queueBuffer = copy.deepcopy(queue[0])
        expand(queue[0],map)
        queue.remove(queueBuffer)
            
  print("Solution not found (DFS)  -> Maximum depth reached")
  return [None,"Maximum depth reached"]