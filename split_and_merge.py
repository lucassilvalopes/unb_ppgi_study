
import numpy as np
import sys

def conver(n,b,m,q):
    """
    
    n: integer in base 10
    b: new base
    m: last level
    q : current level
    
    based on :
    https://stackoverflow.com/questions/47761528
    http://www.cs.trincoll.edu/~ram/cpsc110/inclass/conversions.html
    """
    a = 0
    i = 0
    while n:
        n,r = divmod(n,b)
        a += 10**i * r
        i += 1

    return str(a).zfill(q) + ('0'* (m - q) ) 

def find_x(i_4,n,q):
    """
    i_4 : string in base 4
    n : last level
    q : current level
    """
    s = 0
    for k in range(q):
                
        s += (int(i_4[q - 1 - k]) % 2) * ( 2 ** (n - q + k) )
        
    
    return s 
    
def find_y(i_4,n,q):
    """
    i_4 : string in base 4
    n : last level
    q : current level
    """
    s = 0
    for k in range(q):
        s += (int(i_4[q - 1 - k]) // 2) * ( 2 ** (n - q + k) )

    
    return s 

def find_z(n,q):
    """
    n : last level
    q : current level
    """
    return 2 ** (n - q)

def homogeneity_check(arr, th):
    
    return (np.max(arr) - np.min(arr)) <= 2*th


def split_and_merge_initialization(n, q):

    L = dict()

    for i in range(4**q):
        
        i_4 = conver(i,4,n,q)
        
        x = find_x(i_4,n,q)
        y = find_y(i_4,n,q)
        
        z = find_z(n,q)

        L[i_4] = [x,y,z]

    return n, q, L 
    

def merging(gray, th, n, q, L):

    l = q

    while l > 0:
        
        j = 0
            
        while j < 4**l:
            
            j_0 = conver(j,4,n,l)
            j_1 = conver(j+1,4,n,l)
            j_2 = conver(j+2,4,n,l)
            j_3 = conver(j+3,4,n,l)
                    
            if len(set([L[j_0][2], L[j_1][2], L[j_2][2], L[j_3][2]])) == 1:
                
                x = int(L[j_0][0])
                y = int(L[j_0][1])
                z = int(2*L[j_0][2])
                
                arr = gray[y:(y+z),x:(x+z)]
                
                if homogeneity_check(arr,th):
                    
                    L[j_0][2] = 2* L[j_0][2] 
                    del L[j_1] , L[j_2] , L[j_3]
                
                j = j + 4
            
            else:

                j = j + 4 
                    
        l = l - 1

    return L

def split_and_merge(gray, th = 256 //3):

    N = gray.shape[0]

    n = int( np.log2(N) )

    q = int( np.log2(N) / 2 )

    n, q, L = split_and_merge_initialization(n, q)

    L = merging(gray, th, n, q, L)

    return L


def display_result(gray, L):
    from cv2 import rectangle, namedWindow, imshow, waitKey, destroyAllWindows
    gray_copy = gray.copy()
    gray_copy = np.concatenate([np.expand_dims(gray_copy , axis=2)] * 3, axis = 2)

    for k,v in L.items():
        rectangle(gray_copy,(v[0],v[1]),(v[0]+v[2],v[1]+v[2]), (0,0,255))

    namedWindow("result")
    imshow("result", gray_copy)
    waitKey()
    destroyAllWindows()

def open_img(img_path):
    from cv2 import imread
    gray = imread(img_path,0)
    return gray

if __name__ == "__main__":

    img_path = sys.argv[1]

    gray = open_img(img_path)

    L = split_and_merge(gray)

    display_result(gray, L)