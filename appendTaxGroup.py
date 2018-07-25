import csv
#import pandas as pd
import os
#import rpy2             

def appendTaxGroup(file):
    trematoda = ['Sm', 'Sj', 'Sh', 'Ov', 'Fh', 'Fg', 'Cs']
    cestoda = ['Mc', 'Ta', 'Ts', 'Tsg', 'Me', 'Em', 'Mv']
    monogenea = ['Nm']
    turbellaria = ['Dj', 'Dr', 'Smd', 'Ml','Dw']
    speciesDict = {'Sm':'Schistosoma_mansoni',
                'Sj':'Schistosoma_japonicum',
                'Sh':'Schistosoma_haematobium',
                'Ov':'Opisthorchis_viverrini',
                'Fh':'Fasciola_hepatica',
                'Fg':'Fasciola_gigantica',
                'Cs':'Clonorchis_sinensis',
                'Ta':'Taenia_asiatica',
                'Ts':'Taenia_solium',
                'Tsg':'Taenia_saginata',
                'Me':'Moniezia_expansa',
                'Em':'Echinococcus_multilocularis',
                'Mv':'Mesocestoides_corti',
                'Nm':'Neobenedenia_melleni',
                'Dj':'Dugesia_japonica',
                'Smd':'Schmidtea_mediterranea',
                'Ml':'Macrostomum_ligano',
                'Dw':'Dugesia_ryukyuensis',
                'error':'error'}
    taxaList = []
    VAPbyTaxaList = []
    VAPbyTaxGroupList = []
    taxaByTaxGroupList = []
    taxGroupDict = {}
    
    with open(file, 'r') as sequenceIDs:
        with open(outputFile, 'w') as characterMap:
            for entry in sequenceIDs:
                if 'VAP' in entry:
                    longHeader = entry.split('_')
                    genus = longHeader[1]
                    species = longHeader[2]
                    taxa = genus + '_' + species
                    taxGroup = longHeader[3]
                    VAPID = longHeader[0]
                elif 'VAL' or 'CRISP' in entry:
                    if 'VAL' in entry:
                        shortTaxaName = entry.split('VAL')[0].strip('_')
                    elif 'CRISP' in entry:
                        shortTaxaName = entry.split('CRISP')[0]
                    else:
                        shortTaxaName = 'error'
                    taxa = speciesDict[shortTaxaName]
                    genus = taxa[0]
                    species = taxa[1]
                    VAPID = entry.strip()
                    
                    if shortTaxaName in trematoda:
                        taxGroup = 'trematoda'
                    elif shortTaxaName in cestoda:
                        taxGroup = 'cestoda'
                    elif shortTaxaName in monogenea:
                        taxGroup = 'monogenea'
                    elif shortTaxaName in turbellaria:
                        taxGroup = 'turbellaria'
                    else:
                        taxGroup = 'error'  
                else:
                    taxa = 'error'
                    taxGroup = 'error'
                entry = entry.strip() + '\t' + VAPID + '\t' + taxa + '\t' + taxGroup + '\n'
                characterMap.write(entry)
                VAPbyTaxGroupList.append(taxGroup)
                VAPbyTaxaList.append(taxa)
                taxGroupDict[taxa] = taxGroup
                if taxa not in taxaList:
                    taxaList.append(taxa)
                    taxaByTaxGroupList.append(taxGroup)
                           
        with open(outputFile, 'r') as characterMap:   
            for entry in characterMap:
                if 'error' in entry:
                    print "There is a problem here:",entry
        
        return taxaList, VAPbyTaxaList, VAPbyTaxGroupList, taxGroupDict, taxaByTaxGroupList
         
def getVAPsummary(file):
    
    VAPcount = len(appendTaxGroup(file)[1])
    taxaCount = len(appendTaxGroup(file)[0])
    VAPbyTaxGroupList = appendTaxGroup(file)[2]
    VAPbyTaxaList = appendTaxGroup(file)[1]
    VAPcountPerTaxGroup = {}
    VAPcountPerTaxa = {}
    taxaByTaxGroupList = appendTaxGroup(file)[4]
    
    print "For {} taxa, you have {} total VAPs.\n".format(taxaCount, VAPcount)
    print "Summary VAP tables:"
    print "  Per taxonomic group is saved at VAPcountPerTaxGroup.csv" 
    print "  Per taxa is saved at VAPcountPerTaxGroup.csv\n"
    
    with open('VAPcountByTaxGroup.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Taxonomic Group'] + ['Number of VAPs expressed'] + ['Number of Taxa'] + ['Avg Num of VAPs expressed/ Taxa'])
        for taxGroup in VAPbyTaxGroupList:
            VAPcountPerTaxGroup[taxGroup] = VAPbyTaxGroupList.count(taxGroup)      
        for taxGroup, count in VAPcountPerTaxGroup.iteritems():
            if taxGroup == "turbellaria":
                numTaxa = taxaByTaxGroupList.count('turbellaria')
            if taxGroup == "cestoda":
                numTaxa = taxaByTaxGroupList.count('cestoda')
            if taxGroup == "monogenea":
                numTaxa = taxaByTaxGroupList.count('monogenea')
            if taxGroup == "trematoda":
                numTaxa = taxaByTaxGroupList.count('trematoda')
            avgNumVAP = count/numTaxa
            writer.writerow([taxGroup.title()] + [count] + [numTaxa] + ['%0.2f' % avgNumVAP])
        avgVAPcount = VAPcount/taxaCount
        writer.writerow(['Total'] + [VAPcount] + [taxaCount] + ['%0.2f' % avgVAPcount])
    
    with open('VAPcountByTaxa.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Taxa'] + ['Number of VAPs expressed'])
        for taxa in VAPbyTaxaList:
            VAPcountPerTaxa[taxa] = VAPbyTaxaList.count(taxa)   
        for taxa, value in VAPcountPerTaxa.iteritems():
            writer.writerow([taxa] + [value])
        writer.writerow(['Total'] + [VAPcount])
    
    return VAPcountPerTaxa, VAPcountPerTaxGroup
 
# def appendSignalPeptidePredictions(file):
#     with open('VAP_Sipley_474_signalP.out', 'r') as SignalP:
#         SignalP = pd.read_table(SignalP)
#         for entry in SignalP:
#             if 'VAP' in entry:
#                 VAPID = entry.split('_')[0]
#     # iterate through rows with PANDAS index

os.chdir("/Users/Breanna/Desktop/currentProjects/VAP_manuscript/revised1/files/tree/class/")
file = "bigTree_allTipLabels.txt"
outputFile = "bigTree_characterMap.txt"

appendTaxGroup(file)   
getVAPsummary(file)


# file2 = 'VAP_Sipley_474_signalP.out'
# SignalP = pd.read_table(file2)  
# Rpython2

