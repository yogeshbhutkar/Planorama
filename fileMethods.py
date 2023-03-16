signedInUser = ''


file = open('count.txt','w')
file.write(str(0))
file.close()
f = open('username.txt', 'w')
f.close()

def getCount():
    file = open('count.txt', 'r')
    count = int(file.readline())
    count += 1
    file.close()
    file = open('count.txt','w')
    file.write(str(count))
    return count

def writeFile(string):
    f = open('username.txt', 'w')
    f.write(string)
    f.close()

def readFile():
    f = open('username.txt', 'r')
    return f.readline()