#print([True,7,5.5,1, 'f'])
#print(type([True,7,5.5,1, 'f']))
#print([True,7,5.5,1, 'f'] + [True,7,5.5,1, 'f'])

'''
#LIST CHEATSHEET
#Create
xs = [1,2,3.15,4]
#Index
xs[0] / 1
xs[3] / 4
xs[-1] / 4
#Lenght
leng = len(xs)
#Assignment
xs[0] = 5
#Apend
xs = [1,1]
ys = [3,3]
xs.append(2)
xs = [1,1,2]
xs.append(ys)
xs = [1,1,2,[3,3]]
#Extend
xs.extend(ys)
xs = [1,1,3,3]
#Insert
xs = [1,2]
xs.insert(1,3)
xs = [1,2,3]
#Remove
xs = [1,2,3]
xs.remove(2)
xs = [1,3]
#Slicing
s = 5
st = 15
ste = 2
xs = list(range(20))
print(xs[s:st:ste])
#MinMax/Sum
m = max(xs)
s = sum(xs)
#Sort
xs.sort()
xs = [1,2,3,4,5,6,7,8,9,10]


#Sample
names = []
phones = []
num = 3

for i in range(num):
    name = input("Name: ")
    phone_number = input("Phone Number: ")
    names.append(name)
    phones.append(phone_number)

print("\nNames\t\t\tPhone Numbre\n")
for i in range(num):
    #print(f"{names[i]}\t\t\t{phones[i]}")
    print(names[i] + "\t\t\t" + phones[i])

tearm = input("Term: ")
print("Search Result")

if tearm in names:
    index = names.index(tearm)
    phone_number = phones[index]
    print("Name: " + tearm + " Phone: " + phone_number)
else:
    print("Not found")
'''