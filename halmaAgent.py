# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:45:32 2019

@author: Aishwarya
"""


from queue import PriorityQueue
from math import sqrt
from datetime import datetime

startTime=datetime.now()

###############################################################################
#taking inputs
file=open("input1.txt", "r")
contents=file.readlines()

mode=contents[0].split()
#print(mode[0])
color=contents[1].split()
#print (color)

time=float(contents[2])
#print (contents[3])

board=[['']*16 for i in range(16)]
for i in range(16):
    row=contents[3+i].split()
    for j in range(16):
        board[i][j]=row[0][j]
        
###############################################################################

#directional vectors
rdv=[-1,-1,-1,0,1,1,1,0]
cdv=[-1,0,1,1,1,0,-1,-1]

#camps
camp_black=[[0,0],[1,0],[0,1], [2,0], [1,1],[0,2],[3,0],[2,1],[1,2],[0,3],
            [4,0],[3,1],[2,2],[1,3],[0,4],[4,1],[3,2],[2,3],[1,4]]
camp_white=[[15,15],[14,15],[15,14],[13,15],[14,14],[15,13],[12,15],[13,14],
            [14,13],[15,12],[11,15],[12,14],[13,13],[14,12],[15,11],[11,14],
            [12,13],[13,12],[14,11]]

list_of_moves=[]
# =============================================================================
# for i in board:
#     print(i)
# =============================================================================

###############################################################################


#finding all valid moves for a pawn
def find_valid_moves(row,column,flag):
    available_moves=[]
    seen=set()
    seen.add((row,column))
    path_list=[]
   
    #finding the hops    
    def hop(row,column,r,c,a,b):
        x=row+r
        y=column+c
        #count=0    
        if not (x<0 or y<0 or x>15 or y>15):
            if board[x][y]=='.' and (x,y) not in seen:
                #print ("next dot",x,y)
                hop_path=[]
                hop_path.append([row-r,column-c])
                hop_path.append([x,y])
                #print ("hop_path",hop_path)
                #print ("path_list....before",path_list)
                path_list.append(hop_path)
                #print ("path_list",path_list)
                
                
                seen.add((x,y))
                for i in range(8):
                    if (rdv[i]==(-r)) and (cdv[i]==(-c)):
                        #print ("going back")
                        #count+=1
                        continue
                        
                    new_row=x+rdv[i]
                    new_column=y+cdv[i]
                    #print ("-----new",new_row,new_column)
                    if not (new_row<0 or new_column<0 or new_row>15 or 
                            new_column>15):
                        if board[new_row][new_column]!='.':
                            #print ("hopping again")
                            hop(new_row,new_column,rdv[i],cdv[i],a,b)
                                    
                    else:
                        continue
                #if check_white_moves(x,y,a,b):
                if color[0]=='WHITE':
                    priority=sqrt(((x-0)**2)+((y-0)**2))
                    p=15-max(abs(x-a),abs(y-b))
                    available_moves.append([p,priority,[x,y],[a,b]])
                        
                else:
                    priority=sqrt(((x-15)**2)+((y-15)**2))
                    p=15-max(abs(x-a),abs(y-b))
                    available_moves.append([p,priority,[x,y],[a,b]])
                    
    
    for i in range(8):
        x=row+rdv[i]
        y=column+cdv[i]
        #print ("------------------")
        #print("inside valid moves",x,y)
        #available_moves=PriorityQueue()
        if not (x<0 or y<0 or x>15 or y>15):
            #adjacent moves
            if board[x][y]=='.':
                #print ("adjacent move")
                path_list.append([[row,column],[x,y]])
                if color[0]=='WHITE':
                    priority=sqrt(((x-0)**2)+((y-0)**2))
                    p=15-max(abs(x-row),abs(y-column))
                    available_moves.append([p,priority,[x,y],[row,column]])
                        
                else:
                    priority=sqrt(((x-15)**2)+((y-15)**2))
                    p=15-max(abs(x-row),abs(y-column))
                    available_moves.append([p,priority,[x,y],[row,column]])
            
            #hop
            else:
                #print ("hopping")
                hop(x,y,rdv[i],cdv[i],row,column)
    
    #print (available_moves.queue)
    if flag==1:
        return path_list
    return available_moves
 
###############################################################################
               

            
def rules(moves,b):
    #print ("----",moves.queue)
    Wc = [b[15][15], b[15][14], b[14][15], b[15][13], b[14][14], b[13][15],
          b[15][12], b[14][13], b[13][14], b[12][15], b[15][11],
          b[14][12], b[13][13], b[12][14], b[11][15],
          b[14][11], b[13][12], b[12][13],
          b[11][14]]
    Bc = [b[0][0], b[0][1], b[1][0], b[0][2], b[1][1],
          b[2][0], b[0][3], b[1][2], b[2][1], b[3][0],
          b[0][4], b[1][3], b[2][2], b[3][1],
          b[4][0], b[1][4], b[2][3],
          b[3][2], b[4][1]]
    refW = [(15, 15), (15, 14), (14, 15), (15, 13), (14, 14), (13, 15), (15, 12), (14, 13), (13, 14),
            (12, 15), (15, 11), (14, 12), (13, 13), (12, 14), (11, 15), (14, 11), (13, 12), (12, 13), (11, 14)]
    refB = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (0, 3), (1, 2), (2, 1), (3, 0), (0, 4), (1, 3),
            (2, 2), (3, 1), (4, 0), (1, 4), (2, 3), (3, 2), (4, 1), ]
    if color[0]=="WHITE":
        own_camp=camp_white
        opponent=camp_black
        mycamp=Wc
        othercamp=Bc
        me='W'
        he='B'
    else:
        own_camp=camp_black
        opponent=camp_white
        mycamp=Bc
        othercamp=Wc
        me='B'
        he='W'
        
    p1=PriorityQueue()
    p2=PriorityQueue()
    p3=PriorityQueue()
    #p4=PriorityQueue()
    for move in range(len(moves.queue)):
        move=moves.get()
        #print ("move",move)
        
        ##moves from own camp
        if othercamp.count(me)>=17:
            if ([move[3][0],move[3][1]] in own_camp):
                #print ("in camp")
                if ([move[2][0],move[2][1]] not in own_camp):
                    #print ("not in camp")
                    if color[0]=='WHITE':
                        if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
                            p1.put(move)
                    else:
                        if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
                            p1.put(move)
                elif [move[2][0],move[2][1]] in own_camp:
                    if color[0]=='WHITE':
                        if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
                            p2.put(move)
                    else:
                        if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
                            p2.put(move)
            
            else:
                if color[0]=='WHITE':
                    if (move[2][0]+move[2][1])<=(move[3][0]+move[3][1]):
                        p3.put(move)
                else:
                    if (move[2][0]+move[2][1])>=(move[3][0]+move[3][1]):
                        p3.put(move)
        else:
            if ([move[3][0],move[3][1]] in own_camp):
                #print ("in camp")
                if ([move[2][0],move[2][1]] not in own_camp):
                    #print ("not in camp")
                    if color[0]=='WHITE':
                        if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
                            p1.put(move)
                    else:
                        if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
                            p1.put(move)
                elif [move[2][0],move[2][1]] in own_camp:
                    if color[0]=='WHITE':
                        if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
                            p2.put(move)
                    else:
                        if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
                            p2.put(move)
            
            else:
                if color[0]=='WHITE':
                    if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
                        p3.put(move)
                else:
                    if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
                        p3.put(move)
            
        
        
# =============================================================================
#         #moves from opponent's camp
#         elif [move[3][0],move[3][1]] in opponent:
#             if [move[2][0],move[2][1]] in opponent:
#                 if color[0]=='WHITE':
#                     if (move[2][0]+move[2][1])<(move[3][0]+move[3][1]):
#                         p4.put(move)
#                 else:
#                     if (move[2][0]+move[2][1])>(move[3][0]+move[3][1]):
#                         p4.put(move)
#             elif [move[2][0],move[2][1]] not in opponent:
#                 continue
#            
#             
#             
#         #moves from outside
#         elif [move[3][0],move[3][1]] not in opponent:
#             p3.put(move)
#         
#         else:
#             print (move)
# =============================================================================
                            
        
    if not p1.empty():
        #print ("p1")
        return p1
    elif not p2.empty():
        #print ("p2")
        return p2
# =============================================================================
#     elif not p3.empty():
#         #print ("p3")
#         return p3
# =============================================================================
    else:
        #print ("p4")
        return p3


###############################################################################            

#find all valid moves
def find_all_moves(b):
    Wc = [b[15][15], b[15][14], b[14][15], b[15][13], b[14][14], b[13][15],
          b[15][12], b[14][13], b[13][14], b[12][15], b[15][11],
          b[14][12], b[13][13], b[12][14], b[11][15],
          b[14][11], b[13][12], b[12][13],
          b[11][14]]
    Bc = [b[0][0], b[0][1], b[1][0], b[0][2], b[1][1],
          b[2][0], b[0][3], b[1][2], b[2][1], b[3][0],
          b[0][4], b[1][3], b[2][2], b[3][1],
          b[4][0], b[1][4], b[2][3],
          b[3][2], b[4][1]]
    refW = [(15, 15), (15, 14), (14, 15), (15, 13), (14, 14), (13, 15), (15, 12), (14, 13), (13, 14),
            (12, 15), (15, 11), (14, 12), (13, 13), (12, 14), (11, 15), (14, 11), (13, 12), (12, 13), (11, 14)]
    refB = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (0, 3), (1, 2), (2, 1), (3, 0), (0, 4), (1, 3),
            (2, 2), (3, 1), (4, 0), (1, 4), (2, 3), (3, 2), (4, 1), ]
 
        
    if color[0]=="WHITE":
        pawn='W'
        other = 'B'
        mycamp = refW
        othercamp = refB
        Mc = Wc
        Oc = Bc
    else:
        pawn='B'

        other = 'W'
        mycamp = refB
        othercamp = refW
        Mc = Bc
        Oc = Wc
    moves=PriorityQueue()
    r_moves=PriorityQueue()
    for i in range(16):
        for j in range(16):
            if b[i][j]==pawn:
                if Oc.count(pawn)>=17:
                    if (i,j) in othercamp:
                        continue
                #print (i,j)
                returned_moves=find_valid_moves(i,j,0)
                #print ("returned",returned_moves)
                #returned_moves=rules(returned_moves)
                #print ("p",returned_moves.queue)
                #returned_moves=rules(returned_moves)
                #print (len(returned_moves))
                for k in returned_moves:
                    moves.put(k)
    #print ("moves",len(moves.queue))
    p_moves=rules(moves,b)
    if(len(p_moves.queue)>15):
        for i in range(15):
            r_moves.put(p_moves.get())
        #print ("pr",len(r_moves.queue))
        return r_moves
    #print ("pr",len(p_moves.queue))
    return p_moves


###############################################################################    
# =============================================================================
# def checkIsolated(b,r,c):
#     rdv = [-1, 1, 0, 0, -1, 1, 1, -1]
#     cdv = [0, 0, 1, -1, 1, 1, -1, -1]
#     for i in range(8):
#         new_r=r+rdv[i]
#         new_c=c+cdv[i]
#         if new_r<0 or new_c<0:
#             continue
#         if new_r>=16 or new_c>=16:
#             continue
#         if b[new_r][new_c]!='.':
#             return 0
# 
#     return 1
# =============================================================================


#evaluation function    
def evaluation(state):
    #print("evaluation")
    evaluation_value=0
    A1,A2,B1,B2=0,0,0,0
    for i in range(16):
        for j in range(16):
            if color[0]=='BLACK':
                
                if state[i][j]=='B':
                    #towards the target
                    A1+=(i-15)**2+(j-15)**2
                    if i!=0  and j!=0:
                        B1+=(i+j)/sqrt(i**2+j**2)
                elif state[i][j]=='W':
                    A2+=(i-0)**2+(j-0)**2
                    if i!=0  and j!=0:
                        B2+=(i+j)/sqrt(i**2+j**2)

                    
            else:
                if state[i][j]=='W':
                    A1+=(i-0)**2+(j-0)**2
                    if i!=0  and j!=0:
                        B1+=(i+j)/sqrt(i**2+j**2)
                elif state[i][j]=='B':
                    A2+=(i-15)**2+(j-15)**2
                    if i!=0  and j!=0:
                        B2+=(i+j)/sqrt(i**2+j**2)
                
                
    evaluation_value=(A2-A1)+(B1-B2)          
    return evaluation_value

###############################################################################

def find_move(board,d):
    
    moves=find_all_moves(board)
    #print (moves.queue)
    #print (d)
    val=1000
    tempjumps=[]
    counterpart=[]
    for i in moves.queue:
        tempjumps.append(i[2])
        counterpart.append(i[3])
    #print(tempjumps)
    ##print(counterpart)
    #print("----")
        
        
    
    Wc = [board[15][15], board[15][14], board[14][15], board[15][13], board[14][14], board[13][15],
          board[15][12], board[14][13], board[13][14], board[12][15], board[15][11],
          board[14][12], board[13][13], board[12][14], board[11][15],
          board[14][11], board[13][12], board[12][13],
          board[11][14]]
        
    Bc = [board[0][0], board[0][1], board[1][0], board[0][2], board[1][1],
              board[2][0], board[0][3], board[1][2], board[2][1], board[3][0],
              board[0][4], board[1][3], board[2][2], board[3][1],
              board[4][0], board[1][4], board[2][3],
              board[3][2], board[4][1]]
    refW = [(15, 15), (15, 14), (14, 15), (15, 13), (14, 14), (13, 15), (15, 12), (14, 13), (13, 14),
        (12, 15), (15, 11), (14, 12), (13, 13), (12, 14), (11, 15), (14, 11), (13, 12), (12, 13), (11, 14)]
    refB = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (0, 3), (1, 2), (2, 1), (3, 0), (0, 4), (1, 3),
            (2, 2), (3, 1), (4, 0), (1, 4), (2, 3), (3, 2), (4, 1), ]

    if color[0] == 'BLACK':
        mySymbol = 'B'
        other = 'W'
        mycamp = refB
        othercamp = refW
        Mc = Bc
        Oc = Wc
    else:
        mySymbol = 'W'
        other = 'B'
        mycamp = refW
        othercamp = refB
        Mc = Wc
        Oc = Bc
    if Oc.count(mySymbol)>=17:
        temprow,tempcol=tempjumps[0][0],tempjumps[0][1]
        ind=0
        for i in range(len(Oc)):
            if Oc[i] == '.':
                rr = othercamp[i][0]
                cc = othercamp[i][1]
                #print("rrcc",rr,cc)
                for j in range(len(tempjumps)):
                    aa = tempjumps[j][0]
                    bb = tempjumps[j][1]
                    newval = sqrt((rr - aa) ** 2 + (cc - bb) ** 2)
# =============================================================================
#                     if (rr,cc)==(aa,bb):
#                         continue
# =============================================================================
                    if newval < val:
                        val = newval
                        temprow = aa
                        tempcol = bb
                        ind=j
                        #print("trtc",temprow,tempcol)
                #jumps.append((temprow, tempcol))
                #print("---------------------------")

                break
        return [0,0,[temprow,tempcol],counterpart[ind]]

    

    
    best_value=float("-inf")
    #print (best_value)
    while not moves.empty():
        move=moves.get()
        
        #make the move
        board[move[2][0]][move[2][1]]=board[move[3][0]][move[3][1]]
        board[move[3][0]][move[3][1]]='.'
        
        #find the value
        value_move=minimax(board,0,False,float("-inf"),float("inf"),d)
        
        #print ("from",move[3][0],move[3][1],"move",move[2][0],move[2][1])
        #print ("value",value_move)
       
        
        #undo the move
        
        board[move[3][0]][move[3][1]]=board[move[2][0]][move[2][1]]
        board[move[2][0]][move[2][1]]='.'
        
        if(value_move>best_value):
            #print("xxxx")
            
            best_move=move
            best_value=value_move
            
    return best_move     
                
 
    
##############################################################################       
#minimax implementation
def minimax(state, depth, isMax, alpha, beta,d):
    moves=find_all_moves(board)
    #moves=rules(p_moves)
# =============================================================================
#     if moves.empty():
#         return float("inf")
# =============================================================================
    if terminal_test(state):
        #print(evaluation(state))
        return evaluation(state)+50
    elif depth==d:
        #print(evaluation(state))
        return evaluation(state)
    
    if isMax:
        best_value=float("-inf")
        while not moves.empty():
            move=moves.get()
            
            #make the move
            board[move[2][0]][move[2][1]]=board[move[3][0]][move[3][1]]
            board[move[3][0]][move[3][1]]='.'
            
            #find the value
            best_value=max(best_value,minimax(board,depth+1,False,alpha,beta,d))
            alpha=max(alpha,best_value)
            
            #undo the move
            board[move[3][0]][move[3][1]]=board[move[2][0]][move[2][1]]
            board[move[2][0]][move[2][1]]='.'
            
            if beta<=alpha:
                break
        #print ("max",best_value)   
        return best_value

    else :
        best_value =float("inf")
        while not moves.empty():
            move=moves.get()
            
            #make the move
            board[move[2][0]][move[2][1]]=board[move[3][0]][move[3][1]]
            board[move[3][0]][move[3][1]]='.'
            
            #find the value
            best_value=min(best_value,minimax(board,depth+1,True,alpha,beta,d))
            alpha=min(alpha,best_value)
            
            #undo the move
            board[move[3][0]][move[3][1]]=board[move[2][0]][move[2][1]]
            board[move[2][0]][move[2][1]]='.'
            
            if beta <= alpha:
                break
        #print ("min",best_value)
        return best_value

###############################################################################

#winning condition
def terminal_test(board):
    if color[0]=="WHITE":
        pawn='W'
        opp_camp=camp_black
    else:
        pawn='B'
        opp_camp=camp_white
    count=0
    for i in opp_camp:
        if board[i[0]][i[1]]==pawn:
            count+=1
    if(count==19):
        return True
    else: return False
 

###############################################################################

#make move
def make_move(move):
    #move=moves.get()
    path=[]
    source=[move[3][0],move[3][1]]
    target=[move[2][0],move[2][1]]
    #print (source)
    path.append(target)
    l=find_valid_moves(source[0],source[1],1)
# =============================================================================
#     for i in l:
#         print (i)
# =============================================================================
    #print (target!=source)
    while(target!=source):
        for i in range(len(l)):
            if (l[i][1]==target):
                path.append(l[i][0])
                target=l[i][0]
                #print (target)
    path=path[::-1]        
    print (path)
    
    #print output
# =============================================================================
#     output=open("output.txt","w")
#     if abs(path[0][0]-path[-1][0])==1 or abs(path[0][1]-path[-1][1])==1:
#         output.write('E')
#         output.write(' ')
#         output.write(str(path[0][1]))
#         output.write(',')
#         output.write(str(path[0][0]))
#         output.write(' ')
#         output.write(str(path[1][1]))
#         output.write(',')
#         output.write(str(path[1][0]))
#     else:
#         for i in range(len(path)-1):
#             output.write('J')
#             output.write(' ')
#             output.write(str(path[i][1]))
#             output.write(',')
#             output.write(str(path[i][0]))
#             output.write(' ')
#             output.write(str(path[i+1][1]))
#             output.write(',')
#             output.write(str(path[i+1][0]))
#             output.write('\n')
#     output.close()
# =============================================================================
    
    #print ("final...... from",move[3][0],move[3][1],"move",move[2][0],move[2][1])
    #print (available_moves.get())
    
    
    
    #print output
    board[move[2][0]][move[2][1]]=board[move[3][0]][move[3][1]]
    board[move[3][0]][move[3][1]]='.' 
    for i in board:
        print (i)
    
###############################################################################


#main function
# =============================================================================
# t_board=board
# temp=camp_black
# pawn='B'
# #moves=PriorityQueue()
# if color[0]=='WHITE':
#     temp=camp_white
#     pawn='W'
# =============================================================================
            
# =============================================================================
# if mode[0]=='SINGLE':
#     all_moves=find_all_moves(board)
#     best_move=all_moves.get()
#     make_move(best_move)
# if mode[0]=='GAME':
#     #print ("here")
#     if time<=1:
#         all_moves=find_all_moves(board)
#         best_move=all_moves.get()
#         make_move(best_move)
#     if time>1 and time<=4:
#         best_move=find_move(board,0)
#         make_move(best_move)
#     if time>4 and time<=6:
#         #print ("here")
#         best_move=find_move(board,1)
#         make_move(best_move)
#     if time>6 and time<=200:
#         best_move=find_move(board,1)
#         make_move(best_move)
#     if time>200:
#         best_move=find_move(board,2)
#         make_move(best_move)
#         
# =============================================================================
        
        
        

    
    
    
    
best_move=find_move(board,1)
#print ("#####",best_move)
#print("from",best_move[3][0],best_move[3][1],"to",best_move[2][0],best_move[2][1])
make_move(best_move)
#print ("#####",best_move)




#print (available_moves.queue)
# =============================================================================
# for i in board:
#     print (i)
# =============================================================================
count=0
while (not terminal_test(board)):
    best_move=find_move(board,1)
    make_move(best_move)
    count+=1
    print (count)
    if color[0]=='WHITE':
        color[0]='BLACK'
    else:
        color[0]="WHITE"
        
print ("no. of moves=",count)
    
        
#writing the output
# =============================================================================
# count=0
# while (not terminal_test('WHITE') or not terminal_test('BLACK')):
#     file=open("input1.txt","w")
#     file.write("GAME\n")
#     file.write("BLACK\n")
#     
#     # =============================================================================
#     # if color[0]=="BLACK":
#     #      file.write("WHITE\n")
#     # else:
#     #      file.write("BLACK\n")
#     # =============================================================================
#     file.write(str(time))
#     file.write("\n")
#     for i in board:
#         file.write("".join(i))
#         file.write("\n")
#     file.close()
# =============================================================================
    #call(["python","homework3_naman.py"])
    #count+=1
#print (count)

# =============================================================================
# print(datetime.now()-startTime)
# =============================================================================
print(datetime.now()-startTime)
