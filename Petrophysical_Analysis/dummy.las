~Version Information
 VERS.                  2.0:   CWLS LOG ASCII STANDARD - VERSION 2.0
 WRAP.                  NO:    ONE LINE PER DEPTH STEP

~Well Information Block
#MNEM.UNIT       DATA             DESCRIPTION
 STRT.FT         1000.0           : START DEPTH
 STOP.FT         1010.0           : STOP DEPTH
 STEP.FT         0.5              : STEP
 NULL.           -999.25          : NULL VALUE

~Curve Information Block
#MNEM.UNIT       API CODE         DESCRIPTION
 DEPT.FT         00 001 00 00     : DEPTH
 GR.API          00 001 00 01     : GAMMA RAY
 RES.OHM.M       00 001 00 02     : RESISTIVITY
 RHOB.G/CM3      00 001 00 03     : BULK DENSITY
 NPHI.V/V        00 001 00 04     : NEUTRON POROSITY

~Parameter Information
#MNEM.UNIT       VALUE            DESCRIPTION
 A.              1.0              : TORTUOSITY CONSTANT
 M.              2.0              : CEMENTATION EXPONENT
 N.              2.0              : SATURATION EXPONENT
 RW.OHM.M        0.03             : FORMATION WATER RESISTIVITY

~ASCII Log Data
1000.0  45.0   10.0   2.45   0.18
1000.5  60.0   12.0   2.40   0.20
1001.0  80.0   8.0    2.55   0.15
1001.5  100.0  6.0    2.60   0.14
1002.0  30.0   25.0   2.30   0.22
1002.5  25.0   30.0   2.20   0.24
1003.0  70.0   10.0   2.50   0.16
1003.5  90.0   5.0    2.65   0.12
1004.0  50.0   20.0   2.35   0.19
1004.5  40.0   15.0   2.45   0.18
1005.0  35.0   18.0   2.40   0.20
1005.5  60.0   10.0   2.48   0.17
1006.0  75.0   9.0    2.52   0.16
1006.5  85.0   7.0    2.58   0.13
1007.0  95.0   6.0    2.60   0.14
1007.5  100.0  5.5    2.63   0.13
1008.0  55.0   19.0   2.42   0.18
1008.5  45.0   22.0   2.38   0.19
1009.0  35.0   25.0   2.34   0.21
1009.5  30.0   28.0   2.30   0.22
1010.0  25.0   30.0   2.25   0.24
