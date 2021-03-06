
import numpy as np
import sys

def conver(n,b,m,q):
    """
    
    n: integer in base 10
    b: new base
    m: last level
    q : current level

    Examples:
        inputs:
            n = 10
            b = 4
            m = 9 
            q = 4
        output:
            002200000

        inputs:
            n = 58
            b = 4
            m = 9 
            q = 4
        output:
            032200000
    
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
        # Take the current level digit, which is q - 1 because of zero based indexing.
        # Take the side of the square at the current level, which is 2**(n-q).
        # Take the mod 2 of the current level digit and multiply by the current level side.
        # The result is the x relative to the x of the parent node.
        # Do the same for the parent node to obtain its x, and so on.
        # Add up all the x values and you get the x value relative to the image origin (0,0).
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
        # Take the current level digit, which is q - 1 because of zero based indexing.
        # Take the side of the square at the current level, which is 2**(n-q).
        # Divide the current level digit by 2 and multiply by the current level side.
        # The result is the y relative to the y of the parent node.
        # Do the same for the parent node to obtain its y, and so on.
        # Add up all the y values and you get the y value relative to the image origin (0,0).
        s += (int(i_4[q - 1 - k]) // 2) * ( 2 ** (n - q + k) )

    
    return s 

def find_z(n,q):
    """
    n : last level
    q : current level
    """
    return 2 ** (n - q) # each level distant from the last doubles the side of the square

def homogeneity_check(arr, th):
    
    return (np.max(arr) - np.min(arr)) <= 2*th


def split_and_merge_initialization(n, q):

    L = dict()

    for i in range(4**q): # 4**q is the total number of nodes in the layer q (root is 0)
        
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
                    L[j_1][2] = L[j_2][2] = L[j_3][2] = 0
                
                j = j + 4
            
            else:

                j = j + 4 
                    
        l = l - 1

    return L


def str_item_assignment(s,i,v):
    l = list(s)
    l[i] = v
    return ''.join(l)

def splitting(gray, th, n, q, L):

    j_0s = [conver(k,4,n,q) for k in range(4**q)]
        
    while len(j_0s) > 0:
        
        j_0 = j_0s.pop(0)

        z = int(L[j_0][2])

        if ( (0 < z) and (z <= 2**(n - q)) ):

            l = q

            while l < n:
                
                if L[j_0][2] == 2**(n - l):

                    x = int(L[j_0][0])
                    y = int(L[j_0][1])
                    z = int(L[j_0][2])

                    arr = gray[y:(y+z),x:(x+z)]

                    if not homogeneity_check(arr,th):

                        j_1 = str_item_assignment(j_0,l,'1') 
                        j_2 = str_item_assignment(j_0,l,'2')
                        j_3 = str_item_assignment(j_0,l,'3')

                        L[j_1] = [0,0,0]
                        L[j_2] = [0,0,0]
                        L[j_3] = [0,0,0]

                        L[j_0][2] = L[j_0][2] // 2 
                        L[j_1][2] = L[j_2][2] = L[j_3][2] = L[j_0][2]

                        L[j_1][0] = L[j_0][0] + L[j_0][2]
                        L[j_2][0] = L[j_0][0]
                        L[j_3][0] = L[j_1][0]

                        L[j_1][1] = L[j_0][1]
                        L[j_2][1] = L[j_0][1] + L[j_0][2]
                        L[j_3][1] = L[j_2][1]

                        j_0s = j_0s + [j_1,j_2,j_3]

                        l = l + 1
                    else:
                        l = n
                else:
                    l = l + 1
    
    return L



def split_and_merge(gray, th):

    N = gray.shape[0]

    n = int( np.log2(N) )

    q = int( np.log2(N) / 2 )

    n, q, L = split_and_merge_initialization(n, q)

    L = merging(gray, th, n, q, L)

    L = splitting(gray, th, n, q, L)

    return L


def visualize_result(gray, L):
    from cv2 import rectangle, namedWindow, imshow, waitKey, destroyAllWindows
    gray_copy = gray.copy()
    gray_copy = np.concatenate([np.expand_dims(gray_copy , axis=2)] * 3, axis = 2)

    for k,v in L.items():
        rectangle(gray_copy,(v[0],v[1]),(v[0]+v[2],v[1]+v[2]), (0,0,255))

    namedWindow("result")
    imshow("result", gray_copy)
    waitKey()
    destroyAllWindows()

    return gray_copy

def open_img(img_path):
    from cv2 import imread
    gray = imread(img_path,0)
    return gray

def save_img(gray):
    from cv2 import imwrite
    imwrite("output.jpg", gray)
    return gray

if __name__ == "__main__":

    img_path = sys.argv[1]

    th = int(sys.argv[2])

    gray = open_img(img_path)

    L = split_and_merge(gray, th)

    gray = visualize_result(gray, L)

    save_img(gray)