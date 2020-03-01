import re
import matplotlib.pyplot as plt

triangleCounts = [ [], [], [], [] ]
renderTimes    = [ [], [], [], [] ]

Ts = [ 0, 12, 14 ,16 ]
        
for Tindex in range(len(Ts)):
    for frame in range(65):
        logFile    = "SPONZA_ROTATION2/sponza" + str(frame) + "_T" + str(Ts[Tindex]) + "_log.txt"
        f          = open(logFile)
        txt        = f.read()
        triCount   = re.findall(r'new_num_shapes:\ (\d*)', txt )[0]
        renderTime = re.findall(r'PBRT_TOTAL_RENDER_TIME\ =\ (\d+.*)s', txt )[0]
        triangleCounts[Tindex].append(int(triCount))
        renderTimes[Tindex].append(float(renderTime))

xAxis = [ x for x in range(65) ]
lines = plt.plot(xAxis, renderTimes[0], 'r', xAxis, renderTimes[1], 'g--', xAxis, renderTimes[2], 'b--', xAxis, renderTimes[3], 'm--')
plt.title( "Performance" )
plt.ylabel('Frame Time (s)')
plt.xlabel('Frame Nr')
#plt.axis([0, 20, 0, 350])
plt.legend( lines, ["Base", "Threshold 12", "Threshold 14", "Threshold 16" ] )
plt.show()

lines = plt.plot(xAxis, triangleCounts[0], 'r', xAxis, triangleCounts[1], 'g--', xAxis, triangleCounts[2], 'b--', xAxis, triangleCounts[3], 'm--')
plt.title( "Triangle References" )
plt.ylabel('Number of Triangle References')
plt.xlabel('Frame Nr')
#plt.axis([0, 20, 0, 350])
plt.legend( lines, ["Base", "Threshold 12", "Threshold 14", "Threshold 16" ] )
plt.show()
