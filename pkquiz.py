import os
import random
import math
import typeMatrix as tm

def randomMonoType():
    return tm.types[random.randint(0,len(tm.types) - 1)]

def randomDualType():
    typeOne = randomMonoType()

    typeTwo = randomMonoType()

    while(typeOne == typeTwo):
        typeTwo = randomMonoType()

    return [typeOne, typeTwo]

def typeToIndex(givenType):
    for i, type in enumerate(tm.types):
        if type == givenType:
            return i
    return -1

def getWeakMono(givenType):
    weakList = []
    index = typeToIndex(givenType)
    for i, type in enumerate(tm.types):
        if tm.immunityMatrix[i][index] != 1 and tm.universeMatrix[i][index] == 1:
            weakList.append(tm.types[i])
    print(weakList)
    return weakList

def askWeakMono():
    quizType = randomMonoType()
    key = getWeakMono(quizType)

    question = [quizType, key]

    print(question)

    return question

def getWeakDual(givenType1, givenType2):
    weakList = []
    indexes = [typeToIndex(givenType1), typeToIndex(givenType2)]
    for i, type in enumerate(tm.types):
        if tm.immunityMatrix[i][indexes[0]] != 1 and tm.immunityMatrix[i][indexes[1]] != 1 and tm.universeMatrix[i][indexes[0]] + tm.universeMatrix[i][indexes[1]] > 0:
            weakList.append(tm.types[i])
    print(weakList)
    return weakList

def askWeakDual():
    quizTypes = randomDualType()
    key = getWeakDual(quizTypes[0], quizTypes[1])

    question = [quizTypes, key]

    print(question)

    return question

def askCycleMono(cycle):
    quizType = tm.types[int(cycle) % len(tm.types)]
    key = getWeakMono(quizType)

    question = [quizType, key]

    print(question)

    return question

def askCycleDual(cycle):

    poss = len(tm.types) * len(tm.types) - len(tm.types)
    
    cycle = cycle % poss
    
    rinc = poss // len(tm.types)
    
    row = cycle // rinc
    col = cycle % (len(tm.types) - 1)
    
    if col >= row:
        col += 1

    quizTypes = [tm.types[row], tm.types[col]]
    key = getWeakDual(quizTypes[0], quizTypes[1])

    question = [quizTypes, key]

    print(question)

    return question



