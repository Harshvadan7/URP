import numpy as np

def createCubeList(filename):
    global vars
    f = open(filename,'r')
    vars = int(f.readline())
    cubes = int(f.readline())

    cubeList = np.zeros((cubes,vars), dtype=int)

    for k in range(cubes):
        line = f.readline()
        line = line.split()
        for i in range(0, len(line)):
            line[i] = int(line[i])

        for i in range(1,int(line[0])+1):
            if(int(line[i])>0):
                cubeList[k][int(line[i])-1] = 1
            else:
                cubeList[k][-1*(int(line[i]))-1] = 10


    for i in range(cubes):
        for j in range(vars):
            if(cubeList[i][j] == 0):
                cubeList[i][j] = 11

    f.close()
    return cubeList

def mostBinate(cubeList):
        
        unate = False

        binNot11 = []
        indexNot11 = []
        indexBinate = []

        bin01 = []
        bin10 = []
        bin11 = []

        unates = []
        binate = []

        binNot11Count = 0
        bin01Count = 0
        bin10Count = 0
        bin11Count = 0

        for j in range(np.size(cubeList,1)):
            for i in range(np.size(cubeList,0)):
                if(cubeList[i][j] == 1):
                    binNot11Count = binNot11Count + 1
                    bin01Count = bin01Count + 1

                if(cubeList[i][j] == 10):
                    binNot11Count = binNot11Count + 1
                    bin10Count = bin10Count + 1
                
                if(cubeList[i][j] == 11):
                    bin11Count = bin11Count + 1
                
            binNot11.append(binNot11Count)
            bin01.append(bin01Count)
            bin10.append(bin10Count)
            bin11.append(bin11Count)
            binNot11Count = 0
            bin01Count = 0
            bin10Count = 0
            bin11Count = 0
        
        for i in range(len(bin11)):
            if((bin01[i] == 0 and bin11[i] != 0) or (bin10[i] == 0 and bin11[i] != 0)):
                unates.append(i)
        
        
        if(len(unates) == len(bin11)):
            unate = True
                    
        if(not(unate)):
           
            for i in range(len(binNot11)):
                if((binNot11[i] == max(binNot11)) and (i not in unates)):
                    indexNot11.append(i)

            if(len(indexNot11)==1):
                x = indexNot11[0]
                #print('x1')

            else:
                for bin01,bin10 in zip(bin01,bin10):
                    binate.append(bin01 - bin10)

                for i in range(len(binate)):
                    if(binate[i]<0):
                        binate[i] = -1*binate[i]
                
                reqBinate = [binate[i] for i in indexNot11]

                for i in indexNot11:
                    if(binate[i] == min(reqBinate)):
                        indexBinate.append(i)

                x = indexBinate[0]
                #print('x2')

        else:
            for i in range(len(binNot11)):
                if(binNot11[i] == max(binNot11)):
                    indexNot11.append(i)

            x = indexNot11[0]
            #print('x3')
    
        return x

def cofactor(cubeList,type,x):

    tempList = []
    for i in range(np.size(cubeList,0)):
        if(type):
            if(cubeList[i][x] == 1):
                tempNP = np.copy(cubeList[i])
                tempList.append(tempNP)
                tempList[-1][x] = 11

            elif(cubeList[i][x] == 11):
                tempList.append(cubeList[i])
            
        else:
            if(cubeList[i][x] == 10):
                tempNP = np.copy(cubeList[i])
                tempList.append(tempNP)
                tempList[-1][x] = 11

            elif(cubeList[i][x] == 11):
                tempList.append(cubeList[i])
    
    return np.array(tempList)


def cubeAND(cubeList,x,type):
    for i in range(np.size(cubeList,0)):
        if(type):
            cubeList[i][x] = 1 
        else:
            cubeList[i][x] = 10 

    
    return cubeList

def cubeOR(PList,NList):
    if(PList.size == 0):
        return NList
    elif(NList.size == 0):
        return PList
    return np.vstack((PList,NList))

def Complement(cubeList):

    if(cubeList.size == 0):
        dontCareList = np.full((1,vars), 11, dtype=int)
        return dontCareList
    
    dontCareList = np.full((1,np.size(cubeList,1)), 11, dtype=int)
    
    for i in range(np.size(cubeList,0)):
        comp = dontCareList == cubeList[i]
        if(comp.all()):
            return np.array([])

    if(np.size(cubeList,0) == 1):
        newList = []
        newCount = 0
        for i in range(np.size(cubeList,1)):
            if(cubeList[0][i] != 11):
                newList.append(np.full(np.size(cubeList,1), 11, dtype=int))
                
                if(cubeList[0][i] == 1):
                    newList[newCount][i] = 10
                elif(cubeList[0][i] == 10):
                    newList[newCount][i] = 1

                newCount = newCount + 1

        return np.array(newList)
    

    else:
        x = mostBinate(cubeList)

        PCubeList = Complement(cofactor(cubeList,True,x))
        NCubeList = Complement(cofactor(cubeList,False,x))

        PCubeList = cubeAND(PCubeList,x,True)
        NCubeList = cubeAND(NCubeList,x,False)
        return (cubeOR(PCubeList,NCubeList))


def writeCubes(cubeList):
    line = []
    line.append(str(cubeList.shape[1]))
    line.append('\n')
    line.append(str(cubeList.shape[0]))
    line.append('\n')

    not11 = 0
    cubeValues = []

    for i in range(cubeList.shape[0]):
        for j in range(cubeList.shape[1]):
            if(cubeList[i][j] == 1):
                not11 = not11 + 1
                cubeValues.append(str(j+1))
     
            elif(cubeList[i][j] == 10):
                not11 = not11 + 1
                cubeValues.append(str(((-1)*(j+1))))

        line.append(str(not11))
        line.append(' ')
        for k in range(not11):
            line.append(cubeValues[k])
            if(k!=not11 - 1):
                line.append(' ')
        #line = [sub[: -1] for sub in line]
        line.append('\n')
        cubeValues.clear()
        not11 = 0

    f = open("output/part1answer.txt",'w')
    f.writelines(line)
    print("The file has been created in the output folder!")


def main():
    filename = 'input/part1.pcn'
    cubeList = createCubeList(filename)
    print("The obtained cubelist is:")
    print(cubeList)
    print('\n')
    compCubeList = Complement(cubeList)
    print("The complemented cubelist is:")
    print(compCubeList)
    print('\n')
    writeCubes(compCubeList)



if __name__ == "__main__":
    main()