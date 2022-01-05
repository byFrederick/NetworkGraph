from deserealize import *

class graph:
    def __init__(self):
        self.graph = {}
        self.importJsonObj = importJson("C:\Temp\json_data.json")
        self.users = self.importJsonObj.getUsers()
        self.relations = self.importJsonObj.getRelations()
        self.addNode()
        self.addEdge()

    #Método para añadir un nodo al grafo via JSON
    def addNode(self):
        for key in self.users:
            if not self.checkNode(key["id"]):
                self.graph[(key["id"], key["name"])] = []
            else:
                print("El usuario con el id", key["id"], "ya existe")

    #Método para añadir un nodo al grafo manualmente 
    def addNodeManual(self, id, user):
        if not self.checkNode(id):
            self.graph[id, user] = []
            return True
        return False

    #Método para añadir un conexión entre nodos del grafo via JSON 
    def addEdge(self):
        for key in self.relations:
            if self.checkNode(key[0]) and self.checkNode(key[1]):
                if key[1] not in self.graph[key[0], self.userLookup(key[0])] and key[0] != key[1]:
                    self.graph[(key[0], self.userLookup(key[0]))].append(key[1])
                    self.graph[(key[1], self.userLookup(key[1]))].append(key[0])
                else:
                    print("La relación entre los nodos ingresados ya existe || No se puede relacionar un nodo consigo mismo")
            else:
                print("Los nodos o un nodo de los proveídos no existe(n)")

    #Método para añadir un conexión entre nodos del grafo manualmente - ready
    def addEdgeManual(self, node1, node2):
        if self.checkNode(node1) and self.checkNode(node2) and node1 != node2:
            if node2 not in self.graph[node1, self.userLookup(node1)]:
                self.graph[(node1, self.userLookup(node1))].append(node2)
                self.graph[(node2, self.userLookup(node2))].append(node1)
                return True
        return False

    #Método para buscar nombre de usuario con id como parámetro - ready
    def userLookup(self, id):
        for key in self.graph:
            if key[0] == id:
                return key[1]

    #Método para verificar la existencia de un nodo - ready
    def checkNode(self, id):
        return ((id, self.userLookup(id)) in self.graph)

    #Método para verificar la relacion entre dos nodos - ready
    def checkEdge(self, node1, node2):
        if self.checkNode(node1) and self.checkNode(node2):
            return node2 in self.graph[node1, self.userLookup(node1)]
        return False

    #Método para eliminar un nodo del grafo - incomplete
    def deleteNode(self, node):
        if self.checkNode(node):
            for connection in self.graph[node, self.userLookup(node)]:
                self.graph[connection, self.userLookup(connection)].remove(node)
            self.graph.pop((node, self.userLookup(node)))
            return True
        return False             
    

    #Método para eliminar una relación del grafo - incomplete
    def deleteEdge(self, node1, node2):
        if self.checkEdge(node1, node2):
            self.graph[node1, self.userLookup(node1)].remove(node2)
            self.graph[node2, self.userLookup(node2)].remove(node1)
            return True
        return False
    
    def shortestPath(self, source, destination):
        previous = self.bfs(source)
        path = []
        currentNode = destination
        while currentNode != None:
            path.append(currentNode)
            currentNode = previous[currentNode]
            
        path.reverse()
        
        if path[0] == source:
            return path
        return "No existen un camino entre los nodos ingresados"

    def bfs(self, source):
        queue = []
        queue.append(source)
        visited = [False] * len(self.graph)
        visited[source] = True
        
        prev = [None] * len(self.graph)
        while queue:
            node = queue.pop(0)
            adjacencys = self.graph[node, self.userLookup(node)]
            
            for adjacency in adjacencys:
                if not visited[adjacency]:
                    queue.append(adjacency)
                    visited[adjacency] = True
                    prev[adjacency] = node
        return prev
    
    def suggestedRelations(self, node):
        relations = []
        secondRelations = {}
        if self.checkNode(node):
            for relation in self.graph[node, self.userLookup(node)]:
                for secondRelation in self.graph[relation, self.userLookup(relation)]:
                    secondRelations[secondRelation] = secondRelations.get(secondRelation, 0) + 1
            for suggestRelation in secondRelations:
                if secondRelations.get(suggestRelation) > 1:
                    if suggestRelation != node and suggestRelation not in self.graph[node, self.userLookup(node)]:
                        relations.append(suggestRelation)
        else:
            return "El nodo no existe"
        if relations:
            return relations
        else:
            return "No existen sugerencias de relaciones"
    #Método para desplegar el grafo
    def printGraph(self):
        print(self.graph)

