import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd # read in data quickly
from scipy.ndimage import rotate

pivot_distance = 140 # must be central (in current code), mm units
image_space_size = 600 # 1 pixel = 1 mm (user choice)
angle = [22, 30, 45, 90] # angles other than 0 degrees
distance_over = 401 # number of mm slices produced from imaging app

list_of_folders = ["Run20_Cs", "Run21_Cs", "Run22_Cs", "Run23_Cs", "Run24_Cs"]
slices = np.zeros((image_space_size,distance_over,len(list_of_folders)+1), dtype = np.float64) # store xz slices (float so that when you normalise it can be something other than 0 and 1)

for i, folder in enumerate(list_of_folders):

    print("working folder " + folder)
    folder_location = "./test_data/" + folder # alter this
    files = glob(folder_location + "/slice*")
    image_space = np.zeros((image_space_size,image_space_size,distance_over), dtype = np.int64)

    for file in files:
        index_z = int(file.split("/")[-1].split("_")[1]) # slice to add to numpy array
        slice = pd.read_csv(file, header = None).values.reshape((image_space_size,image_space_size)) # read 600 x 600 array
        image_space[:,:,index_z] = slice # store array as slice in 3D array

    max_y_slice = np.where(image_space == image_space.max())[0][0] # get xz slice
    slices[:,:,i] = image_space[max_y_slice,:,:] # store xz slice in second matrix

for k in range(slices.shape[2]-2):
    tester = slices[:,:,(k+1)]
    flag = 0

    # crop or extend slice depending on position of pivot and number of slices
    if(tester.shape[1] < 2*pivot_distance):
        difference = 2*pivot_distance - tester.shape[1]
        j = np.concatenate(([tester, np.zeros((image_space_size,difference))]), axis = 1)
        flag = 1
    else:
        j = tester[:,0:2*pivot_distance]

    if(k == 0): # for the first combination you add non rotated and first rotated slice
        if(flag == 1):
            slices[:,:,-1] = slices[:,:,0]/(slices[:,:,0].max()) + rotate(input = j/(j.max()), angle = 1*angle[k], reshape = False)[:,0:distance_over]
        else:
            slices[:,:,-1] = slices[:,:,0]/(slices[:,:,0].max()) + np.concatenate(([rotate(input = j/(j.max()), angle = 1*angle[k], reshape = False), np.zeros((image_space_size, tester.shape[1] - 2*pivot_distance))]), axis = 1)
    else: # add next rotated slice to current image
        if(flag == 1):
            slices[:,:,-1] = slices[:,:,-1] + rotate(input = j/(j.max()), angle = 1*angle[k], reshape = False)[:,0:distance_over]
        else:
            slices[:,:,-1] = slices[:,:,-1] + np.concatenate(([rotate(input = j/(j.max()), angle = 1*angle[k], reshape = False), np.zeros((image_space_size, tester.shape[1] - 2*pivot_distance))]), axis = 1)


# alter this to show what you want
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(figsize=(18, 10), ncols = 3, nrows = 2)
p1 = ax1.imshow(slices[:,:,0])
p2 = ax2.imshow(slices[:,:,1])
p3 = ax3.imshow(slices[:,:,2])
p4 = ax4.imshow(slices[:,:,3])
p5 = ax5.imshow(slices[:,:,4])
p6 = ax6.imshow(slices[:,:,-1])
ax1.set_title("angle 0 degrees")
ax2.set_title("angle 22.5 degrees")
ax3.set_title("angle 30 degrees")
ax4.set_title("angle 45 degrees")
ax5.set_title("angle 90 degrees")
ax6.set_title("combined")
cbar1 = fig.colorbar(p1, ax = ax1).minorticks_on()
cbar2 = fig.colorbar(p2, ax = ax2).minorticks_on()
cbar3 = fig.colorbar(p3, ax = ax3).minorticks_on()
cbar4 = fig.colorbar(p4, ax = ax4).minorticks_on()
cbar5 = fig.colorbar(p5, ax = ax5).minorticks_on()
cbar6 = fig.colorbar(p6, ax = ax6).minorticks_on()
plt.show()

#np.savetxt("./Cs.txt", slices[:,:,-1], delimiter = ',') # save data
