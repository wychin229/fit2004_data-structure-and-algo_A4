import math


# modified it from lecture codes.
class Graph:
    def __init__(self, vertices_filename, edges_filename):
        file_1 = open(vertices_filename,"r")
        self.my_graph = []
        counter = 0
        # O(V) to add in the vertices
        for lines in file_1:
            lines = lines.strip("\n")
            if counter == 0:  # the first line in vertices file is the number of vertices
                self.my_graph = [None]*int(lines)  # initialise a list with number of vertices
            else:  # start constructing the graph by adding in the vertices
                lines = lines.split(" ")
                ver_id = int(lines[0])
                word = lines[1]
                self.my_graph[ver_id] = Vertex(ver_id, word)
            counter += 1
        # O(E) to add in the edges
        file_2 = open(edges_filename,"r")
        for edges in file_2:
            edges = edges.strip("\n")
            edges = edges.split(" ")
            self.add_edge(int(edges[0]), int(edges[1]))
            self.add_edge(int(edges[1]), int(edges[0]))
        # self.get_graph()  # to get a visualise version of the graph

    def get_graph(self):
        for i in range(len(self.my_graph)):
            print(self.my_graph[i].show_vertex())

    def get_vertex(self, id_num):
        return self.my_graph[id_num]  # 0 is the size of graph

    def add_edge(self, u, v):
        vertex_u = self.get_vertex(u)
        vertex_v = self.get_vertex(v)
        a = vertex_u.get_word()
        b = vertex_v.get_word()
        weight = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                weight += int(math.pow(((ord(a[i]) - 96) - (ord(b[i]) - 96)), 2))

        edge = Edge(vertex_u, vertex_v, weight)
        vertex_u.add_edge(edge)

    def show_queue(self, queue):
        for item in queue:
            print(item.show_vertex())

    def reset_graph(self):
        for i in range(len(self.my_graph)):
            self.my_graph[i].visited = False
            self.my_graph[i].discovered = False
            self.my_graph[i].distance = 0

    def solve_ladder(self, start_vertex, target_vertex):
        # map the distance from the source
        start = 0  # pointer to indicate the first item of queue
        discover_queue = []
        current = self.get_vertex(start_vertex)  # get the starting vertex
        discover_queue.append(current)
        current.discovered = True
        while start < len(discover_queue):
            # when there are vertex that is still not visited(served) in the queue
            """
            !!! to visualise the queue
            for ver in discover_queue:
                if ver is not None and ver.visited != True:
                    print(ver.show_vertex())
                else:
                    print(None)
            print(start)
            """
            current = discover_queue[start]  # i will serve out the first thing and set the as my current
            current.visited = True  # set the visited to true, as i already visited and served this vertex
            for edge in current.edge_list:  # add in newly discovered node
                v = edge.v  # pick the vertex at the other end of the edge ( the vertex linked to current )
                # if the edge is already discovered, mean that the distance is already updated.
                if v.discovered is True:
                    pass
                # if it is not visited or discovered, add to the queue
                elif v.discovered is False:
                    v.distance = current.distance + 1
                    discover_queue.append(v)
                    v.discovered = True
            start += 1  # increment the pointer after i served

        # backtrack from the end point (target)
        end = self.get_vertex(target_vertex)
        path = [end.get_word()]  # the ending point must be the target_vertex
        if target_vertex != start_vertex and end.distance != 0: # if a path can be found
            while end.distance > 0:  # if it needs to traverse through a vertex the distance should be at least 1
                # if my search have not encountered the source yet or the target vertex is not the source
                if end.distance == 1:
                    path.append(self.get_vertex(start_vertex).get_word())
                    break
                for edge in end.edge_list:  # search through the edge_list to find a path that lead to source
                    v = edge.v  # get the vertex connected through this edge
                    # if the distance is -1 smaller than the current it means that it
                    # lead toward the source, as the source is 0
                    if v.distance == end.distance-1:
                        path.append(v.get_word())  # append it to the path
                        end = v  # traverse to the next vertex
            self.reset_graph()  # reset the variable after the search
            path.reverse()  # O(K) for K is the length of the path list
            return path
        elif target_vertex == start_vertex:
            self.reset_graph()  # reset the variable after the search
            return path
        elif target_vertex != start_vertex and end.distance == 0: # you cant get to target from source
            self.reset_graph()  # reset the variable after the search
            return False

    def cheapest_ladder(self, start_vertex, target_vertex, req_char):
        # first, check if any vertex in the graph has the req_char
        if start_vertex == target_vertex and req_char in self.my_graph[start_vertex].get_word():
            return 0, [self.my_graph[start_vertex].get_word()]

        success = False
        # search if there is a vertex with the required character in the graph,
        # if there is, then i might have a path.
        for i in range(len(self.my_graph)):
            if req_char in self.my_graph[i].get_word():
                success = True
                break

        if success is True:
            # have to reset the visited and discovered.
            self.reset_graph()
            self.dijkstra_algo(start_vertex)  # find the shortest path to a vertex that has the required character
            # get the word with the required character which has the shortest path
            shortest_path_to_req_char = None
            shortest = math.inf
            for i in range(len(self.my_graph)):
                if req_char in self.my_graph[i].get_word() and self.my_graph[i].distance < shortest:
                    if self.my_graph[i].distance == 0 and i != start_vertex:
                        continue
                    else:
                        shortest = self.my_graph[i].distance
                        shortest_path_to_req_char = (start_vertex, self.my_graph[i].get_id())

            if shortest_path_to_req_char is not None:
                path_1 = self.backtrack(start_vertex, shortest_path_to_req_char[1])
                if path_1 is False:
                    return False
                path_1[1].reverse()

                self.reset_graph()
                self.dijkstra_algo(shortest_path_to_req_char[1])
                path_2 = self.backtrack(shortest_path_to_req_char[1], target_vertex)

                # if i can manage to find a path to the target
                if path_2 is not False:
                    path_2[1].pop()  # O(1) : pop the last item
                    path_2[1].reverse()
                    total_dis = path_1[0] + path_2[0]
                    result = (total_dis,path_1[1]+path_2[1])
                    self.reset_graph()
                    return result
                else:  # if i cant find a complete path, this fails.
                    return False
            else:  # if a path that involve a vertex with required character is not found, there is no valid path.
                return False
        else:  # there is no vertex that has the req_char
            return success

    def dijkstra_algo(self,source):
        source_queue = MinHeap(len(self.my_graph))  # create a MinHeap with size v, v is the number of vertex
        self.my_graph[source].discovered = True
        source_queue.add_node(0, self.my_graph[source])
        while source_queue.is_empty() is False:  # complexity of O(V)
            min_ver = source_queue.get_min()  # get the min vertex, complexity of O(V)
            min_ver[1].visited = True  # update the status
            for edges in min_ver[1].edge_list:
                if edges.v.discovered is False and edges.v.visited is False:
                    source_queue.add_node(min_ver[0] + edges.w, edges.v)  # add in the children
                    edges.v.discovered = True
                    edges.v.distance = min_ver[0] + edges.w
                    edges.v.sourcever = edges.u

                # if it is already discovered, but no visited, it means that it is still in the queue
                elif edges.v.discovered is True and edges.v.visited is False:
                    item = source_queue.get_item(edges.v)
                    if item is not False:
                        # it means that the item is in the heap
                        if min_ver[0] + edges.w < source_queue.priority_queue[item][0]:
                            # therefore, i might need to update its key
                            source_queue.priority_queue[item][0] = min_ver[0] + edges.w  # update the queue
                            self.my_graph[edges.v.get_id()].distance = min_ver[0] + edges.w  # update the graph
                            self.my_graph[edges.v.get_id()].sourcever = edges.u  # update the source
        # self.get_graph()
    def backtrack(self, source, end):
        path = []
        distance = self.my_graph[end].distance
        current = self.my_graph[end]
        path.append(current.get_word())
        if self.my_graph[end].distance == 0 and source == end:
            # this means that i do not have a route to this target
            return 0, [current.get_word()]
        elif self.my_graph[end].distance == 0 and source != end:
            return False
        while current.get_id() != source:  # traverse until reach the source
            current = current.sourcever
            path.append(current.get_word())
        return distance, path


