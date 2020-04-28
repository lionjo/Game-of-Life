# This function takes in an MxNxP array and plots it somehow in a convinient way
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



def showinit(Array,color='gray'):
    shape = np.shape(Array)

    if(len(shape)!=3):
        print("meeeeeh, not the right dimension!")


    w,l,d = shape

    aratio = l/w

    fig = plt.figure(figsize=(5*aratio,5),facecolor='black') 
    ax = plt.subplot(1,1,1)


    ax.imshow(Array[1],cmap ='gray')

    ax.axis('off')
    plt.show()


def animatethisplease(Array,color='gray'):
    shape = np.shape(Array)

    if(len(shape)!=3):
        print("meeeeeh, not the right dimension!")


    w,l,d = shape

    aratio = l/w

    fig = plt.figure(figsize=(5*aratio,5),facecolor='black') 
    ax = plt.subplot(1,1,1)

    ims = []
    for i in range(0,d):
        im = plt.imshow(Array[:,:,i],cmap ='gray',animated=True)
        
        ims.append([im])

    
    ani = animation.ArtistAnimation(fig, ims,repeat=False,interval=200)

   

    fig.tight_layout()
    plt.show()


    ax.axis('off')
    plt.show()


aspectratio = 1.2
size = 40

testarray = np.random.random_integers(0,high=1, size=(40,int(40*aspectratio),100))


animatethisplease(testarray)