#!/usr/bin/python3
import os
import re
import sys
from collections import Counter
# own stuff
from aq2_msgs import *

# version v0.4 6.4.2022

# 0.4: dotn count warmup frags/deaths

# TODO
# make code more simple, beautiful and readable


# DEBUG

_debug = False
#_debug = True

# some colors

def color_print(text,color):
        if color == 'cyan':
                string = '\033[96m' + text + '\033[0m'
                print(string)
        elif color == 'yellow':
                string = '\033[93m' + text + '\033[0m'
                print(string)
        elif color == 'magenta':
                string = '\033[95m' + text + '\033[0m'
                print(string)
        elif color == 'white':
                string = '\x1b[97m' + text + '\033[0m'
                print(string)
        elif color == 'green':
                string = '\x1b[32m' + text + '\033[0m'
                print(string)
        elif color == 'red':
                string = '\x1b[91m' + text + '\033[0m'
                print(string)
        elif color == 'purple':
                string = '\033[1;35m' + text + '\033[0m'
                print(string)

# Prepare dicts and lists
kills = []
deaths = []
stats = {}
output = []
players = []

argc = len(sys.argv)

# If server has Warmup,  set it to True, else False
WARMUP = True


# info

# comand  sv softmap  or  normal map change, then we have SpawnServer info, we can get map information
# command map wfall, new players connect then we dont have information about the map
# command gamemap wfall, players are visible as they were always connect, no information about the map

# Above information doesnt matter if we parse specific demo, with live logfile parsing information above is important

if argc < 2:
        print ("Usage: script.py <input_file> <optional_output_file>")
        sys.exit()
elif argc >= 2:
        fn = sys.argv[1]
        if os.path.exists(fn):
                if argc == 2:
                        print ("STATS for %s"%sys.argv[1])
        else:
                sys.exit("File does not exists!")


def get_Accuracy( plr ):
	acc_lists = [3,6,9,12,15]
	if stats[plr]['hss'] in acc_lists:
		stats[plr]['acc']+=1
		#print("STATS: AWARD \t%15s   -> \t   ACCURACY (%s)"%(plr,stats[plr]['acc']))
		#print("STATS: KILL \t%15s   ->   \t%15s\t\t(%s)" %(att,vic,k))
		if _debug:
			string = "STATS: AWARD \t{:>15s}   -> \t   ACCURACY ({})".format(plr,stats[plr]['acc'])
			color_print(string, "white")

def get_Impressive( plr ):
	imp_lists = [5,10,15,20,25,30,35,40,45,50]
	if stats[plr]['streak'] in imp_lists:
		stats[plr]['imp']+=1
		if _debug:
			string = "STATS: AWARD \t{:>15s}   -> \tIMPRESSIVE! ({})".format(plr,stats[plr]['imp'])
			color_print(string, "yellow")

def get_Excellents( plr ):
	exe_lists = [12,24,36,48,60]
	if stats[plr]['streak'] in exe_lists:
		stats[plr]['exe']+=1
		if _debug:
			string = "STATS: AWARD \t{:>15s}   -> \t EXCELLENT! ({})".format(plr,stats[plr]['exe'])
			color_print(string, "purple")



def makePlayerStats( plr ):
	stats[plr] = {}
	stats[plr] = {'frags':0,'deaths':0, \
			'mk23':0,'mp5':0,'m4':0,'m3':0,'hc':0,'ssg':0,'knife':0,'kick':0,'plum':0,'other':0,'hs':0, \
        		'mk23_d':0,'mp5_d':0,'m4_d':0,'m3_d':0,'hc_d':0,'ssg_d':0,'knife_d':0,'kick_d':0,'other_d':0,'hs_d':0, \
			'streak':0,'streak_d':0,'KS':0,'DS':0,'1stK':0,'roundspl':0,'boom':0,'boom_d':0,'hss':0, \
			'acc':0,'imp':0,'exe':0,'dead':False}

def add_frag( plr,wpn ):
        def wpn_sort( wpn ):
                if 'mk23' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['mk23']+=1
                elif 'mp5' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['mp5']+=1
                elif 'm4' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['m4']+=1
                elif 'm3' in wpn:
                        stats[plr]['m3']+=1
                        stats[plr]['hss']=0
                elif 'hc' in wpn:
                        stats[plr]['hc']+=1
                        stats[plr]['hss']=0
                elif 'ssg' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        if 'zoom' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['ssg']+=1
                elif 'sknife' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['knife']+=1
                elif 'tknife' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs']+=1
                                stats[plr]['hss']+=1
                        else:
                                stats[plr]['hss']=0
                        stats[plr]['knife']+=1
                elif 'kick' in wpn:
                        stats[plr]['kick']+=1
                        stats[plr]['hss']=0
                elif 'grenade' in wpn:
                        stats[plr]['boom']+=1
                        stats[plr]['hss']=0
                else:
                        stats[plr]['other']+=1
                        stats[plr]['hss']=0