# modified it from lecture codes.
class Vertex:
    def __init__(self, id, word):
        self.id = id
        self.word = word
        # adjacency list to save edges connected to this vertex
        self.edge_list = []
        self.visited = False  # indicate that is it not visited
        self.discovered = False  # indicate that it is still not in the queue
        self.distance = 0  # it will be renew to 0 every search
        self.sourcever = None  # save the previous vertex that points to it

    def __eq__(self, other):
        if other.id == self.id:
            return True
        else:
            return False

    def show_vertex(self):
        retval = "id:"+str(self.id)+" word:"+self.word+" distance:"+\
                 str(self.distance)+" edges>>> "
        for i in range(len(self.edge_list)):
            retval += "("+self.edge_list[i].show_edge()+")"
        if len(self.edge_list) == 0:
            retval += "No edge"
        if self.sourcever is not None:
            retval += " source vertex: "+str(self.sourcever.get_id())
        return retval

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def get_word(self):
        return self.word

    def get_id(self):
        return self.id


# modified it from lecture codes.
class Edge:
    def __init__(self, u, v, w):
        self.u = u  # first end
        self.v = v  # second end
        self.w = w  # weight of edge

    def show_edge(self):
        return "u:"+str(self.u.get_id())+" v:"+str(self.v.get_id())+" weight:"+str(self.w)


