import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as nm
from scipy import stats
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
mpl.use('TkAgg')  # I added this line as a fix to a Matplotlib error


def getFileNames():
    """Returns the names of the input files"""
    files = os.listdir("evaluated")
    # files = filter(lambda ob: ".txt" in ob, files)
    return files

names = []
mapValues = []
p10Values = []
RPrecValues = []

# open every file in the cvrp directory and give the data to the class Problem to read and elaborate
for inputFile in getFileNames():
	# data = nm.loadtxt('input/' + inputFile)
	f = open('evaluated/' + inputFile)
	names.append(inputFile[:-4])
	data = f.read()
	currentMaps = re.findall(r'^map .*', data, flags=re.MULTILINE)
	currentMaps = [float(e.split('\t')[2]) for e in currentMaps]

	# insert in list line with map
	del currentMaps[-1]  # remove last map value from list (all)
	mapValues.append(currentMaps)

	currentRPrec = re.findall(r'^Rprec .*', data, flags=re.MULTILINE)
	currentRPrec = [float(e.split('\t')[2]) for e in currentRPrec]
	del currentRPrec[-1]
	RPrecValues.append(currentRPrec)

	currentP10 = re.findall(r'^P_10 \D.*', data, flags=re.MULTILINE)
	currentP10 = [float(e.split('\t')[2]) for e in currentP10]
	del currentP10[-1]
	p10Values.append(currentP10)

print('Mean values')
print('Run \t\t Map \t Rprec \t P_10')
for i in range(len(names)):
	print('{}\t {:.4f}\t {:.4f}\t {:.4f}'.format(names[i], float(nm.mean(mapValues[i])), float(nm.mean(RPrecValues[i])), float(nm.mean(p10Values[i]))))

print()
f, p = stats.f_oneway(mapValues[0], mapValues[1], mapValues[2], mapValues[3])
print('One-way ANOVA')
print('=============')
print('Map')
print('F value:', f)
print('P value:', p, '\n')

f, p = stats.f_oneway(RPrecValues[0], RPrecValues[1], RPrecValues[2], RPrecValues[3])
print('RPrec')
print('F value:', f)
print('P value:', p, '\n')

f, p = stats.f_oneway(p10Values[0], p10Values[1], p10Values[2], p10Values[3])
print('Precision 10')
print('F value:', f)
print('P value:', p, '\n')

maps = nm.array(mapValues)
plt.boxplot([maps[0], maps[1], maps[2], maps[3]], vert=True, labels=[names[0], names[1], names[2], names[3]])
plt.title("Distributions of MAPs")
plt.xlabel("MAP")
plt.tight_layout()
plt.savefig("./figures/distr_maps.png")
plt.savefig("./figures/distr_maps.pdf")
plt.clf()

rprecs = nm.array(RPrecValues)
plt.boxplot([rprecs[0], rprecs[1], rprecs[2], rprecs[3]], vert=True, labels=[names[0], names[1], names[2], names[3]])
plt.title("Distributions of Rprecs")
plt.xlabel("Rprec")
plt.tight_layout()
plt.savefig("./figures/distr_rprecs.png")
plt.savefig("./figures/distr_rprecs.pdf")
plt.clf()

p10s = nm.array(p10Values)
plt.boxplot([p10s[0], p10s[1], p10s[2], p10s[3]], vert=True, labels=[names[0], names[1], names[2], names[3]])
plt.title("Distributions of Precision 10")
plt.xlabel("Precision 10")
plt.tight_layout()
plt.savefig("./figures/distr_p10.png")
plt.savefig("./figures/distr_p10.pdf")
plt.clf()

# needed for `pairwise_tukeyhsd`
names2 = nm.repeat(names[0], 50)
names2 = nm.append(names2, nm.repeat(names[1], 50))
names2 = nm.append(names2, nm.repeat(names[2], 50))
names2 = nm.append(names2, nm.repeat(names[3], 50))

# reshaping for `pairwise_tukeyhsd`
maps.shape      = (200,)
rprecs.shape    = (200,)
p10s.shape  = (200,)


alpha           = .05
tukey_maps      = pairwise_tukeyhsd(maps, names2, alpha)
tukey_rprecs    = pairwise_tukeyhsd(rprecs, names2, alpha)
tukey_precs_10  = pairwise_tukeyhsd(p10s, names2, alpha)

# print tables
print()
print(tukey_maps.summary())
print()
print(tukey_rprecs)
print()
print(tukey_precs_10)
print()

# saving plots
tukey_maps.plot_simultaneous(names[0], xlabel='MAP').savefig("./figures/tukey_map.png")
tukey_maps.plot_simultaneous(names[0], xlabel='MAP').savefig("./figures/tukey_map.pdf")
tukey_rprecs.plot_simultaneous(names[0], xlabel='Rprec').savefig("./figures/tukey_rprec.png")
tukey_rprecs.plot_simultaneous(names[0], xlabel='Rprec').savefig("./figures/tukey_rprec.pdf")
tukey_precs_10.plot_simultaneous(names[0], xlabel='Precision 10').savefig("./figures/tukey_p_10.png")
tukey_precs_10.plot_simultaneous(names[0], xlabel='Precision 10').savefig("./figures/tukey_p_10.pdf")