#                get_Accuracy( plr ) # count accuracy
#                get_Impressive( plr ) # count impressives
                if not stats[plr]['dead']:
                        stats[plr]['streak']+=1
                stats[plr]['streak_d']=0 # set killing streak to 0
                if stats[plr]['streak'] > stats[plr]['KS']:
                        stats[plr]['KS'] = stats[plr]['streak']
#                get_Impressive( plr ) # count impressives
	
        if plr in stats:
                stats[plr]["frags"]+=1
                wpn_sort( wpn )
        else:
                makePlayerStats( plr )
                stats[plr]['frags']+=1
                wpn_sort( wpn )


# Collect deaths function
def add_death( plr, wpn ):
        def wpn_sort (wpn):
                if 'mk23' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['mk23_d']+=1
                elif 'mp5' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['mp5_d']+=1
                elif 'm4' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['m4_d']+=1
                elif 'm3' in wpn:
                        stats[plr]['m3_d']+=1
                elif 'hc' in wpn:
                        stats[plr]['hc_d']+=1
                elif 'ssg' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        if 'zoom' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['ssg_d']+=1
                elif 'sknife' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['knife_d']+=1
                elif 'tknife' in wpn:
                        if 'head' in wpn:
                                stats[plr]['hs_d']+=1
                        stats[plr]['knife_d']+=1

                elif 'kick' in wpn:
                        stats[plr]['kick_d']+=1
                elif 'fall' in wpn:
                        stats[plr]['plum']+=1
                elif 'grenade' in wpn:
                        stats[plr]['boom_d']+=1
                else:
                        stats[plr]['other_d']+=1

                stats[plr]['streak_d']+=1
                stats[plr]['streak']=0 # set killing streak to 0
                if stats[plr]['streak_d'] > stats[plr]['DS']:
                        stats[plr]['DS'] = stats[plr]['streak_d']

        if plr in stats:
                stats[plr]["deaths"]+=1
                stats[plr]['dead']=True
                wpn_sort(wpn)
        else:
                makePlayerStats( plr )
                stats[plr]['deaths']+=1
                wpn_sort( wpn )


def player_1st_kill(plr):
	global round
	if round == 0:
		stats[plr]['1stK']+=1
		if _debug:
			#print ("STATS: AWARD \t%15s   ->   \t   1st KILL (%s)"%(plr,stats[plr]['1stK']))
			string = "STATS: AWARD \t{:>15s}   ->   \t   1st KILL ({})".format(plr,stats[plr]['1stK'])
			color_print(string,"red")
		round = 1


def collect_frags_deaths( line ):
        for k,v in frag_msgs.items():
                m = re.search(v,line)
                if m:
                        if len(m.groups()) == 1:
                                vic=m.group(1)
                                add_death(vic,k)
                                PlayerRounds(vic)
                        else:
                                vic,att=[m.group(1),m.group(2)]
                                add_frag(att,k)
                                if _debug:
                                        print("STATS: KILL \t%15s   ->   \t%15s\t\t(%s)" %(att,vic,k))
                                #
                                get_Accuracy( att ) # count accuracy
                                get_Impressive( att ) # count impressives
                                get_Excellents( att )
                                add_death(vic,k)
                                player_1st_kill(att)
                                PlayerRounds(vic,att)	# add vic and att to player round list

def getRounds( line ):
        for k,v in other_msgs.items():
                m = re.search(v,line)
                global round
                global total_rounds
                global players
                if m:
                        if k == "round_over":
                                if _debug:
                                        #print ("STATS: Round %s END"%(total_rounds))
                                        string = "STATS: ROUND {} ENDS".format(total_rounds)
                                        color_print(string,"green")
                                round = 0;
                                total_rounds += 1
                                for plr in players:
                                        stats[plr]['roundspl']+=1
                                        stats[plr]['dead']=False
                        elif k == "quit":
                                quiter=m.group(1)
                                if quiter in players:
                                        players.remove(quiter)
                                if round == 1 and quiter in stats:
                                        stats[quiter]['roundspl']+=1 # he still played that round!
                                if _debug:
                                        print ("STATS: QUIT \t%15s"%(quiter))
                        elif k == "namechange":
                                oldnick,newnick=[m.group(1),m.group(2)]
                                if oldnick in players:
                                        stats[newnick]=stats[oldnick] # nick change, remove old player from stats with new nick
                                        players.remove(oldnick) # remove oldnick from current players list
                                        players.append(newnick) # add new nick to current players list
                                        del stats[oldnick] # delete old stats
					
	
