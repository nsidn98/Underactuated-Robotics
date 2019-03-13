import numpy as np

axes = input('Please enter the number of axes: ')
print('Please enter the Matrix in the form :')
print('[Theta , d , a , alpha ]')

dh=[]
for i in range(int(axes)):
    theta = float(input('theta_'+str(i+1)+': '))
    d = float(input('d_'+str(i+1)+': '))
    a = float(input('a_'+str(i+1)+': '))
    alpha = float(input('alpha_'+str(i+1)+': '))
    dh.append(np.array([theta,d,a,alpha]))
    
    
class DH_transform():
    
    def __init__(self,dh):
        self.dh = dh
        
    def link_tf(self):
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
        T_i = T[0]
        for i in range(int(axes)-1):
            T_i = np.dot(T_i,T[i+1])
        return T_i
        
    def coords(self,T):
        pos_vec = T[0:3,-1]
        theta_vec = T[0:3,0:3]
        print('Position vector wrt base:')
        print(pos_vec)
        print()
        print('Orientation Vector wrt base:')
        print(theta_vec)
        
        
DH = DH_transform(dh)
T=DH.link_tf()
tool = DH.tool_base(T)
coords_ = DH.coords(tool)
