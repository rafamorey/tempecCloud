#Comentario
'''
Comentario
Comentario

def func(x, y = [4,2]):
    print(y)
    y.append(x)
    return y
print(func(1,[3,2]))

from pytube import YouTube
link = input("Enter link: ")
video = YouTube(link)
stream = video.streams.get_highest_resolution()
stream.download()

int1 = 10
int2 = 6
if int != 14:
    int2 = ++int1
    print(int1 - int2)

n = 8
ascii = 65
for i in range(n):
    print((n-i-1)*" ", end="")
    for j in range(0, i+1):
        print(chr(ascii), end=" ")
        ascii+=1
    print()

def fun():
    print('fun')
print(fun())
#fun none, when a function does not have return it will always return none

a = [0,1,2,3]
print("= " + str(a[-1]))
print(a)
for a[-1] in a:
    print(a)
    print(a[-1])
'''
#print(100//5*100/5) #400