# got the idea from 1008 lecture slides, i modified it myself to make it work in my algorithm
class MinHeap:
    def __init__(self, size):
        self.count = 0
        self.priority_queue = [None]*int(size+1)  # root starts at 1

    def is_empty(self):
        if self.count > 0:
            return False
        else:
            return True

    def get_item(self,other):  # other is a vertex()
        for i in range(1,self.count+1):
            if other == self.priority_queue[i][1]:
                return i

    def add_node(self, key, data):  # key = distance to source, data = vertex()
        item = [key, data]
        self.priority_queue[self.count+1] = item  # put the item in the last position of minheap
        self.count += 1  # update counter
        self.rise(self.count)  # the index of the inserted item

    def rise(self, index):
        while index > 1 and self.priority_queue[index][0] < self.priority_queue[index//2][0]:
            self.swap(index, index//2)
            index //= 2

    def swap(self, current, parent):
        self.priority_queue[current], self.priority_queue[parent] = \
            self.priority_queue[parent], self.priority_queue[current]

    def get_min(self):
        if self.is_empty() is False:
            if self.count > 1:
                self.swap(self.count, 1)  # swap root with last item
                item = self.priority_queue.pop(self.count)  # pop out the last item
                self.count -= 1  # remove last item
                self.sink(1)  # while order is broken, sink from the root
                return item
            else:
                self.count -= 1  # remove last item
                return self.priority_queue[1]  # if there is only one node, just return the root
        else:
            return False

    def smallest_child(self, index):
        # also check if there is only one child
        if 2*index == self.count or self.priority_queue[2*index][0] < self.priority_queue[2*index+1][0]:
            return 2*index
        else:
            return 2*index+1

    def sink(self, index):
        while 2*index <= self.count:
            child = self.smallest_child(index)
            if self.priority_queue[index][0] <= self.priority_queue[child][0]:
                break
            self.swap(child, index)
            index = child

    def show_heap(self):
        print("number of node in heap:",self.count)
        for i in range(1, (self.count+1)//2+1):
            print("parent id:",self.priority_queue[i][1].get_id())
            print("distance from source:", str(self.priority_queue[i][0]))
            if self.priority_queue[i*2] is not None:
                print("left child:", str(self.priority_queue[i*2][1].get_id()))
                print("distance from source:", str(str(self.priority_queue[i*2][0])))
                if self.priority_queue[i*2+1] is not None:
                    print("right child:", str(self.priority_queue[i*2+1][1].get_id()))
                    print("distance from source:", str(str(self.priority_queue[i * 2+1][0])))


if __name__ == "__main__":
    new_graph = Graph("vertices.txt", "edges.txt")
    new_graph.solve_ladder(0,6)
    new_graph.cheapest_ladder(0,6,'c')
    # print(new_graph.solve_ladder(0, 6))
    # print(new_graph.solve_ladder(0, 0))
    # print(new_graph.cheapest_ladder(0,6,'c'))
    # print(new_graph.cheapest_ladder(0,6,'z'))
    # print(new_graph.cheapest_ladder(0,6,'a'))
    # print(new_graph.cheapest_ladder(0, 0, 'a'))
    # new_graph2 = Graph("vertices2.txt", "edges2.txt")
    # print(new_graph2.cheapest_ladder(0,3,'d'))
    # new_graph3 = Graph("vertices3.txt", "edges3.txt")
    # print(new_graph3.cheapest_ladder(0,3,'a'))
    # my_graph = Graph('btext.txt', 'bedge.txt')
    # my_graph1 = Graph('atext1.txt', 'aedge1.txt')
    # #
    # w = open("my_output.txt", 'w')
    # for i in range(8):
    #     for j in range(8):
    #         w.write(str(my_graph.solve_ladder(i, j)) + '\n')
    # for i in range(13):
    #     for j in range(13):
    #         w.write(str(my_graph1.solve_ladder(i, j)) + '\n')
    # # #
    # for i in range(8):
    #     for j in range(8):
    #         for c in ['a', 'b', 'c', 'z']:
    #             w.write(str(my_graph.cheapest_ladder(i, j, c)) + '\n')
    # # #
    # for i in range(13):
    #     for j in range(13):
    #         for c in ['c', 'w', 't', 'p', 's', 'w', 'z']:
    #             w.write(str(my_graph1.cheapest_ladder(i, j, c)) + '\n')
    # w.close()
    # print('done')
    # x = open("my_output.txt")
    # y = open("output.txt")
    # a = []
    # b = []
    # count = 0
    # for line in x:
    #     a.append(line)
    # for line in y:
    #     b.append(line)
    # for i in range(len(a)):
    #     if a[i] != b[i]:
    #         count += 1
    #         print("error",i)
    #         print("a:",a[i]," b:",b[i])
    # x.close()
    # y.close()
    # print(count)
    # print("same")
