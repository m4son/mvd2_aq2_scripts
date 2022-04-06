#!/usr/bin/python3

import re
import sys

if len(sys.argv) < 2:
	print("USAGE: MVDscoreboard.py DEMONAME.MVD2")
	sys.exit()


with open(sys.argv[1],'rb') as file:
    datafile = file.readlines()
    
matchScoreboard = 0
matchLine = 0
matchRounds = 0

for line in datafile:
	if b' Score - ' in line:
		scoreLine = matchLine - 1
		#print(scoreLine)
		#print(line)

	if b'Current score' in line:
		matchRounds += 1

	if b'Team Player          Time Ping Kills Deaths Damage Acc' in line:
		matchScoreboard = matchLine
		#print(matchScoreboard)
		#print(datafile[matchScoreboard])

	matchLine += 1


	#print(line)


players = re.findall(b" (\d.)\s+(...............)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",datafile[matchScoreboard])
#print(datafile[85])

def TeamNameScores():
	teamNames = re.findall(b" (.+) Score - (.+) Score",datafile[scoreLine+1])
	teamScores = re.findall(b"\[(\d+)\]\s+\[(\d+)\]",datafile[scoreLine+2])
	return teamNames, teamScores
	


t1 = []
t2 = []

for player in players:
	if b"2" in player[0]:
		PLR = player[1].decode().strip()
		FRG = player[4].decode()
		DTH = player[5].decode()
		DMG = player[6].decode()
		ACC = player[7].decode()
		DPR = round(int(player[6])/matchRounds)
		KPR = round(int(player[4])/matchRounds,2)
		KDR = int(player[4]) - int(player[5])
		t2.append(f"{PLR:<16}{FRG:>5}\t{DTH:>6}\t{DMG:>5}\t{ACC:>3}\t{KPR:<4}\t{KDR:>3}\t{DPR:>3}")
	if b"1" in player[0]:
		PLR = player[1].decode().strip()
		FRG = player[4].decode()
		DTH = player[5].decode()
		DMG = player[6].decode()
		ACC = player[7].decode()
		DPR = round(int(player[6])/matchRounds)
		KPR = round(int(player[4])/matchRounds,2)
		KDR = int(player[4]) - int(player[5])
		t1.append(f"{PLR:<16}{FRG:>5}\t{DTH:>6}\t{DMG:>5}\t{ACC:>3}\t{KPR:<4}\t{KDR:>3}\t{DPR:>3}")
		
def ScoreBoard():
	teamNames, teamScores = TeamNameScores()
	print(f"{teamNames[0][0].decode()}: {teamScores[0][0].decode()}")
	print("\t\tFrags\tDeaths\tDamage\tAcc\tKPR\tKDR\tDPR")
	for plr in t1:
		print(plr)
	print("\n")
	print(f"{teamNames[0][1].decode()}: {teamScores[0][1].decode()}")
	print("\t\tFrags\tDeaths\tDamage\tAcc\tKPR\tKDR\tDPR")
	for plr in t2:
		print(plr)

#TeamNameScores()
#print(t1)
#print(t2)
ScoreBoard()
