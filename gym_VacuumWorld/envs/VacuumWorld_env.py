import gym
from gym import error, spaces, utils
from gym.utils import seeding

from random import sample
from random import random
from random import randint
from random import seed

from gym_VacuumWorld.envs.board import Board

LEFT = 0
FORWARD = 1
RIGHT = 2
VACUUM = 3
OFF = 4


class VacuumWorldEnv(gym.Env):

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self,N,
                 p_dirt=0.5,
                 p_furn=0.01,
                 facing='right',
                 display=None,
                 delay=0.2,):

        self.display=display
        self.delay=delay
        self.size=(N,N)
        self.p_dirt=p_dirt
        self.p_furn=p_furn
        self.facing=facing

        self.reward=None

        self.action_space=spaces.Discrete(5)

        self.observation_space=spaces.Tuple((
                spaces.MultiDiscrete((N*N)*[2]), # Board
                spaces.Discrete(N*N), # row
                spaces.Discrete(N*N), # col
        ))

        self.reset()

    def Forward(self):
        self.move_count=self.move_count+1;

        self.reward=-1

        self.cmd='Forward';
        new_col=self.col
        new_row=self.row;
        if (self.direc==0):
            new_col=new_col+1;
        elif (self.direc==90):
            new_row=new_row-1;
        elif (self.direc==180):
            new_col=new_col-1;
        elif (self.direc==270):
            new_row=new_row+1;
            
            
        if (new_row<0) | (new_row>=self.size[0]) | (new_col<0) | (new_col>=self.size[1]):
            self.agent_touched=True;
        elif self.room[new_row,new_col]==2:  # furniture
            self.agent_touched=True;
        else:
            self.agent_touched=False;
            self.row=new_row;
            self.col=new_col;
    
        
    def Left(self):

        self.reward=-1
        
        self.agent_touched=False
        self.move_count=self.move_count+1;
        self.cmd='Left';
        self.direc=self.direc+90;
        if (self.direc>=360):
            self.direc=0;
        
    def Right(self):

        self.reward=-1
        
        self.agent_touched=False
        self.move_count=self.move_count+1;
        self.cmd='Right';
        self.direc=self.direc-90;
        if (self.direc<0):
            self.direc=270;


    def Vacuum(self):

        self.reward=-1
        
        self.agent_touched=False
        self.move_count=self.move_count+1;
        self.cmd='Vacuum';
        if (self.room[self.row,self.col]==1):
            self.room[self.row,self.col]=0
            self.reward=100

    def Off(self):
            
        dirt=[x for x in self.room if x==1]
        self.cmd='Off'
        
        if not self.AtHome:
            self.reward=-1000-sum(dirt)*100
        else:
            self.reward=-1-sum(dirt)*100

       

    def step(self, action):
        actions={0:self.Left,1:self.Forward,2:self.Right,3:self.Vacuum,4:self.Off}
        actions[action]()

        state=tuple(self.room.board),self.row,self.col
        reward=self.reward
        done=1 if self.cmd=='Off' else 0
        info={}

        return state,reward,done,info


    def reset(self):
        self.room=Board(*self.size)

        if self.p_furn<1:
            for i in range(len(self.room)):
                if self.room[i]==0 and (random()<self.p_furn):
                    self.room[i]=2
        else:        
            r=[]
            for i in range(1,len(self.room)):
                if self.room[i]==0:
                    r.append(i)
            idx=sample(r,int(self.p_furn))               
            for i in idx:
                self.room[i]=2
        
        if self.p_dirt<1:
            for i in range(len(self.room)):
                if self.room[i]==0 and (random()<self.p_dirt):
                    self.room[i]=1
        else:
            r=[]
            for i in range(1,len(self.room)):
                if self.room[i]==0:
                    r.append(i)
            idx=sample(r,int(self.p_dirt))               
            for i in idx:
                self.room[i]=1
        
        self.room[0]=0
        self.move_count=0
        self.agent_touched=False
        
        self.row=0
        self.col=0
        
        direcs={'right':0,'left':180,'up':90,'down':270,'rand':int(random()*4)*90}
        self.direc=direcs[self.facing]
        
        self.cmd=''
        self.msg=''


    def render(self, mode='human'):
        board=Board(*self.room.shape)
        board.pieces=['.','*','X','>','^','<','V','*>','*^','<*','*V']
        for i in range(len(board)):
            board[i]=self.room[i]
            
        d=board[self.row,self.col]
        
        if (self.direc==0):
            board[self.row,self.col]=3+4*d
        elif (self.direc==90):
            board[self.row,self.col]=4+4*d
        elif (self.direc==180):
            board[self.row,self.col]=5+4*d
        elif (self.direc==270):
            board[self.row,self.col]=6+4*d
        
        if mode=='human':
            print(board)
        else:        
            return(str(board))

    @property
    def AtHome(self):
        return ((self.row==0) & (self.col==0))
            
    @property
    def IsDirt(self):
        return (self.room[self.row,self.col]==1)

    @property
    def Touched(self):
        return (self.agent_touched)

    def close(self):
        pass

