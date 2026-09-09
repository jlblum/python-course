try:
    #throw except if pyfiglet has not been installed. 
    import pyfiglet
    HAVE_PYFIG = True
except ImportError:
    HAVE_PYFIG = False

if HAVE_PYFIG:    
    title_string = pyfiglet.figlet_format("Hello, My name is Jesse")
    print(title_string)

else:
    print("Hello, My name is Jesse")

value1 = 9
value2 = 11

finalValue = value1 * value2
print(value1, "multiplied by", value2 , "equals" , finalValue)