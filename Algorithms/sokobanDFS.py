import copy

#################################################33

class HashTable:
 
    # Create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()
 
    def create_buckets(self):
        return [[] for _ in range(self.size)]
 
    # Insert values into hash map
    def set_val(self, key, val):
       
        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size
         
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
 
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
             
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break
 
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))
 
    # Return searched value with specific key
    def get_val(self, key):
       
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
         
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
 
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
             
            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                found_key = True
                break
 
        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:
            return True
        else:
            return False
 
    # Remove a value with specific key
    def delete_val(self, key):
       
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
         
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
 
        found_key = False
        for index, record in enumerate(bucket):
            record_key = record
             
            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return
 
    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)
    

hash_table = HashTable(50)

#este es el arreglo con todas las operaciones posibles
operations = [[-1,0,'U'],[0,-1,'L'],[0,1,'R'],[1,0,'D']]
#Se define el arreglo para los casos ya visitados y así no caer en bucles




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
          elif(hash_table.get_val(str(stack[0]))):
            cancelOperation = True
          elif (map[box[0]][box[1]] == 'X'):
            boxes.insert((boxes.index(boxBuffer)),box)
            boxes.remove(boxBuffer)
            stateBuffer[3::] = boxes
            deleteIndex = forCounter
            delete = True
          elif(map[box[0]][box[1]] == '0'):
            stateBuffer[2::boxes.insert((boxes.index(boxBuffer))+1, box)]
            stateBuffer[2::boxes.remove(boxBuffer)]
        forCounter+=1

      #aquí se borra la caja que se movería a una meta y se convierte esa meta en una pared
      if delete:
        boxes[deleteIndex][2]=1
      if not cancelOperation:        
        stateBuffer[1]=stateBuffer[1]+[operation[2]]                 
        stack.insert(0,[newPos]+[stateBuffer[1]]+[stateBuffer[2]+1]+boxes)
        hash_table.set_val(str(stack[0]), "a")    
  return None

#Funcion principal que recibe el estado inicial y el mapa
def resultDFS(initialState,map):
  global stack
  stack = [initialState]
  
  while (stack):
      if (isSolution(stack[0])):
          print("Solution Found (DFS)!!!: ", stack[0])
          return stack[0]
      #como tiene maximo 64 niveles de profundidad, si se desea que imprima el archivo con el mensaje de maximum depht reached rapido se de debe bajar al 64
      elif (stack[0][2] > 64):
          stack.pop(0)
      else:
        stackBuffer = copy.deepcopy(stack[0])
        expand(stack[0],map)
        stack.remove(stackBuffer)
            
  print("Solution not found (DFS)  -> Maximum depth reached")
  return [None,"Maximum depth reached"]