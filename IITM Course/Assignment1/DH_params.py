import numpy as np

axes = input('Please enter the number of axes: ')
print('Please enter the Matrix in the form :')
print('Please enter all angles in degrees')
print('[Theta , d , a , alpha ]')

dh=[]
# take user input
for i in range(int(axes)):
    theta = float(input('theta_'+str(i+1)+': '))
    theta = float(np.deg2rad(theta))
    d = float(input('d_'+str(i+1)+': '))
    a = float(input('a_'+str(i+1)+': '))
    alpha = float(input('alpha_'+str(i+1)+': '))
    alpha = float(np.deg2rad(alpha))
    dh.append(np.array([theta,d,a,alpha]))
    
    

class DH_transform():
    '''
    Class for all functions related to the DH parameters
    '''
    def __init__(self,dh):
        self.dh = dh
        
    def link_tf(self):
        '''
        Returns T(k-1 to k)
        '''
        dh = self.dh
        T = []
        for i in range(int(axes)):
            T_i = np.zeros((4,4))
            theta_k = dh[i][0]
            d_k = dh[i][1]
            a_k = dh[i][2]
            alpha_k = dh[i][3]
            # first row
            T_i[0][0] = np.cos(theta_k)
            T_i[0][1] = -np.cos(alpha_k)*np.sin(theta_k)
            T_i[0][2] = np.sin(alpha_k)*np.sin(theta_k)
            T_i[0][3] = a_k*np.cos(theta_k)
            
            # second row
            T_i[1][0] = np.sin(theta_k)
            T_i[1][1] = np.cos(alpha_k)*np.cos(theta_k)
            T_i[1][2] = -np.sin(alpha_k)*np.cos(theta_k)
            T_i[1][3] = a_k*np.sin(theta_k)
            
            # third row
            T_i[2][0] = 0
            T_i[2][1] = np.sin(alpha_k)
            T_i[2][2] = np.cos(alpha_k)
            T_i[2][3] = d_k
            
            # fourth row
            T_i[3][0] = 0
            T_i[3][1] = 0
            T_i[3][2] = 0
            T_i[3][3] = 1
            
            T.append(T_i)
        return T
        
    def inverse_link_tf(self):
        '''
        Returns T(k to k-1)
        '''
        dh = self.dh
        T = []
        for i in range(int(axes)):
            T_i = np.zeros((4,4))
            theta_k = dh[i][0]
            d_k = dh[i][1]
            a_k = dh[i][2]
            alpha_k = dh[i][3]
            # first row
            T_i[0][0] = np.cos(theta_k)
            T_i[0][1] = np.sin(theta_k)#-np.cos(alpha_k)*np.sin(theta_k)
            T_i[0][2] = 0 #np.sin(alpha_k)*np.sin(theta_k)
            T_i[0][3] = -a_k#*np.cos(theta_k)
            
            # second row
            T_i[1][0] = -np.cos(alpha_k)*np.sin(theta_k)
            T_i[1][1] = np.cos(alpha_k)*np.cos(theta_k)
            T_i[1][2] = np.sin(alpha_k)#*np.cos(theta_k)
            T_i[1][3] = -d_k*np.sin(alpha_k)
            
            # third row
            T_i[2][0] = np.sin(alpha_k)*np.sin(theta_k)
            T_i[2][1] = -np.sin(alpha_k)*np.cos(theta_k)
            T_i[2][2] = np.cos(alpha_k)
            T_i[2][3] = -d_k*np.cos(alpha_k)
            
            # fourth row
            T_i[3][0] = 0
            T_i[3][1] = 0
            T_i[3][2] = 0
            T_i[3][3] = 1
            
            T.append(T_i)
        return T
        
        
    def tool_base(self,T):
        '''
        Takes in all the transformation matrices from base to tip
        and returns the base to tip transformation matrix
        '''
        T_i = T[0]
        for i in range(int(axes)-1):
            T_i = np.dot(T_i,T[i+1])
        return T_i
        
    def coords(self,T):
        '''
        Takes in matrix and splits it
        into translation vector and rotation matrix
        '''
        pos_vec = T[0:3,-1]
        theta_vec = T[0:3,0:3]
        print('Position vector wrt base:')
        print(pos_vec)
        print()
        print('Orientation(rotation matrix) Vector wrt base:')
        print(theta_vec)
        
        
DH = DH_transform(dh)
T=DH.link_tf()
print('Transformation matrix from base to elbow')
print(T[0]@T[1])
for i in range(len(T)):
    print("Transformation matrix from link_"+str(i) +' to link_'+str(i+1))
    print(T[i])
tool = DH.tool_base(T)
coords_ = DH.coords(tool)
