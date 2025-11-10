import time
frame = 2
stime = 5
window_width = frame * stime

array  = [[0]] * window_width
print(len(array))
print(array)
subarray = [[1,2,3,4], [5,6,7,8]]
lock = 1
i =0
j = 0
while lock:
    
        i = (i%window_width)
        print('i: ', i)
        if(j==0):
            array[i] = input('add: ') #trocar input por função de captura de frame
        else:
            array = array[1:window_width] + [input('add: ')] #trocar input por função de captura de frame
        print('array :', i, '\n',array,'\n')
        i = i+1
        if(i >= window_width):
             j=1