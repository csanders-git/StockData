import numpy as np
import matplotlib.pyplot as plt
import csv
from cycler import cycler

fname = "gen_scatter.csv"
# Read in our data
groups = []
sets = []
with open(fname) as csv_file:
    csv_reader = csv.reader(csv_file)
    inital_row = next(csv_reader)
    x_values = np.array([inital_row[1],inital_row[2],inital_row[3],inital_row[4],inital_row[5],inital_row[6]])
    x_values = [1,2, 3, 4, 5, 6]
    for row in csv_reader:
        if row[0] == "CHG":
            continue
        y_values = np.array([row[1],row[2],row[3],row[4],row[5],row[6]])
        print np.array(y_values)
        groups.append(row[0])
        sets.append((x_values, y_values))

data = tuple(sets)
# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
plt.axhline(y=00, color='r', linestyle='-')

ax.xaxis.tick_top()
x = [1,2, 3, 4, 5, 6]
for data, group in zip(data, groups):
    x, y = data
    ax.scatter(x, y, c=np.random.rand(3,1), edgecolors='none', s=30, label=group)

plt.legend(loc=8, bbox_to_anchor=(0.5, -0.1), ncol=10, fontsize=8)

a = np.arange(6)
print a

plt.title('% Change Since Breach', y=1.07, fontname="Ariel Bold")
plt.ylabel('Stock % change since breach')
#ax.xaxis.set_ticks(a)
plt.xlabel('Market Days since Breach')
my_xticks = ['', 'One Week','Two Weeks','One Month','One Year', 'Two Years', 'Three Years', '']
ax.xaxis.set_ticklabels(my_xticks)

plt.show()
