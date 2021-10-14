from flask import Flask, render_template, request, redirect
import math
import time
import pymysql

app = Flask(__name__)


@app.route("/")
def hello():
    conn = pymysql.connect("localhost", "root", "", "dsa_project")
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor4 = conn.cursor()
    
    sqlFetchQuery = "select * from output_info order by executionTime asc"
    sqlFetchQuery1 = "select * from output_info1 order by executionTime1 asc"
    sqlFetchQuery2 = "select * from output_info2 order by executionTime2 asc"
    sqlGetTimeOfExecQuery = "select * from selfTime order by test_id"
    
    noOfVerticesList = []
    noOfEdgesList = []
    executionTimeList = []

    noOfVerticesList1 = []
    noOfEdgesList1 = []
    executionTimeList1 = []

    noOfVerticesList2 = []
    noOfEdgesList2 = []
    executionTimeList2 = []

    aStarSelfTime = []
    bellmanFordSelfTime = []
    floydSelfTime = []

    percentageList = []
    try:
        cursor.execute(sqlFetchQuery)
        cursor1.execute(sqlFetchQuery1)
        cursor2.execute(sqlFetchQuery2)
        cursor4.execute(sqlGetTimeOfExecQuery)
        
        results = cursor.fetchall()
        results1 = cursor1.fetchall()
        results2 = cursor2.fetchall()
        results4 = cursor4.fetchall()
        
        for row in results:
            noOfVerticesList.append(row[1])
            noOfEdgesList.append(row[2])
            executionTimeList.append(int(row[3] * (math.pow(10, 6))))

        for row1 in results1:
            noOfVerticesList1.append(row1[1])
            noOfEdgesList1.append(row1[2])
            executionTimeList1.append(int(row1[3] * (math.pow(10, 6))))

        for row2 in results2:
            noOfVerticesList2.append(row2[1])
            noOfEdgesList2.append(row2[2])
            executionTimeList2.append(int(row2[3] * (math.pow(10, 6))))
            
        for eachColVal in results4:
            aStarSelfTime.append(eachColVal[1])
            bellmanFordSelfTime.append(eachColVal[2])
            floydSelfTime.append(eachColVal[3])

        percentageCorrectQuery = "select * from (select round(avg(aStar)*100) 'Correct percentage of A*', round(avg(bellman)*100) 'Correct percentage of Bellman', round(avg(floyd)*100) 'Correct percentage of Floyd' from correctNess lol) lol;"
        cursor3.execute(percentageCorrectQuery)
        tempPercentageList = cursor3.fetchall()
        #for x in tempPercentageList:
            #tp = list(x)
            #for y in range (len(x)):
                #if ord(tp[y]) < 48 and ord(tp[y]) > 57:
                    #del tp[y]
            #tp = "".join(tp)
            #percentageList.append(tp)
        print(aStarSelfTime, bellmanFordSelfTime, floydSelfTime)

    except:
        print("Unable to fetch")
    return render_template("home.html", v=noOfVerticesList, e=noOfEdgesList,t=executionTimeList, l=len(noOfEdgesList), v1=noOfVerticesList1, e1=noOfEdgesList1,t1=executionTimeList1, l1=len(noOfEdgesList1)
                           ,v2=noOfVerticesList2, e2=noOfEdgesList2,t2=executionTimeList2, l2=len(noOfEdgesList2), percentageList= tempPercentageList, aStarSelfTime = aStarSelfTime, bellmanFordSelfTime = bellmanFordSelfTime, floydSelfTime = floydSelfTime)




