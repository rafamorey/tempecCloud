'''
#Operadores Aritmeticos
a,b = 10,20
#suma
a + b
#resta
a - b
#multiplicacion
a * b
#divicion
a / b
#Modulo
a % b
#Potencia
a ** 3
#Divicion con entero
a // b
#Operadores Relacionales
a > b
a < b
a >= b
a <= b
a != b
a == b

#Operadores Logicos
# a and b
# a or b 
# a not b

#Operadores de pertenencia
#a = [1,2,3,4,5]
#Esta 3 en la lista a?
# print 3 in a # Muestra True  
#No está 12 en la lista a?
# print 12 not in a # Muestra True
# str = "Hello World"
#Contiene World el string str?
# print "World" in str # Muestra True
#Contiene world el string str? (nota: distingue mayúsculas y minúsculas)
# print "world" in str # Muestra False  
# print "code" not in str # Muestra True

#Operadores de Identidad
a = 3
b = 3  
c = 4
print a is b # muestra True
print a is not b # muestra False
print a is not c # muestra True

x = 1
y = x
z = y
print z is 1 # muestra True
print z is x # muestra True

str1 = "FreeCodeCamp"
str2 = "FreeCodeCamp"

print str1 is str2 # muestra True
print "Code" is str2 # muestra False

a = [10,20,30]
b = [10,20,30]

print a is b # muestra False (ya que las listas son objetos mutables en Python)

'''