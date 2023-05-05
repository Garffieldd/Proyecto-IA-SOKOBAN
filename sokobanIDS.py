import copy
import sys
#este es el estado inicial, la posición 0 del arreglo almacena las coordenadas del jugador, el resto de posiciones almacenan las coordenadas de las cajas
#startingState = [[3,3],[],0,[1,4,0],[3,2,0],[3,4,0],[4,3,0]]
#startingState = [[1,4],[],0,[1,3,0],[2,3,0]]
#startingState = [[3,5],[],0,[2,2,0],[2,3,0],[3,4,0]]
iterativeQueue = []
#este es el arreglo con todas las operaciones posibles
operations = [[-1,0,'U'],[0,-1,'L'],[0,1,'R'],[1,0,'D']]
#estos son los datos del mapa, 'w' representa las paredes, 'g' representa las metas, 'b' representa las cajas y 'p' representa al jugador

# map=[
#   ['w','w','w','w','w','w'],
#   ['w','g','g','b','p','w'],
#   ['w','w','w','b','x','w'],
#   ['w','w','w','x','x','w'],
#   ['w','w','w','w','w','w']
# ]

# map=[
#     ['w','w','w','w','w','w','w'],
#     ['w','w','x','x','x','w','w'],
#     ['w','w','b','b','x','x','w'],
#     ['w','g','g','g','b','p','w'],
#     ['w','w','w','w','w','w','w']
#     ]

# map=[
#     ['w','w','w','w','w','w','w'],
#     ['w','x','x','x','w','p','w'],
#     ['w','x','x','x','g','x','w'],
#     ['w','x','x','b','w','w','w'],
#     ['w','g','x','x','w','w','w'],
#     ['w','w','w','w','w','w','w'],
#     ['w','w','w','w','w','w','w']
#     ]

# map=[
#   ['w','w','w','w','w','w','w'],
#   ['w','g','x','g','b','p','w'],
#   ['w','w','b','w','w','w','w'],
#   ['w','w','g','w','w','w','w'],
#   ['w','w','w','w','w','w','w']
# ]

# map=[
#   ['w','w','w','w','w'],
#   ['w','w','g','w','w'],
#   ['w','w','b','w','w'],
#   ['w','g','g','p','w'],
#   ['w','w','w','w','w']
# ]

# map=[
# ['w','w','w','w','w','w'],
# ['w','x','x','w','p','w'],
# ['w','x','b','b','g','w'],
# ['w','x','x','w','x','w'],
# ['w','x','x','x','x','w'],
# ['w','x','g','x','x','w'],
# ['w','w','w','w','w','w']
# ]

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
            boxes.insert((boxes.index(boxBuffer)), box)
            boxes.remove(boxBuffer)
            stateBuffer[3::] = boxes
        #print(boxes[forCounter])
        forCounter+=1
        

      #aquí se borra la caja que se movería a una meta y se convierte esa meta en una pared
      if delete:
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
        #print(stateBuffer[1][:3:])
        #print(stateBuffer) 
        # if(stateBuffer[1][:11:] == ['L','L','R','R','D','D','L','U','R','U','L']):
        #     print ("EL ESTADO ORIGINAL ES: ",state,"EL ESTADO ACTUAL ES:",stateBuffer)
        if(stateBuffer[2]+1<10):        
          queue.insert(0,[newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
        elif(stateBuffer[2]+1>54):
          break
        else:
          try:
            iterativeQueue[stateBuffer[2]-9].append([newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
          except:
            iterativeQueue.append([])
            iterativeQueue[stateBuffer[2]-9].append([newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
       # print("Estado bufeador chaval ",stateBuffer)
        
        #print(queue)
  #print("Expanded!")
  return None

# def iterativeMode():
#   i = 0
  
#   for j in range(54):
#     k = 0
    
#     print(iterativeQueue)
#     while(iterativeQueue):
      
#       try:
#         if(isSolution(iterativeQueue[i][k])):   
#           print("Solution Found!!! (IDS-iterativequeue): ", iterativeQueue[i][k])
#           answer = iterativeQueue[i][k]
#           return 0
#         else:
#           expand(iterativeQueue[i].pop(0),mapa)
#           iterativeQueue[i].pop(0)
#       except:
#         break       
#       k+=1
#     i+=1
#   return print("Arroz")
#queue = [startingState]
def resultIDS(initialState,map):
  global queue
  global mapa
  queue = [initialState]
  mapa = map
  while (queue):
      if (isSolution(queue[0])):
          print("Solution Found (IDS-result)!!!: ", queue[0])
          return queue[0]
          #sys.exit()
      # elif(answer != None):
      #   return answer
      else:
        #print("starting queue: ",queue)
        queueBuffer = copy.deepcopy(queue[0])
        expand(queue[0],map)
        queue.remove(queueBuffer)
  i = 0
  
  for j in range(54):
    k = 0
    
    #print(iterativeQueue)
    while(iterativeQueue):
      
      try:
        if(isSolution(iterativeQueue[i][k])):   
          print("Solution Found!!! (IDS-iterativequeue): ", iterativeQueue[i][k]) 
          return iterativeQueue[i][k]
        else:
          expand(iterativeQueue[i].pop(k),mapa)
          #iterativeQueue[i].pop(0)
      except:
        break       
      k+=1
    i+=1
  #iterativeMode()
      #   try:
      #     queue.pop(1)
          
      #   except:
      #     #print("hola")
    #     queue.pop(0)









  
