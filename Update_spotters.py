import csv
import maidenhead as mh

# Placeholder for the RBN data (paste your data here)
# Format should be tab-separated with columns: callsign, band, grid, dxcc, cont, itu, cq, first seen, last seen
# Example:
# callsign	band	grid	dxcc	cont	itu	cq	first seen	last seen
# IT9GSF	15m,17m,20m,30m,40m	JM67SS	IT9	EU	28	15	14 years ago	online
# KM3T-5	15m,17m,20m,30m,40m	FN42ET	K	NA	8	5	218 days ago	online
# Paste your RBN data below this line, replacing the example if needed
data = """
callsign	band	grid	dxcc	cont	itu	cq	first seen	last seen
"""
callsign	band	grid	dxcc	cont	itu	cq	first seen	last seen
VE6AO	20m,30m	DO31AC	VE	NA	2	4	13 years ago	online
K7EK	20m	EM77AT	K	NA	8	4	16 years ago	online
LZ4AE	15m,17m,20m,40m	KN13US	LZ	EU	28	20	6 years ago	online
K3PA-2	10m,6m	EM29MD	K	NA	7	4	1 year ago	online
DF7GB	17m,20m,40m	JN49CX	DL	EU	28	14	12 years ago	online
KP3CW	20m	FK68XI	KP4	NA	11	8	1 year ago	online
IK3STG	10m,20m,40m	JN55XK	I	EU	28	15	14 years ago	online
JK1QLQ		PM96MJ	JA	AS	45	25	351 days ago	online
WC2L	20m,30m,40m	FN32BS	K	NA	8	5	6 years ago	online
JH7CSU1	20m,40m	PM95TP	JA	AS	45	25	5 years ago	online
BH4XDZ	17m,20m,40m	OM94NO	BY	AS	44	24	5 years ago	online
K5TR	10m,15m,20m,30m	EM00UF	K	NA	7	4	7 years ago	online
ZL2KS		RE68XL	ZL	OC	60	32	3 years ago	online
HG8A	17m,20m,40m	JN96RK	HA	EU	28	15	4 years ago	online
MM0ZBH	17m,20m,30m,40m	IO86IB	GM	EU	27	14	4 years ago	online
KH6LC	20m	BK29CW	KH6	OC	61	31	14 years ago	online
W2LB		FN12HW	K	NA	8	5	13 years ago	online
ET3AA		KJ99JA	ET	AF	48	37	9 years ago	online
NG7M	15m,17m,20m,40m	DN31xb	K	NA	6	3	8 years ago	online
N7TUG	20m,30m	CN87TQ	K	NA	6	3	9 years ago	online
HA1VHF	20m,2m,30m,40m	JN87GF	HA	EU	28	15	13 years ago	online
NU4F	17m,20m	EL96WD	K	NA	8	5	316 days ago	online
DF2CK	15m,160m,17m,20m,30m,40m,80m	JO71AD	DL	EU	28	14	16 years ago	online
SM0TCZ		JO89XF	SM	EU	18	14	8 years ago	online
J68HZ		FK93LU	J6	NA	11	8	9 years ago	online
WZ7I		FN20KK	K	NA	8	5	16 years ago	online
NA3M 2		FM19JE	K	NA	8	5	198 days ago	online
TI7W	10m,12m,15m,17m,20m	EK70LR	TI	NA	11	7	3 years ago	online
LZ7AA	20m,40m	KN12qq	LZ	EU	28	20	8 years ago	online
GE0FRE		IO82UC	G	EU	27	14	204 days ago	online
WV4P	17m,20m,40m,80m	EM55VD	K	NA	8	4	1 year ago	online
LZ5DI	20m	KN12PQ	LZ	EU	28	20	2 years ago	online
LU8XW		FD55UE	LU	SA	16	13	1 year ago	online
N8DXE		EN91EF	K	NA	8	4	3 years ago	online
JE1AEX-2		PM95LL	JA	AS	45	25	234 days ago	online
KW7MM	12m,15m,17m,20m,30m	DM42MM	K	NA	6	3	6 years ago	online
W2MV		FN31BA	K	NA	8	5	5 years ago	online
JI1HFJ	17m	PM95SS	JA	AS	45	25	6 years ago	online
SQ5J	15m,17m,20m,30m,40m,80m	KO02KF	SP	EU	28	15	2 years ago	online
F4GOU	17m,20m,30m,40m	JN05BX	F	EU	27	14	11 years ago	online
K5EM	20m,30m,40m	CN87UQ	K	NA	6	3	2 years ago	online
ES5PC	15m,17m,20m,30m,40m	KO38HJ	ES	EU	29	15	15 years ago	online
K2PO/7	15m,20m,40m,80m	CN85LI	K	NA	6	3	11 years ago	online
DK3UA		JO64LF	DL	EU	28	14	13 years ago	online
3D2AG	20m	RH91FV	3D2	OC	56	32	4 years ago	online
K4PP	17m,20m,30m,40m,80m	EM64PT	K	NA	8	4	4 years ago	online
LZ4UX	15m,20m	KN23TB	LZ	EU	28	20	10 years ago	online
ON6ZQ	17m,20m,30m,40m	JO20EQ	ON	EU	27	14	13 years ago	online
KC4YVA		FM17IL	K	NA	8	5	7 years ago	online
S53F	15m,17m,20m,40m	JN75ON	S5	EU	28	15	10 years ago	online
SZ1A	17m,20m	KM08QR	SV	EU	28	20	7 years ago	online
NT6Q	15m,17m,20m,30m,40m,80m	DM13LC	K	NA	6	3	3 years ago	online
WA7LNW	20m,30m,40m,80m	DM37GD	K	NA	6	3	14 years ago	online
UA4M		LO44WI	UA	EU	29	16	10 years ago	online
VE6WZ-1		DO21ST	VE	NA	2	4	2 years ago	online
JA1JRS		PM95VS	JA	AS	45	25	9 years ago	online
WW1L		FN54OM	K	NA	8	5	5 years ago	online
KD2OGR	17m,20m,40m	FN20SL	K	NA	8	5	5 years ago	online
K7CO	20m	DN40BN	K	NA	6	3	1 year ago	online
HA6PX	17m,20m,30m,40m,80m	JN98WD	HA	EU	28	15	14 years ago	online
W4AX		EM74TC	K	NA	8	5	14 years ago	online
LA7GIA		JO59LX	LA	EU	18	14	7 years ago	online
AA0O	20m	EL87PS	K	NA	8	5	1 year ago	online
S50ARX		JN65TW	S5	EU	28	15	14 years ago	online
OH4KA	20m	KP31WN	OH	EU	18	15	5 years ago	online
K6FOD	20m,30m,80m	DM04WC	K	NA	6	3	3 years ago	online
WT9U	15m,20m,30m	EN71AO	K	NA	8	4	228 days ago	online
W2NNN	20m,30m,40m	FN20RQ	K	NA	8	5	12 years ago	online
IK7YTT	20m,40m	JN81DC	I	EU	28	15	4 years ago	online
JO1YYP		PM95VW	JA	AS	45	25	9 years ago	online
BA4OP	17m,20m,40m	OM96NX	BY	AS	44	24	74 days ago	online
DG6FL		JO40DA	DL	EU	28	14	8 years ago	online
JJ0VLH		PM96CO	JA	AS	45	25	174 days ago	online
VE6WZ	20m	DO21ST	VE	NA	2	4	14 years ago	online
S50U	15m,17m,20m,40m	JN66XD	S5	EU	28	15	7 years ago	online
W4KAZ	20m,40m	FM05OS	K	NA	8	5	13 years ago	online
VK2GEL		QF55HJ	VK	OC	59	30	7 years ago	online
OK4QRO	17m,20m,30m,40m	JN79XN	OK	EU	28	15	2 years ago	online
KW7MM/7	20m	DM42LL	K	NA	6	3	39 days ago	online
DL0PF	15m,17m,20m,40m,80m	JN68RN	DL	EU	28	14	5 years ago	online
IW9GDC	20m	JM78SD	IT9	EU	28	15	74 days ago	online
DL8LAS	15m,17m,20m	JO54EF	DL	EU	28	14	14 years ago	online
DK8NE		JO50AL	DL	EU	28	14	14 years ago	online
K9IMM	17m,20m,30m,40m	EN52CV	K	NA	8	4	10 years ago	online
BD4UNT		OM92JB	BY	AS	44	24	3 years ago	online
DR4W	15m,20m,40m	JN59SV	DL	EU	28	14	8 years ago	online
F4BPO		JN36DG	F	EU	27	14	112 days ago	online
KM3T-2	20m,40m	FN42et	K	NA	8	5	7 years ago	online
HA8TKS-2	17m	JN96UV	HA	EU	28	15	1 day, 4 hours ago	online
S53A	15m,20m,40m,80m	JN75FT	S5	EU	28	15	3 years ago	online
PY2KNK	40m	GG56NH	PY	SA	15	11	107 days ago	online
G0KTN	17m,20m,30m,40m	IO81TI	G	EU	27	14	15 years ago	online
W3DAN		EN91EF	K	NA	8	5	3 years ago	online
N2YCH	10m,17m,20m,30m,40m,6m	FN31JG	K	NA	8	5	43 days ago	online
DO4DXA	15m,17m,20m,30m,40m	JN58QC	DL	EU	28	14	13 years ago	online
ZS1NN	15m	JF96KO	ZS	AF	57	38	1 year ago	online
OK1HRA	20m,40m,80m	JO60WA	OK	EU	28	15	3 years ago	online
CX6VM	15m,20m,40m	GF27XU	CX	SA	14	13	14 years ago	online
OZ1AAB	20m,40m	JO65CS	OZ	EU	18	14	2 years ago	online
F6KGL	20m,40m	JN18GU	F	EU	27	14	1 year ago	online
UY2RA	20m	KO51IM	UR	EU	29	16	6 years ago	online
S54L	15m,17m,20m,30m,40m,80m	JN75FV	S5	EU	28	15	1 year ago	online
DL1HWS-4	30m	JO61aq	DL	EU	28	14	203 days ago	online
WS2C	20m,30m,40m	FM29KR	K	NA	8	5	356 days ago	online
JN1ILK	15m,17m,20m	PM95ET	JA	AS	45	25	3 years ago	online
OE9GHV	40m	JN47WK	OE	EU	28	15	5 years ago	online
JJ2VLY	20m,30m	PM95JG	JA	AS	45	25	10 years ago	online
JG1DLY		QM05DN	JA	AS	45	25	9 years ago	online
W3RGA	15m,17m,20m,30m,40m	FN10PV	K	NA	8	5	7 years ago	online
W3UA		FN42GV	K	NA	8	5	14 years ago	online
KD7EFG	20m,30m,40m	DN31UO	K	NA	6	3	112 days ago	online
E28AC	20m,40m	OK01CT	HS	AS	49	26	8 years ago	online
S53WW	15m,20m,30m,40m	JN76HE	S5	EU	28	15	3 years ago	online
RK3TD-2		LO26CI	UA	EU	29	16	1 year ago	online
WE9V	20m,30m,40m	EN52XN	K	NA	8	4	16 years ago	online
UA4CC	17m,20m	LO31DN	UA	EU	29	16	3 years ago	online
G4ZFE	20m,30m,40m	IO91PK	G	EU	27	14	9 years ago	online
VE6WZ-2		DO21ST	VE	NA	2	4	5 years ago	online
PY2PE	10m,40m,6m	GG66PO	PY	SA	15	11	111 days ago	online
RN4WA	15m,17m,20m	LO66PU	UA	EU	30	16	15 years ago	online
BH4RRG	40m	OM92IC	BY	AS	44	24	11 years ago	online
BG0AJO	15m	NN33SU	BY	AS	42	23	2 years ago	online
PC5Q	40m	JO22UB	PA	EU	27	14	7 years ago	online
KM3T-3	17m,20m,30m,40m	FN42ET	K	NA	8	5	2 years ago	online
SE5E	15m,20m,30m,40m	JO89LW	SM	EU	18	14	10 years ago	online
W3OA	10m,12m,15m,17m,20m,30m,40m,6m	EM95MN	K	NA	8	5	17 years ago	online
K1RA	15m,17m,20m,30m,40m	FM18CR	K	NA	8	5	14 years ago	online
VE6JY	20m,40m	DO33OR	VE	NA	2	4	8 years ago	online
IT9GSF	15m,17m,20m,30m,40m	JM67SS	IT9	EU	28	15	14 years ago	online
KM3T-5	30m,40m	FN42ET	K	NA	8	5	219 days ago	online
DL0LA	20m	JN68CM	DL	EU	28	14	4 years ago	online
UT5R-1	20m	KO51IM	UR	EU	29	16	105 days ago	online
W2NAF	20m,40m	FN21EI	K	NA	8	5	9 years ago	online
VE3EID	10m,12m,15m,17m,20m,30m,40m	FN05GK	VE	NA	4	4	8 years ago	online
VU2CPL		MK83TE	VU	AS	41	22	8 years ago	online
W1NT-6	17m,20m,30m,40m	FN42LU	K	NA	8	5	6 years ago	online
SM1HEV	17m,20m,40m	JO97BM	SM	EU	18	14	1 year ago	online
DK3WW	17m,20m,30m,40m,80m	JO62MG	DL	EU	28	14	7 years ago	online
UT5R	20m	KO51IM	UR	EU	29	16	4 years ago	online
DK0TE	15m,20m,40m	JN47RP	DL	EU	28	14	12 years ago	online
BD7JNA	17m,40m	OL63QD	BY	AS	44	24	8 years ago	online
W1NT-2	20m,40m	FN42LU	K	NA	8	5	11 years ago	online
IV3DXW	15m,20m,2m,40m	JN65QQ	I	EU	28	15	2 years ago	online
DK9IP-1	20m,40m	JN48FX	DL	EU	28	14	16 years ago	online
HB9BXE	17m,20m,40m	JN47EB	HB	EU	28	14	11 years ago	online
WE4M		FM07II	K	NA	8	5	13 years ago	online
PI4CC	17m,20m,30m,40m	JO21BX	PA	EU	27	14	1 year ago	online
LZ3CB	17m,20m,30m	KN32SN	LZ	EU	28	20	5 years ago	online
LB9KJ		JO29QJ	LA	EU	18	14	1 year ago	online
OH0K/6		KP03SF	OH	EU	18	15	3 years ago	online
N9CO	20m,40m	EN52QA	K	NA	8	4	2 years ago	online
DK9IP	20m	JN48FX	DL	EU	28	14	16 years ago	online
EA5WU	15m,17m,20m,40m	IM99WU	EA	EU	37	14	12 years ago	online
ES2RR	17m,20m,30m,40m	KO29HG	ES	EU	29	15	3 years ago	online
LA6TPA	20m	JP54RL	LA	EU	18	14	11 years ago	online
DL1HWS-3	17m,20m,30m	JO61AQ	DL	EU	28	14	316 days ago	online
HB9DCO		JN37SM	HB	EU	28	14	13 years ago	online
PA5WT		JO22HG	PA	EU	27	14	16 years ago	online
K9LC	10m,17m,20m,30m,40m	EN52MG	K	NA	8	4	5 years ago	online
DK2GOX		JN49WS	DL	EU	28	14	4 years ago	online
ZL4YL	17m,20m	RF80LF	ZL	OC	60	32	8 years ago	online
W8WTS	10m,20m,40m	EN91JJ	K	NA	8	4	15 years ago	online
W6YX	15m,20m,40m,80m	CM87VJ	K	NA	6	3	4 years ago	online
PA5KT	20m,40m	JO11WL	PA	EU	27	14	17 years ago	online
VU2TUM	15m,17m	ML88LJ	VU	AS	41	22	224 days ago	online
K3PA-1	20m,30m,40m	EM29MD	K	NA	7	4	8 years ago	online
OE3KLU	10m	JN88FD	OE	EU	28	15	134 days ago	online
KO7SS	40m	DM42OK	K	NA	6	3	10 years ago	online
EA2RCF-4	20m,30m	IN82PU	EA	EU	37	14	2 years ago	online
DL1HWS	17m,20m,30m,40m	JO61AQ	DL	EU	28	14	3 years ago	online
DE1LON	17m,20m,40m	JO31HG	DL	EU	28	14	11 years ago	online
PE5TT		JO21TV	PA	EU	27	14	5 years ago	online
KV4TT	10m,15m,17m,20m,30m,40m	FM03PT	K	NA	8	5	8 years ago	online
VK6ANC	40m	OF78WE	VK	OC	58	29	5 years ago	online
G4IRN	15m,17m,20m,30m,40m	IO82MO	G	EU	27	14	12 years ago	online
ON7KEC	17m,20m,30m,40m	JO21CE	ON	EU	27	14	2 years ago	online
G3YPP	20m	JO02RV	G	EU	27	14	3 years ago	online
W8WWV	17m,20m,40m	EN91HM	K	NA	8	4	12 years ago	online
N2CR	20m,30m,40m	FN20SU	K	NA	8	5	211 days ago	online
OZ4ADX		JO75IC	OZ	EU	18	14	2 years ago	online
BG4GOV		PM00VW	BY	AS	44	24	8 years ago	online
CT1EYQ	15m,17m,20m,40m	IM58OB	CT	EU	37	14	2 years ago	online
YO5LD	15m,17m,20m,30m,40m	KN05NR	YO	EU	28	20	13 years ago	online
WB6BEE	20m	FM17OG	K	NA	8	5	9 years ago	online
ND7K	20m,40m	DM34OB	K	NA	6	3	2 years ago	online
EA2CW	17m,20m,30m,40m	IN83MG	EA	EU	37	14	11 years ago	online
VK3RASA		QF21WV	VK	OC	59	30	4 years ago	online
RK3TD	15m,20m	LO16QW	UA	EU	29	16	15 years ago	online
DM5GG	15m,17m,20m,30m,40m	JO61UE	DL	EU	28	14	3 years ago	online
OK1FCJ	15m,17m,20m,30m,40m,80m	JO70GA	OK	EU	28	15	15 years ago	online
YO2CK	15m,17m,20m,30m,40m	KN15LO	YO	EU	28	20	301 days ago	online
VE7CC	10m,17m,20m	CN89RE	VE	NA	2	3	11 years ago	online
BG0AJO/0	17m	NN33SU	BY	AS	42	23	172 days ago	online
7N4XCV	20m	PM95PW	JA	AS	45	25	8 years ago	online
BI4MPH-1		PM07QM	BY	AS	44	24	1 year ago	online
W3LPL		FM19LG	K	NA	8	5	14 years ago	online
VK2RH		QF56OC	VK	OC	59	30	2 years ago	online
AC0C-1	15m,17m,20m,30m,40m	EM28QP	K	NA	7	4	4 years ago	online
JE1AEX-1		PM95LL	JA	AS	45	25	242 days ago	online
N6TV	17m,20m,40m,80m	CM97CF	K	NA	6	3	14 years ago	online
R4NCU	20m	LO48VI	UA	EU	29	16	186 days ago	online
BA6KC	17m	OM65XH	BY	AS	44	24	3 years ago	10 minutes ago
DL8TG	17m,20m,30m,40m,60m	JO52IJ	DL	EU	28	14	8 years ago	12 minutes ago
HA8TKS	15m,20m	JN96UV	HA	EU	28	15	11 years ago	14 minutes ago
5Z4GO		KI96UA	5Z	AF	48	37	363 days ago	14 minutes ago
MM0GPZ		IO67HK	GM	EU	27	14	109 days ago	52 minutes ago
DL5RMH	15m,20m,40m	JN68BN	DL	EU	28	14	5 years ago	1 hour, 37 minutes ago
F8KGU		JN19BQ	F	EU	27	14	3 hours, 54 minutes ago	3 hours, 51 minutes ago
VK2EBN	15m,20m	QF57UB	VK	OC	59	30	4 years ago	5 hours, 33 minutes ago
3B8GL	15m	LG89RR	3B8	AF	53	39	228 days ago	5 hours, 36 minutes ago
DD5XX	10m,15m,17m,20m,30m	JN48PS	DL	EU	28	14	7 years ago	5 hours, 54 minutes ago
BD7LAE		OL62LL	BY	AS	44	24	3 years ago	6 hours, 1 minute ago
ZL3X	20m,30m,40m,80m	RE66IR	ZL	OC	60	32	5 years ago	8 hours, 40 minutes ago
KM4SII	20m,40m	EM72GO	K	NA	8	5	5 years ago	10 hours, 46 minutes ago
BG2TFW	15m,20m,30m,40m	PN11SW	BY	AS	44	24	2 years ago	12 hours, 55 minutes ago
LY3G	17m	KO05NS	LY	EU	29	15	7 years ago	16 hours, 5 minutes ago
DL5RCN		JN68RS	DL	EU	28	14	1 year ago	19 hours, 28 minutes ago
WX7V/5	17m	EM12ou	K	NA	7	4	336 days ago	20 hours, 23 minutes ago
F6KBF		JN18BW	F	EU	27	14	21 hours, 30 minutes ago	21 hours, 1 minute ago
UR6EA	20m	KN68RA	UR	EU	29	16	5 years ago	21 hours, 45 minutes ago
PA3GRM		JO22QE	PA	EU	27	14	7 years ago	1 day, 1 hour ago
VU2PTT	15m	MK82TX	VU	AS	41	22	14 years ago	1 day, 2 hours ago
BI4MPH	15m,20m,40m	PM07QM	BY	AS	44	24	3 years ago	1 day, 3 hours ago
RL3A		KO75KR	UA	EU	29	16	14 years ago	1 day, 7 hours ago
IK4VET	20m,40m,80m	JN54MM	I	EU	28	15	7 years ago	1 day, 10 hours ago
PR1T	20m,40m,80m	GG87JR	PY	SA	15	11	15 years ago	1 day, 10 hours ago
GX0FRE	10m,17m,20m,40m	IO82UC	G	EU	27	14	217 days ago	1 day, 16 hours ago
EA1URA	10m,17m,20m	IN73DK	EA	EU	37	14	4 years ago	1 day, 22 hours ago
G4MKR	20m	IO92VD	G	EU	27	14	15 years ago	2 days ago
BH4RXP		OM91IP	BY	AS	44	24	9 years ago	2 days ago
YO2MAX	10m,15m,17m,20m,30m,40m,6m	KN15MR	YO	EU	28	20	1 year ago	2 days ago
EL2BG		IJ46PI	EL	AF	46	35	7 years ago	2 days ago
KE3BK		CM97fs	K	NA	6	3	6 years ago	2 days ago
SM7IUN	20m,30m,40m	JO65MR	SM	EU	18	14	7 years ago	2 days ago
V51YJ		JG86NJ	V5	AF	57	38	14 years ago	2 days ago
PA0MBO	160m,20m,30m,40m,80m	JO32KE	PA	EU	27	14	14 years ago	2 days ago
5Z4NZ		KI88JS	5Z	AF	48	37	9 days ago	2 days ago
RU9CZD	15m,20m,30m	MO07OD	UA9	AS	30	17	13 years ago	2 days ago
HA5PP	15m,17m,20m,30m,40m	JN97MO	HA	EU	28	15	11 years ago	2 days ago
KP2RUM		FK77PR	KP2	NA	11	8	4 years ago	2 days ago
EA1DIW	20m	IN70DX	EA	EU	37	14	84 days ago	3 days ago
BH4XDZ-1		OM94NO	BY	AS	44	24	2 years ago	3 days ago
IZ6198SWL		JN61VQ	I	EU	28	15	5 years ago	3 days ago
BH4HKZ	40m	PM01SD	BY	AS	44	24	51 days ago	4 days ago
F4VVG	20m,40m	JN48BX	F	EU	27	14	3 years ago	4 days ago
R6YY	15m,20m,30m,40m	LN04AN	UA	EU	29	16	12 years ago	4 days ago
LU6KK		FG75GF	LU	SA	14	13	230 days ago	4 days ago
ZF9CW	10m,12m,15m,17m,20m,30m	FK09CR	ZF	NA	11	8	6 years ago	4 days ago
SP5JXK	15m,17m,20m,30m,40m	KO02ML	SP	EU	28	15	37 days ago	4 days ago
HG0Y	20m	JN97WW	HA	EU	28	15	6 years ago	4 days ago
OH6BG	15m,17m,20m,30m	KP03QA	OH	EU	18	15	14 years ago	4 days ago
VR2FUN-77	10m,15m,20m	OL62LL	VR	AS	44	24	2 years ago	5 days ago
VK3VB	40m	QF21PW	VK	OC	59	30	4 years ago	5 days ago
M0SEJ		IO91NW	G	EU	27	14	55 days ago	5 days ago
F1EZG		JN18AX	F	EU	27	14	5 days ago	5 days ago
OZ1BZS	20m	JO46LE	OZ	EU	18	14	1 year ago	5 days ago
IK2LFF	20m,40m	JN45KW	I	EU	28	15	3 years ago	6 days ago
K7RUT		CN87PE	K	NA	6	3	8 years ago	6 days ago
WC8GOP	20m	EN72PS	K	NA	8	4	1 year ago	7 days ago
IK6HIR	6m	JN63KW	I	EU	28	15	2 years ago	7 days ago
PA2SQ	20m	JO22TR	PA	EU	27	14	4 years ago	7 days ago
UA0S	15m,17m,20m,40m	OO22GE	UA9	AS	32	18	4 years ago	8 days ago
EA3QP	15m,17m,20m,30m,40m	JN11EL	EA	EU	37	14	13 days ago	8 days ago
SV1CDN		KM17TX	SV	EU	28	20	11 years ago	8 days ago
5Z/VE3NZ	20m	KI88JS	5Z	AF	48	37	17 days ago	9 days ago
N8NJH		EN81EQ	K	NA	8	4	1 year ago	9 days ago
R1LB	20m	KO49TQ	UA	EU	29	16	6 years ago	10 days ago
SP8R	20m,40m	KO10AA	SP	EU	28	15	4 years ago	10 days ago
DM6EE		JO52KJ	DL	EU	28	14	5 years ago	11 days ago
OH8KA	20m,40m	KP25QC	OH	EU	18	15	3 years ago	11 days ago
JH4UTP	40m,80m	PM64VN	JA	AS	45	25	7 years ago	13 days ago
OE8TED		JN76AO	OE	EU	28	15	3 years ago	13 days ago
GI4DOH-2		IO74DP	GI	EU	27	14	7 years ago	13 days ago
DL1AMQ		JO50UU	DL	EU	28	14	16 years ago	13 days ago
IU0MVD	40m	JN62EC	I	EU	28	15	1 year ago	13 days ago
DJ3AK	2m	JO52GJ	DL	EU	28	14	14 years ago	13 days ago
OG73X	15m,20m	KP24JO	OH	EU	18	15	5 years ago	14 days ago
DF2JP	15m,20m	JO31ET	DL	EU	28	14	9 years ago	14 days ago
DD0VS	15m,20m	JN59PM	DL	EU	28	14	8 years ago	14 days ago
DL1EFW	15m,20m,40m	JO31FD	DL	EU	28	14	13 years ago	15 days ago
PA8MM	15m,20m,40m	JO22LL	PA	EU	27	14	6 years ago	15 days ago
F6IIT	15m,17m,20m,30m,40m	JN06FQ	F	EU	27	14	12 years ago	15 days ago
VE3NZ	15m	FN03HT	VE	NA	4	4	10 years ago	16 days ago
YU1EW		KN04CP	YU	EU	28	15	6 years ago	17 days ago
TF3Y	17m,20m,40m	HP94BD	TF	EU	17	40	15 years ago	17 days ago
DF4UE/1	10m,15m,17m,20m,30m,40m,60m	JN48RR	DL	EU	28	14	9 years ago	17 days ago
RU4FMM		LO13VL	UA	EU	29	16	34 days ago	18 days ago
NN3RP		FM18LW	K	NA	8	5	14 years ago	18 days ago
JI1ACI		PM96XJ	JA	AS	45	25	2 years ago	19 days ago
DF4UE	10m,15m,17m,20m,30m,40m	JN48rr	DL	EU	28	14	11 years ago	20 days ago
BI4UYX	15m,40m	OM91LL	BY	AS	44	24	1 year ago	20 days ago
S57M		JN76PO	S5	EU	28	15	6 years ago	20 days ago
EA5RQ/A	20m	IM99TL	EA	EU	37	14	1 year ago	21 days ago
VE2WU		FN35AA	VE	NA	4	5	17 years ago	21 days ago
BD8CS		OM30BP	BY	AS	43	24	3 years ago	21 days ago
WC2L-2		FN32BS	K	NA	8	5	28 days ago	21 days ago
BG4WOM	15m,17m,20m,40m	OM91JQ	BY	AS	44	24	8 years ago	22 days ago
IQ9RG	10m,15m,20m	JM76GV	IT9	EU	28	15	78 days ago	23 days ago
PD0WAG	20m	JO21TX	PA	EU	27	14	1 year ago	23 days ago
EU1ST		KO33TU	EU	EU	29	16	9 years ago	23 days ago
M0ORD	10m,15m,17m,20m,30m,40m	IO91ON	G	EU	27	14	8 years ago	25 days ago
ZF1A	17m,20m	EK99IG	ZF	NA	11	8	3 years ago	25 days ago
R9IR		NO26MO	UA9	AS	31	18	3 years ago	27 days ago
CT7ASV		IM57SC	CT	EU	37	14	39 days ago	27 days ago
N7OR	15m,20m,40m	CN85UJ	K	NA	6	3	10 years ago	27 days ago
DL9GTB		JO63LX	DL	EU	28	14	14 years ago	28 days ago
4X5XL		KM71jx	4X	AS	39	20	42 days ago	28 days ago
PY2KJ		GG66KN	PY	SA	15	11	7 years ago	29 days ago
BY4XRA	20m,40m	OM94OO	BY	AS	44	24	1 year ago	31 days ago
R8QAT	20m	MO25QK	UA9	AS	30	17	32 days ago	32 days ago
3V9A		JM54IQ	3V	AF	37	33	2 years ago	33 days ago
UD4FD		LO23OQ	UA	EU	29	16	10 years ago	34 days ago
WA7AI	15m,17m,20m	CN87PE	K	NA	6	3	3 years ago	34 days ago
G4YBU	15m	IO91UI	G	EU	27	14	5 years ago	35 days ago
DE2SAX		JN48XK	DL	EU	28	14	4 years ago	35 days ago
G0TMX	10m,17m,20m,30m,40m	JO02IF	G	EU	27	14	11 years ago	35 days ago
M7KPO	20m	IO91RV	G	EU	27	14	1 year ago	36 days ago
OG66X	20m	KP24HP	OH	EU	18	15	4 years ago	37 days ago
DL3OBQ		JN57UV	DL	EU	28	14	255 days ago	37 days ago
OE3KLU-3		JN88FD	OE	EU	28	15	120 days ago	38 days ago
KW7MM-2		DM42LL	K	NA	6	3	39 days ago	39 days ago
KW7MM/2	20m,40m	DM42LL	K	NA	8	5	39 days ago	39 days ago
VY0ERC		ER60TB	VE	NA	4	2	5 years ago	40 days ago
F5AHD		JN37RO	F	EU	27	14	13 years ago	40 days ago
DL8LDN		JO43XT	DL	EU	28	14	42 days ago	42 days ago
R3IBZ	40m	KO76LM	UA	EU	29	16	2 years ago	42 days ago
W2ASX		EM93UB	K	NA	8	5	56 days ago	42 days ago
HA2NA	20m,40m	JN97IT	HA	EU	28	15	6 years ago	43 days ago
OE6ADD	20m,30m,40m	JN77PA	OE	EU	28	15	5 years ago	44 days ago
EA4FIT		IN80di	EA	EU	37	14	11 years ago	44 days ago
HA2DXC	40m	JN97IT	HA	EU	28	15	44 days ago	44 days ago
OE6TZE		JN76RX	OE	EU	28	15	11 years ago	45 days ago
HB9GVO		JN46LI	HB	EU	28	14	3 years ago	46 days ago
K7MJG		DM33XH	K	NA	6	3	4 years ago	46 days ago
MM3NDH-3		IO86ha	GM	EU	27	14	1 year ago	47 days ago
NK4DX		EL98LL	K	NA	8	5	50 days ago	47 days ago
MM3NDH	15m,20m,30m,40m	IO86HA	GM	EU	27	14	2 years ago	48 days ago
MM3NDH-2	20m,40m	IO86ha	GM	EU	27	14	1 year ago	48 days ago
CT7ANO	17m,20m,40m	IM58HU	CT	EU	37	14	8 years ago	48 days ago
DM7EE	160m,17m,20m,40m,80m	JO52JJ	DL	EU	28	14	5 years ago	48 days ago
EA5RQ	10m,15m	IM99TL	EA	EU	37	14	1 year ago	49 days ago
9J2FI		KH44GP	9J	AF	53	36	49 days ago	49 days ago
HZ1FI		LL74TH	HZ	AS	39	21	14 years ago	49 days ago
OH4MFA		KP32NG	OH	EU	18	15	15 years ago	50 days ago
K3SIW		EN52TB	K	NA	8	4	50 days ago	50 days ago
S50BCC	10m,15m,20m,40m	JN75ON	S5	EU	28	15	52 days ago	52 days ago
DO4ZT	20m,40m	JO61VD	DL	EU	28	14	176 days ago	54 days ago
WS3W		FM19NG	K	NA	8	5	4 years ago	55 days ago
GI0RQK	20m	IO74AS	GI	EU	27	14	13 years ago	55 days ago
GI4DOH-1		IO74DP	GI	EU	27	14	217 days ago	56 days ago
""" 

# Split the data into lines and skip the header
lines = data.strip().split('\n')[1:]

# List to store the processed data
updated_data = []

# Process each line
for line in lines:
    columns = line.split('\t')
    if len(columns) == 9:  # Ensure the line has all expected columns
        callsign = columns[0].strip()
        grid = columns[2].strip()
        # Include all nodes with a valid grid square, regardless of last seen status
        if grid:  # Only process if grid is not empty
            try:
                # Convert grid square to latitude and longitude
                lat, lon = mh.to_location(grid)
                # Round to three decimal places for consistency with your original CSV
                lat = round(lat, 3)
                lon = round(lon, 3)
                updated_data.append({
                    'callsign': callsign,
                    'latitude': lat,
                    'longitude': lon
                })
            except ValueError:
                print(f"Skipping {callsign}: Invalid grid square '{grid}'")

# Write the updated data to a new CSV file
with open('updated_spotter_coords.csv', 'w', newline='') as csvfile:
    fieldnames = ['callsign', 'latitude', 'longitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in updated_data:
        writer.writerow(row)

print(f"Updated CSV file 'updated_spotter_coords.csv' created successfully with {len(updated_data)} nodes.")
