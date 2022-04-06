### MVDscoreboard.py
This script grabs last layout informationi from a MVD2 file.
```
./MVDscoreboard.py 2022-04-06_0105_MollysMen_KvakiDuraki_country.mvd2
Team 1: 14
                Frags   Deaths  Damage  Acc     KPR     KDR     DPR
Ralle              24       15   4621    22     0.92      9     178
1.ruf              24       23   3571     9     0.92      1     137
uno.misse          18       17   4170    15     0.69      1     160
uno.Pain           13       22   2411    15     0.5      -9      93


Team 2: 12
                Frags   Deaths  Damage  Acc     KPR     KDR     DPR
Baystrup           26       21   5390    19     1.0       5     207
dos.Rezet          24       18   4771    13     0.92      6     184
dos.Artem          14       19   3630    25     0.54     -5     140
dos.bombermynz     13       21   2746    20     0.5      -8     106
```

### logfile.py
Additional more in depth statistics from a MVD logfile.

Requirement for this script to work is a MVDTOOL from Skuller https://git.skuller.net/mvdtool/

We need to parse out strings from the MVD2 with mvdtool:

`mvdtool strings 2022-04-06_0105_MollysMen_KvakiDuraki_country.mvd2 > 2022-04-06_0105_MollysMen_KvakiDuraki_country.txt`

And then we can execute logfile.py

```
./logfile.py  2022-04-06_0105_MollysMen_KvakiDuraki_country.txt
STATS for 2022-04-06_0105_MollysMen_KvakiDuraki_country.txt
Player name       K   D K-D     HS   MK23    MP5    M4     M3    HC    SSG   KNF   KICK  BOOM PLU  OTHR STRK 1K Acc Imp Exc PLD
Ralle            24  15   9   4/10   0/ 1   2/ 1   7/ 7   0/0   0/0  14/ 5   0/1   0/0   0/0   0   1/0   3/2  2  0   0   0   26
dos.Rezet        24  18   6  12/ 8   0/ 2   0/ 3  23/ 6   0/1   0/0   0/ 5   1/1   0/0   0/0   0   0/0   3/3  2  1   0   0   26
Baystrup         26  21   5  12/ 4   4/ 0   0/ 0  11/11   0/1   0/0  11/ 8   0/0   0/0   0/0   0   0/1   6/3  8  2   1   0   26
1.ruf            24  23   1   7/ 6   2/ 2   0/ 0  21/12   0/0   0/0   0/ 9   0/0   0/0   0/0   0   1/0   5/4  6  1   1   0   26
uno.misse        18  17   1   8/ 4   3/ 0   1/ 5   6/ 4   0/1   0/0   8/ 4   0/0   0/0   0/2   0   0/1   5/5  0  0   1   0   26
dos.Artem        14  19  -5   4/ 5   0/ 2   0/ 0   0/11   0/0   0/0  13/ 5   0/0   0/0   0/0   0   1/1   4/4  3  0   0   0   26
dos.bombermynz   13  21  -8   2/ 3   0/ 1   7/ 0   0/15   1/0   0/0   2/ 4   0/0   0/0   3/1   0   0/0   3/6  5  0   0   0   26
uno.Pain         13  22  -9   1/10   0/ 1   0/ 1   9/11   2/0   0/0   0/ 8   1/0   0/0   1/1   0   0/0   2/4  0  0   0   0   26
Total of 26 rounds played
```