def PlayerRounds( *plrs ):
	global players
	for plr in plrs:
		if plr not in players:
			players.append(plr)


# core of the script,  lets parse logfile
round = 0
total_rounds = 1
with open(fn, 'r') as f:
	for line in f:
		line = line.replace('\n','')
		
		if "MVD ACTION" in line: # Lets count Frags after first Action and ignore warmup frags...
			WARMUP = False
		
		if not WARMUP:
			collect_frags_deaths( line )
			getRounds(line)

# Lets make nicer output
for player,k in stats.items():
	output.append([player,k['frags'],k['deaths'],(k['frags']-k['deaths']), \
				k['hs'],k['hs_d'], \
				k['mk23'],k['mk23_d'], \
				k['mp5'],k['mp5_d'], \
				k['m4'],k['m4_d'], \
				k['m3'],k['m3_d'], \
				k['hc'],k['hc_d'], \
				k['ssg'],k['ssg_d'], \
				k['knife'],k['knife_d'], \
				k['kick'],k['kick_d'], \
				k['plum'], \
				k['other'],k['other_d'], \
				k['KS'],k['DS'], \
				k['streak'],k['1stK'], \
				k['roundspl'],k['boom'],k['boom_d'], \
				k['acc'],k['imp'],k['exe']])
# Sorting output by fragi-deaths
output = sorted(output, key=lambda output: output[3], reverse=True)

# Prepare column names
if argc == 2:

        #print ('%-15s%3s%4s%4s%6s%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%3s\t%3s\t%3s\t%3s' \
        print ('%-16s%3s%4s%4s%7s%7s%7s%6s%7s%6s%7s%6s%7s%6s%4s%6s%5s%3s%4s%4s%4s%4s' \
        %('Player name','K','D','K-D','HS','MK23','MP5','M4','M3','HC','SSG','KNF','KICK','BOOM','PLU','OTHR','STRK',"1K","Acc","Imp","Exc","PLD"))

# Write  statistics
        for v in output:
        	print ('%-16s%3s%4s%4s' \
        		' %3s/%2s' \
        		' %3s/%2s' \
        		' %3s/%2s' \
        		' %3s/%2s' \
        		' %3s/%s' \
        		' %3s/%s' \
        		' %3s/%2s' \
        		' %3s/%s' \
        		' %3s/%s' \
                        ' %3s/%s' \
        		' %3s' \
        		' %3s/%s' \
        		' %3s/%s' \
        		' %2s %2s' \
                        ' %3s  %2s  %3s' \
        		%(v[0],v[1],v[2],v[3], \
        		v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13], \
        		v[14],v[15],v[16],v[17],v[18],v[19],v[20],v[21],v[30],v[31], \
                        v[22],v[23],v[24],v[25],v[26],v[28],v[32],v[33],v[34],v[29]))
        print ("Total of %s rounds played"%(total_rounds-1)) # Last round played sets +1 to round count becasue we cannot parse start of the round, no usable print available


elif argc == 3:
	out=sys.argv[2]
	fo = open(out, "w")
	fo.write("STATS: %s -> %s rounds played\n"%(out,total_rounds-1))
	fo.write('%-16s%4s%4s%4s%7s%7s%7s%6s%7s%6s%7s%6s%7s%6s%4s%6s%5s%6s%4s%4s%4s%4s\n' \
	        %('Player name','K','D','K-D','HS','MK23','MP5','M4','M3','HC','SSG','KNF','KICK','BOOM','PLU','OTHR','STR',"1stK","Acc","Imp","Exc","PLD"))
	for v in output:
		fo.write( '%-16s%4s%4s%4s' \
       	         ' %3s/%2s' \
       	         ' %3s/%2s' \
	                ' %3s/%2s' \
        	        ' %3s/%2s' \
                	' %3s/%s' \
	                ' %3s/%s' \
        	        ' %3s/%2s' \
	                ' %3s/%s' \
	                ' %3s/%s' \
                        ' %3s/%s' \
        	        ' %3s' \
	                ' %3s/%s' \
        	        ' %3s/%2s' \
              		' %3s %3s' \
                        ' %3s %3s  %3s\n' \
	                %(v[0],v[1],v[2],v[3], \
	                v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13], \
	 	        v[14],v[15],v[16],v[17],v[18],v[19],v[20],v[21],v[30],v[31],v[22],v[23],v[24],v[25],v[26],v[28],v[32],v[33],v[34],v[29]));

	fo.close()
else:
	sys.exit()
