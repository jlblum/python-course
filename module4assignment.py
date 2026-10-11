# Space for imports if needed
import math

shapeList = ["cube","sphere","pyramid"]
pi = 3.14159
calculations = ["Area","Volume","Mass"]

def shapeSurfaceArea(shape,dim):
    """This function returns the area of a shape."""
    value = int(dim)
    area = 0
    try:
        if shape  == "square":

            area = value * value

        elif shape == "cube":
            area = 6*(value*value)
      
        elif shape == "sphere":
            area = 4*pi*(value*value)

        elif shape == "pyramid":
            volume = shapeVolume(shape,dim)
            basearea = dim * dim
            height = (3*volume)/dim
            slantheight = math.sqrt((height*height)+(dim/2)*(dim/2))
            area = basearea + (1/2 * (4*dim) * slantheight)

        return area
    except:
        print("An error occured while performing calculations.")

def shapeVolume(shape,dim):
    """This function returns the volume of a shape."""

    volume = 0
    try:
        if shape == "cube":
            volume = dim * dim * dim         

        elif shape == "sphere":
            volume = 4/3*(pi*(dim*dim*dim))

        elif shape == "pyramid":
        #height = int(input("Enter the height of the Pyramid")) . 
            volume = (dim * dim)/3                     
                                                        
        return volume
    except:
        print("An error occured while perfoming calculations.")

def shapeMass(volume,density):
    """This function returns the mass of a shape."""
    mass = 0
    try:
        mass = volume * density;

        return mass
    except:
        print("An error occured while performing calculations.")

def shapeCalculate(shape,dim,density):
    """This funcion returns a list containg the results for Area,Volume, and Mass"""
    
    shapeValues = []
    dimension = 0
    if shape == "pyramid":
        dimension = dim[1]    #length of base side of pyramid
    else:
        dimension = dim
    shapeValues.append(shapeSurfaceArea(shape,int(dimension)))
    #print(shapeValues[0])

    shapeValues.append(shapeVolume(shape,dimension))
    #print(shapeValues[1])
    shapeValues.append(shapeMass((shapeValues[1]),density))
    #print("shapeValues")
    return shapeValues

def printResults(solutionsArray):
    """This function prints the results yielded from other functions in this library"""
    print("----------------------------------")
    print("   Results of Calculations Made   ")
    print("----------------------------------")
    print(" " + str(calculations[0]) + " : " + str(solutionsArray[0]))
    print(" " + str(calculations[1]) + " : " + str(solutionsArray[1]))
    print(" " + str(calculations[2]) + " : " + str(solutionsArray[2]))


def main():
    """The main method contains the driver code for this program"""
    print("Please choose the shape you wish to calculate from the list\n")
    #print("Type one of the following - \nSquare\n Cube\n Sphere\n Pyramid")
    shape = input("Type one of the following - \n Square\n Cube\n Sphere\n Pyramid\n : ").lower()
    
   # selection = re.sub(r'[^a-zA-Z0-9]', '', shape)
    #selection = shape.lower

    if shape == "square":
        try:
            length = int(input("Please input the length of one side of the square : "))
            solutions = shapeCalculate(shape,length,0)
            printResults(solutions)
        except ValueError:
            print("Only whole number values accepted")

    elif shape == "cube":
        try:
            length = int(input("Please input the length of one side of the cube : "))
            density = int(input("Input the density of the object's material : "))
            solutions = shapeCalculate(shape,length,density)
            printResults(solutions)
        except ValueError:
            print("Only whole number values accepted")

      
    elif shape == "sphere":
        try:
            length = int(input("Please input the radius measurement of the sphere : "))
            density = int(input("Input the density of the object's material : "))
            solutions = shapeCalculate(shape,length,density)
            printResults(solutions)
        except ValueError:
            print("Only whole number values accepted")
           
    elif shape == "pyramid":
        try:
            length = int(input("Please input the length of one side of the pyramid's base : "))
            height = int(input("Input the height of the pyramid : "))
            density = int(input("Input the density of the object's material : "))
            heightAndLength = []
            heightAndLength.append(height)
            heightAndLength.append(length)
            solutions = shapeCalculate(shape,heightAndLength,density)
            printResults(solutions)
        except ValueError:
            print("Only whole number values accepted")
          
    else:
     print("That is not a valid selection")

main()

