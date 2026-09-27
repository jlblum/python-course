#space left here for imports if later needed



pi = 3.14159
radius = 4
height = 10

stringOne = "blue"
stringTwo = "yellow"
stringThree = "red"

stringsList = ["watermelon","orange","cherry","lemon","apple","lime"]

booleanTrue = True
booleanFalse = False


def conCatStrings (string1, string2):   #function accepts two strings as arguments
    total = string1 + " " + string2
    return total

def conCatMultipleStrings (myList):        #function accepts a list of strings for an argument
    fruitString = str()
    for fruit in stringsList:
        fruitString = conCatStrings(fruitString,fruit)
        
    return fruitString.lstrip()            # lstrip removes the leading empty space(s)

def conCatusingJoin(myList) :                     # returns the same conCatMultipleStrings, using join
    seperatorChar = " "
    answer = seperatorChar.join(myList)
    return answer

def surfaceAreaOfaCylinder():       # Area = 2pi(r)(h)+2pi(r^2)
    twoTimesPi = 2 * pi
    answer = twoTimesPi * (radius * height) + twoTimesPi * (radius * radius)
    return answer

def compareStrings(string1,string2):
    return string1 == string2



def main():
    print("The concatenation of two strings, blue + yellow:")
    print(conCatStrings(stringOne,stringTwo)+"\n")

    print("Function takes in a List, and returns a string of concatenated items from the list :")
    print(conCatMultipleStrings(stringsList)+"\n")
    
    print("Function that returns the same concatenation of list items, using Python's join() :")
    print(conCatusingJoin(stringsList)+"\n")

    print("Function that returns the surface area of a Cylinder :")
    print(str(surfaceAreaOfaCylinder())+ "\n")

    print(stringsList[1] + " is equal to "+ stringsList[1] + ":")
    print(str(compareStrings(stringsList[1],stringsList[1])) + "\n")

    print(stringsList[2] + " is equal to "+ stringsList[3] + ":")
    print(str(compareStrings(stringsList[2],stringsList[3]))+ "\n")

    print("Apple is < " + stringsList[5] + " :")
    print("Apple" < stringsList[5])
if __name__ == "__main__":
    main()