@app.route('/mainPageFormValidation', methods=['GET'])
def check():
    n = request.args['algo_n']
    print(n)
    if(n=="Astar"):

        start_time = time.time()

        def get_neighbours(graph, v):
            neighbourTuple = tuple()
            for x in range(len(graph[v])):
                if graph[v][x] != 0:
                    neighbourTuple = neighbourTuple + ((x, graph[v][x]),)
            return neighbourTuple

        def aStar(graph, source, destination):
            open_set = set()
            open_set.add(int(source))
            closed_set = set()
            g = {}
            parents = {}
            g[source] = 0
            parents[source] = source
            flag = 0
            finalN = None
            while len(open_set) > 0:
                n = None
                for v in open_set:  # minimum f among unvisited nodes
                    if n == None or g[v] + Heu_dist[v] < g[n] + Heu_dist[n]:
                        n = v

                if n == destination or graph[n] == None:
                    pass
                else:
                    for m in get_neighbours(graph, n):  # get neighbours and update g() and parents
                        if (m[0] not in open_set) and (m[0] not in closed_set):
                            open_set.add(int(m[0]))
                            parents[m[0]] = n
                            g[m[0]] = g[n] + m[1]
                        else:
                            if g[m[0]] > g[n] + m[1]:
                                g[m[0]] = g[n] + m[1]
                                parents[m[0]] = n

                                if m[0] in closed_set:
                                    closed_set.remove(m[0])
                                    open_set.add(int(m[0]))
                if n == None:
                    return None

                if n == destination:
                    flag = 1
                    finalN = n

                open_set.remove(n)
                closed_set.add(n)
            if flag == 1:
                path = []
                n = finalN
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                path.append(source)
                path.reverse()
                return (path, g[finalN])
            else:
                return None

        Heu_dist = {}
        n = int(request.args['n_r'])
        tempHeu = list(request.args['heuristics'].split(' '))
        print(len(tempHeu))
        print(tempHeu)

        for eachHeuristic in range(len(tempHeu)):
            Heu_dist[eachHeuristic] = int(tempHeu[eachHeuristic])

        graph = []
        tpGraph = request.args['adjMat']
        print(tpGraph)
        arr = tpGraph.split("\n")
        print(arr)
        for i in range(n):
            tempArr = [int(s) for s in arr[i].split()]
            graph.append(tempArr)
        noOfPaths = 0

        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] != 0:
                    noOfPaths += 1

        source = int(request.args['source'])
        destination = int(request.args['destination'])

        shortestPath, costOfShortestPath = aStar(graph, source, destination)

        if shortestPath is None:
            print('\nPath does not exist !')
        # else:
        #     for x in shortestPath:
        #         print(x)
        #     print ("\n"+str(costOfShortestPath))

        execTime = time.time() - start_time
        print("Execution time:" + str(execTime))

        conn = pymysql.connect("localhost", "root", "", "dsa_project")
        cursor = conn.cursor()

        sqlFetchQuery = "select * from output_info order by executionTime asc"
        noOfVerticesList = []
        noOfEdgesList = []
        executionTimeList = []
        noOfPathsList = []

        try:
            cursor.execute(sqlFetchQuery)
            results = cursor.fetchall()
            for row in results:
                noOfVerticesList.append(row[1])
                noOfPathsList.append(row[2])
                executionTimeList.append(row[3])
            print(noOfVerticesList, "\n", noOfPathsList, "\n", executionTimeList)
        except:
            print("LOL")

        sqlInsertion = "INSERT INTO output_info ( noOfVertices, noOfPaths, executionTime) VALUES (%s, %s, %s)"
        val = (n, noOfPaths, execTime)
        try:
            cursor.execute(sqlInsertion, val)
            conn.commit()
            arr = ['Number of vertices', 'Heuristics', 'Adjacency matrix', 'Source', 'Destination']
            return render_template('/outputFile.html', form_data=request.args, inputLabels=arr, graph=graph,
                                   shortestPath=shortestPath, costOfShortestPath=costOfShortestPath)
        except:
            conn.rollback()
            return redirect('/?failure=1')



    if(n=="Bellman"):
        start_time = time.time()
        v=int(request.args['n_r'])
        edn = int(request.args['n_n'])
        src=int(request.args['source'])

        graph = []
        tpGraph = request.args['adjMat']
        arr = tpGraph.split("\n")
        for i in range(edn):
            tempArr = [int(s) for s in arr[i].split()]
            graph.append(tempArr)

        #def bellman_ford(graph, src,v,edn):
        dist = [float("Inf")] * v
        dist[src] = 0
        for j in range(v):
            for i in range(edn):
                s=graph[i][0]
                d=graph[i][1]
                w=graph[i][2]
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
        execTime = time.time() - start_time
        print(execTime)
        conn = pymysql.connect("localhost", "root", "", "dsa_project")
        cursor = conn.cursor()
        sqlInsertion = "INSERT INTO output_info1 ( noOfVertices1, noOfPaths1, executionTime1) VALUES (%s, %s, %s)"
        val = (v, edn, execTime)
        cursor.execute(sqlInsertion, val)
        conn.commit()

        return render_template('/outputFile1.html', v=v,edn=edn,src=src,gr=graph,dis=dist)


    if(n=="Floyed"):
        start_time = time.time()
        n = int(request.args['n_r'])
        e = int(request.args['n_n'])
        graph = []
        tpGraph = request.args['adjMat']
        arr = tpGraph.split("\n")
        for i in range(n):
            tempArr = [int(s) for s in arr[i].split()]
            graph.append(tempArr)

        distance = list(map(lambda i: list(map(lambda j: j, i)), graph))

        # Adding vertices individually
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

        execTime = time.time() - start_time
        print(distance)
        print(execTime)
        conn = pymysql.connect("localhost", "root", "", "dsa_project")
        cursor = conn.cursor()
        sqlInsertion = "INSERT INTO output_info2 ( noOfVertices2, noOfPaths2, executionTime2) VALUES (%s, %s, %s)"
        val = (n, e, execTime)
        cursor.execute(sqlInsertion, val)
        conn.commit()

        return render_template('/outputFile2.html', n=n, e=e,d=distance,g=graph)

if __name__ == '__main__':
    app.run(debug=True)
