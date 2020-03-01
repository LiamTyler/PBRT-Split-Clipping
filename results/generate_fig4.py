import re
import matplotlib.pyplot as plt

files = [
    "SPACESHIP_T_0_TO_20/space_T0_log.txt",
    "SPACESHIP_T_0_TO_20/space_T1_log.txt",
    "SPACESHIP_T_0_TO_20/space_T2_log.txt",
    "SPACESHIP_T_0_TO_20/space_T3_log.txt",
    "SPACESHIP_T_0_TO_20/space_T4_log.txt",
    "SPACESHIP_T_0_TO_20/space_T5_log.txt",
    "SPACESHIP_T_0_TO_20/space_T6_log.txt",
    "SPACESHIP_T_0_TO_20/space_T7_log.txt",
    "SPACESHIP_T_0_TO_20/space_T8_log.txt",
    "SPACESHIP_T_0_TO_20/space_T9_log.txt",
    "SPACESHIP_T_0_TO_20/space_T10_log.txt",
    "SPACESHIP_T_0_TO_20/space_T11_log.txt",
    "SPACESHIP_T_0_TO_20/space_T12_log.txt",
    "SPACESHIP_T_0_TO_20/space_T13_log.txt",
    "SPACESHIP_T_0_TO_20/space_T14_log.txt",
    "SPACESHIP_T_0_TO_20/space_T15_log.txt",
    "SPACESHIP_T_0_TO_20/space_T16_log.txt",
    "SPACESHIP_T_0_TO_20/space_T17_log.txt",
    "SPACESHIP_T_0_TO_20/space_T18_log.txt",
    "SPACESHIP_T_0_TO_20/space_T19_log.txt",
    "SPACESHIP_T_0_TO_20/space_T20_log.txt",
]

files = [
    "SPONZA_T_0_TO_20/sponza_T0_log.txt",
    "SPONZA_T_0_TO_20/sponza_T1_log.txt",
    "SPONZA_T_0_TO_20/sponza_T2_log.txt",
    "SPONZA_T_0_TO_20/sponza_T3_log.txt",
    "SPONZA_T_0_TO_20/sponza_T4_log.txt",
    "SPONZA_T_0_TO_20/sponza_T5_log.txt",
    "SPONZA_T_0_TO_20/sponza_T6_log.txt",
    "SPONZA_T_0_TO_20/sponza_T7_log.txt",
    "SPONZA_T_0_TO_20/sponza_T8_log.txt",
    "SPONZA_T_0_TO_20/sponza_T9_log.txt",
    "SPONZA_T_0_TO_20/sponza_T10_log.txt",
    "SPONZA_T_0_TO_20/sponza_T11_log.txt",
    "SPONZA_T_0_TO_20/sponza_T12_log.txt",
    "SPONZA_T_0_TO_20/sponza_T13_log.txt",
    "SPONZA_T_0_TO_20/sponza_T14_log.txt",
    "SPONZA_T_0_TO_20/sponza_T15_log.txt",
    "SPONZA_T_0_TO_20/sponza_T16_log.txt",
    "SPONZA_T_0_TO_20/sponza_T17_log.txt",
    "SPONZA_T_0_TO_20/sponza_T18_log.txt",
    "SPONZA_T_0_TO_20/sponza_T19_log.txt",
    "SPONZA_T_0_TO_20/sponza_T20_log.txt",
]


triangleCounts = []
renderTimes    = []

for file in files:
    f = open(file)
    txt = f.read()
    triCount = re.findall(r'new_num_shapes:\ (\d*)', txt )[0]
    renderTime = re.findall(r'PBRT_TOTAL_RENDER_TIME\ =\ (\d+.*)s', txt )[0]
    triangleCounts.append(int(triCount))
    renderTimes.append(float(renderTime))

relativeCounts = [ 100 * x / triangleCounts[0] for x in triangleCounts ]
relativeTimes  = [ 100 * x / renderTimes[0] for x in renderTimes ]

xAxis = [ x for x in range(21) ]
lines = plt.plot(xAxis, relativeCounts, 'r', xAxis, relativeTimes, 'g--')
plt.title( "Sponza Atrium (Frame 16)" )
plt.ylabel('Percentage')
plt.xlabel('Threshold')
plt.axis([0, 20, 0, 350])
plt.legend( lines, ["# Triangles %", "Render Time %" ] )
plt.show()
