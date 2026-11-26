"""Original deterministic newspaper artwork for the Thursday competition."""
from pathlib import Path
from collections import Counter
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PAPER = '#f4f0e5'
INK = '#122837'
RED = '#b6332d'
MUTED = '#52626b'
RULE = '#c7c5ba'
GOLD = '#ceaa60'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
if (FONT_DIR / 'DejaVuSans.ttf').exists():
    REGULAR = FONT_DIR / 'DejaVuSans.ttf'
    BOLD = FONT_DIR / 'DejaVuSans-Bold.ttf'
else:
    FONT_DIR = Path('/usr/share/fonts/truetype/noto')
    REGULAR = FONT_DIR / 'NotoSans-Regular.ttf'
    BOLD = FONT_DIR / 'NotoSans-Bold.ttf'
assert REGULAR.exists() and BOLD.exists()
fonts = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in fonts:
        fonts[key] = ImageFont.truetype(str(BOLD if bold else REGULAR), size)
    return fonts[key]

# Each brief is independently numbered; supporting context is never counted.
# Region taxonomy: Americas, Europe, Africa, Middle East, South Asia,
# East Asia, Oceania. Eighteen editorial fields are assigned explicitly.
briefs = [
('SOLOMONS PICK AUSTRALIA OVER CHINA','Security treaty picks Canberra; no foreign military base.','Reuters / AP','Oceania','Diplomacy','flag'),
('NORTH KOREA EXPELS SWISS ENVOY','48 hours to leave over Songdowon camp sanctions.','Reuters / AP','East Asia','Diplomacy','flag'),
("DURAN DURAN’S ANDY TAYLOR DIES AT 65",'Prostate cancer; co-wrote “Hungry Like the Wolf” and “Rio”.','Reuters / AP','Europe','Culture','music'),
('INDIA: HASINA RETURN SEPARATE FROM EXTRADITION','Delhi separates voluntary return from Dhaka’s request; death sentence at home.','Reuters','South Asia','Diplomacy',None),
('TAIWAN SHARES SINK 1,927 POINTS','Closes 38,195.43; Taiwan dollar weakens past 33 per US dollar.','wire','East Asia','Markets','chart'),
('FED BEIGE BOOK: MODEST GROWTH','Wage gains and persistent price pressure across US districts.','wire','Americas','Economy',None),
('US TIGHTENS AI CHIP ACCESS','Remote-access rules tighten; thousands of Nvidia B300 GPUs seek buyers.','wire','Americas','Technology','chip'),
('ECONOMISTS WARN OF AI BUBBLE','A burst could exceed the dot-com crisis impact.','wire','Americas','Economy',None),
('F-15EX FIGHTERS UNVEILED AT KADENA','US Air Force shows new fighters at its Okinawa base.','wire','East Asia','Defence','plane'),
('INDIA MARKS CONSTITUTION DAY','Samvidhan Divas: 77 years since adoption.','wire','South Asia','Politics','book'),
('MUMBAI REMEMBERS 26/11','Nationwide tributes on the attacks’ 18th anniversary.','wire','South Asia','Culture',None),
('IITs TO ADD 6,000 TECH SEATS','Robotics, AI and space technology places from 2027.','wire','South Asia','Education',None),
('INDIA: HUMANS MUST CONTROL AI IN WAR','Delhi urges human judgement in military AI operations.','wire','South Asia','Defence',None),
('1,220 CRICKETERS ENTER IPL AUCTION','Registrations pour in for the IPL 2027 auction.','wire','South Asia','Sport','ball'),
('FLIPKART CEO TO STEP DOWN','Kalyan Krishnamurthy will leave in December, reports say.','wire','South Asia','Business',None),
('BANGLADESH RAISES GARMENT WAGE 36%','Entry-level garment workers’ minimum monthly pay jumps.','wire','South Asia','Labour','shirt'),
('GUKESH DRAWS GAME 2 IN 20 MOVES','World champion shares point with Sindarov in Geneva.','wire','Europe','Sport',None),
('ASTEROID DEFENCE CRATER REVEALED','Close-ups show crater from Earth’s deliberate impact test.','wire','Americas','Science','asteroid'),
('WOLBACHIA MOSQUITOES CUT INFECTIONS 68%','Brazil release programme cuts mosquito-borne viral infections.','wire','Americas','Health','mosquito'),
('EMIRATES TOPS AIRLINE RANKINGS','Dubai carrier leads global rankings; reliability in focus.','wire','Middle East','Business',None),
('GUTERRES PRAISES COLOMBIA PEACE','UN chief hails a decade of progress since peace accord.','UN','Americas','Diplomacy',None),
('TEMPUS TO BUY PERSONALIS FOR $600M','Cash-election merger agreement announced.','Investing.com','Americas','Business',None),
('META FACES CONGRESS ON SUSPENDED ACCOUNTS','Officials meet lawmakers over account suspensions.','wire','Americas','Technology',None),
('LIKUD APPEALS ELECTION RESULTS','Party seeks reruns at 120 polling stations.','Jerusalem Post','Middle East','Politics',None),
('ISRAEL STRIKE KILLS HAMAS OFFICIAL','Al-Shati: Abu al-Ouf, wife and two daughters killed, medics say.','AP','Middle East','Security',None),
('IRAN NAMES PALANTIR AND ANTHROPIC AT UN','Tehran says US automated systems fed coordinates for 2,000 strikes.','CBS','Middle East','Security',None),
('INTRUDER BREACHES US TREASURY UNIT','Break-in hits financial crimes unit’s systems.','Newsweek','Americas','Security',None),
('ISRAEL HOLDS 48 GAZA PRISONERS PAST TERMS','Palestinian commission says detainees kept after sentences expire.','Al Jazeera','Middle East','Security',None),
('XI’S GRAFT PROBE HITS SHANGHAI STAR','Investigation upends China’s traditional path to power.','BBC','East Asia','Politics',None),
('RUSSIA’S OWN FIGURES: NEARLY 500,000 LOST','Moscow’s numbers put Ukraine war dead near half a million.','BBC','Europe','Security',None),
('COLOMBIA POLICE FREE 20 HOSTAGES','Supermarket stormed to end a 17-hour ordeal.','wire','Americas','Security',None),
('US ATTORNEY GENERAL DODGES NVIDIA QUESTIONS','AG declines to answer on the Nvidia investigation.','wire','Americas','Politics',None),
('AMERICA CELEBRATES THANKSGIVING','Parades and family tables on November’s fourth Thursday.','wire','Americas','Culture','table'),
('OPEC+ MEETS SUNDAY ON 2027 OUTPUT','Cartel weighs production as surplus fears cap oil gains.','Reuters','Middle East','Energy',None),
('INDIA CONDEMNS RIYADH ATTACK','Delhi condemns tower strike after two Indians are injured.','wire','South Asia','Diplomacy',None),
('TAIPEI: 15% IS LOWEST TIER','Executive Yuan says US rate is not stacked on existing tariffs.','wire','East Asia','Trade',None),
('MEXICO AND NORWAY SPARED','USTR makes no excess-capacity finding against either for now.','USTR','Americas','Trade',None),
('US CRUDE STOCKS BUILD LESS THAN EXPECTED','Smaller inventory rise supports prices alongside Gulf risk.','Reuters','Americas','Energy',None),
('SAUDI: NO INJURIES AT RAS TANURA','Coalition’s initial assessment: falling drone fragments, no injuries.','Reuters','Middle East','Energy',None),
('RAS TANURA: 550,000 BARRELS A DAY','Complex accounts for about 16% of Saudi refining capacity.','The National','Middle East','Energy',None),
('TANG HONGBO’S THIRD TIANGONG VISIT','Shenzhou-24 commander is first to visit the station three times.','CMSA','East Asia','Space',None),
('YEAR-LONG MISSION BEGINS','Shenzhou-23’s Zhu Yangshu stays for China’s first year-long mission.','CMSA','East Asia','Space',None),
('AUSTRALIA TO SPEND $740M IN SOLOMONS','Decade of grants and loans for police, education and infrastructure.','AAP','Oceania','Diplomacy',None),
('KIM YO JONG: “OPEN HOSTILE ACT”','Leader’s sister condemns Swiss sanctions on children’s camp.','KCNA','East Asia','Diplomacy',None),
('INDIA’S SPACE ECONOMY TO HIT $45BN','Minister Jitendra Singh: up from $9bn within a decade.','wire','South Asia','Space',None),
('KAMARAJAR PORT GETS NEW TERMINAL','Cabinet approves ₹4,288-crore second container terminal.','wire','South Asia','Business',None),
]
leads = [
('US SLAPS TARIFFS ON 14 PARTNERS','Washington proposes Section 301 tariffs over “structural excess capacity”: 15% for the EU, Japan, South Korea, Taiwan and Switzerland; China faces 20% stacked on existing duties. Public comment and a January hearing come first. Taipei calls 15% the lowest tier.','USTR / Reuters','Americas','Trade'),
('HOUTHIS CLAIM RAS TANURA STRIKE — BRENT $94.61','Houthis say they hit Saudi Arabia’s largest refinery and Riyadh’s financial district. Saudi air defences down four drones; satellite images show thick black smoke. Brent settles 3.5% higher at $94.61.','Reuters','Middle East','Energy'),
('CAIRO TANKER FIRE KILLS 31','Overturned tanker ignites on Cairo’s Ring Road in Giza’s Warraq: at least 31 dead, 21 injured. More than two dozen vehicles charred; road reopens.','AP / Reuters','Africa','Disasters'),
('PAKISTAN’S FIRST ASTRONAUT ABOARD TIANGONG','Muhammad Zeeshan Ali is the first Pakistani in orbit and Tiangong’s first foreign visitor. Shenzhou-24 docks with Tang Hongbo and Wu Yi; Ali stays about a week for experiments.','Reuters / CMSA','East Asia','Space'),
]
assert len(briefs) == 46 and len(leads) + len(briefs) == 50
regions = {s[3] for s in briefs + leads}
fields = {s[4] for s in briefs + leads}
assert len(regions) == 7 and len(fields) == 18, (regions, fields)

im = Image.new('RGB', (1024, 1024), PAPER)
d = ImageDraw.Draw(im)
def line(x1,y1,x2,y2,fill=RULE,width=1):
    d.line((x1,y1,x2,y2), fill=fill, width=width)
def text(x,y,s,size=10,bold=False,fill=INK):
    d.text((x,y),s,font=font(size,bold),fill=fill,stroke_width=0)
def wrap(s, size, width, bold=False):
    out=[]
    current=''
    for word in s.split():
        trial=(current+' '+word).strip()
        if d.textlength(trial,font=font(size,bold)) <= width:
            current=trial
        else:
            if current:
                out.append(current)
            assert d.textlength(word,font=font(size,bold)) <= width, word
            current=word
    if current:
        out.append(current)
    return out

def paragraph(x,y,s,size,width,bold=False,fill=INK,leading=None):
    step=leading or size+2
    for row in wrap(s,size,width,bold):
        text(x,y,row,size,bold,fill)
        y+=step
    return y

def spot(kind,x,y,w=26,h=25):
    # Tiny editorial drawings, each composed from original geometric marks.
    cx=x+w/2
    cy=y+h/2
    if kind=='flag':
        line(x+3,y+2,x+3,y+23,INK,2)
        d.polygon([(x+4,y+3),(x+24,y+3),(x+20,y+13),(x+4,y+13)],fill=RED)
    elif kind=='music':
        line(x+10,y+3,x+10,y+20,INK,2)
        line(x+10,y+3,x+22,y+1,INK,3)
        line(x+22,y+1,x+22,y+17,INK,2)
        d.ellipse((x+3,y+17,x+11,y+23),fill=RED)
        d.ellipse((x+15,y+14,x+23,y+20),fill=RED)
    elif kind=='chart':
        line(x+2,y+2,x+2,y+23,INK)
        line(x+2,y+23,x+25,y+23,INK)
        d.line([(x+4,y+4),(x+11,y+9),(x+16,y+7),(x+23,y+20)],fill=RED,width=2)
    elif kind=='chip':
        d.rectangle((x+6,y+6,x+20,y+20),fill=INK)
        for a in range(8,20,4):
            line(x+a,y+2,x+a,y+24,INK)
            line(x+2,y+a,x+24,y+a,INK)
        d.rectangle((x+10,y+10,x+16,y+16),fill=GOLD)
    elif kind=='plane':
        d.polygon([(cx,y),(cx+3,y+9),(x+26,y+17),(cx+2,y+15),(cx+2,y+23),(cx,y+20),(cx-2,y+23),(cx-2,y+15),(x,y+17),(cx-3,y+9)],fill=INK)
    elif kind=='book':
        d.polygon([(x+2,y+4),(cx,y+7),(x+24,y+4),(x+24,y+22),(cx,y+24),(x+2,y+21)],fill=GOLD,outline=INK)
        line(cx,y+7,cx,y+23,INK)
    elif kind=='ball':
        d.ellipse((x+3,y+2,x+24,y+23),fill=RED)
        d.arc((x+6,y+1,x+19,y+24),75,280,fill=PAPER,width=2)
    elif kind=='shirt':
        d.polygon([(x+8,y+3),(x+17,y+3),(x+25,y+9),(x+21,y+15),(x+18,y+12),(x+18,y+24),(x+6,y+24),(x+6,y+12),(x+3,y+15),(x,y+9)],fill=GOLD,outline=INK)
    elif kind=='asteroid':
        d.polygon([(x+7,y+4),(x+18,y+1),(x+25,y+11),(x+20,y+23),(x+8,y+24),(x+1,y+14)],fill=MUTED)
        d.ellipse((x+9,y+8,x+18,y+17),fill=INK)
        d.ellipse((x+5,y+16,x+9,y+20),fill=PAPER)
    elif kind=='mosquito':
        d.ellipse((cx-2,y+8,cx+2,y+20),fill=INK)
        d.ellipse((x+1,y+3,cx,y+12),outline=RED)
        d.ellipse((cx,y+3,x+25,y+12),outline=RED)
        for dy in (9,14,19):
            line(x+4,y+dy+3,cx,y+dy,INK)
            line(cx,y+dy,x+23,y+dy+3,INK)
    else:
        d.rectangle((x+1,y+11,x+25,y+15),fill=RED)
        line(x+4,y+15,x+4,y+24,INK,2)
        line(x+22,y+15,x+22,y+24,INK,2)
        d.ellipse((x+8,y+3,x+18,y+11),fill=GOLD)

def port(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill='#dce4df')
    d.rectangle((x,y+h-24,x+w,y+h),fill=INK)
    for i in range(4):
        xx=x+12+i*57
        for j in range(2):
            yy=y+h-43-j*20
            d.rectangle((xx,yy,xx+52,yy+17),fill=RED if (i+j)%3==0 else GOLD,outline=PAPER)
            for a in range(6,50,8):
                line(xx+a,yy+3,xx+a,yy+14,PAPER)
    for xx in (x+39,x+183):
        line(xx,y+13,xx,y+h-65,INK,4)
        line(xx-28,y+13,xx+75,y+13,INK,4)
        line(xx,y+13,xx+56,y+38,INK,2)
        line(xx+65,y+13,xx+65,y+51,INK)
    for xx,label in ((x+27,'15%'),(x+158,'20%')):
        d.polygon([(xx,y+45),(xx+58,y+45),(xx+69,y+56),(xx+58,y+75),(xx,y+75)],fill=PAPER,outline=RED,width=2)
        text(xx+6,y+46,label,20,True,RED)
    text(x+10,y+h-21,'SECTION 301 / PROPOSED',10,True,PAPER)

def refinery(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill='#dce4df')
    for k in range(7):
        xx=x+25+k*13
        yy=y+25-(k%3)*5
        d.ellipse((xx,yy,xx+28,yy+21),fill=INK)
    for xx,hh in ((x+26,29),(x+59,38),(x+90,24)):
        d.rectangle((xx,y+h-hh,xx+9,y+h),fill=MUTED)
        d.rectangle((xx-2,y+h-hh,xx+11,y+h-hh+4),fill=RED)
    line(x+5,y+h-4,x+w-5,y+h-4,INK,4)

def fire(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill='#dce4df')
    d.polygon([(x,y+h),(x+35,y+14),(x+w-35,y+14),(x+w,y+h)],fill=INK)
    line(x+w//2,y+38,x+w//2,y+h,PAPER,2)
    d.rounded_rectangle((x+31,y+39,x+77,y+56),radius=6,fill=GOLD)
    for xx in (x+36,x+67):
        d.ellipse((xx,y+52,xx+10,y+62),fill=MUTED)
    d.polygon([(x+49,y+45),(x+38,y+28),(x+52,y+34),(x+59,y+10),(x+67,y+31),(x+77,y+23),(x+70,y+46)],fill=RED)
    d.polygon([(x+53,y+44),(x+58,y+25),(x+65,y+44)],fill=GOLD)

def station(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill=INK)
    for i in range(12):
        xx=x+((i*43+7)%w)
        yy=y+((i*17+3)%h)
        d.point((xx,yy),fill=PAPER)
    d.arc((x-30,y+h-18,x+w+40,y+h+45),185,350,fill='#80aaa8',width=10)
    for xx in (x+8,x+80):
        d.rectangle((xx,y+24,xx+29,y+45),fill='#548190',outline=PAPER)
        for a in (10,20):
            line(xx+a,y+24,xx+a,y+45,INK)
        line(xx,y+34,xx+29,y+34,INK)
    d.rounded_rectangle((x+39,y+28,x+78,y+40),3,fill=PAPER)
    line(x+58,y+18,x+58,y+49,PAPER,5)
    d.polygon([(x+78,y+32),(x+91,y+29),(x+97,y+34),(x+91,y+40),(x+78,y+37)],fill=GOLD)

def bounded_art(painter, x, y, w, h, scale=None):
    global d
    tile = Image.new('RGB', (w, h), PAPER)
    original = d
    d = ImageDraw.Draw(tile)
    painter(0, 0, w, h)
    d = original
    if scale:
        tile = tile.resize(scale, Image.Resampling.LANCZOS)
    im.paste(tile, (x,y))

# The large date is part of the identity, not a tiny issue label.
d.rectangle((0,0,1024,98),fill=INK)
text(22,0,'THE WORLD TODAY',53,True,PAPER)
text(25,60,'THURSDAY 26 NOVEMBER 2026',26,True,PAPER)
d.rectangle((22,101,1002,121),fill=RED)
text(30,102,f'50 STORIES · {len(regions)} REGIONS · {len(fields)} FIELDS',12,True,PAPER)
text(735,103,'THE THURSDAY WORLD BRIEF',11,True,PAPER)

text(22,127,'01 / TRADE SHOCK',11,True,RED)
paragraph(22,140,leads[0][0],36,654,True,leading=38)
y=paragraph(22,221,leads[0][1],12,654,leading=15)
text(22,y+1,'[USTR / Reuters]',10,True,MUTED)
port(702,131,300,144)
line(22,289,1002,289,INK,2)

# Three equal-width lead cards with compact silhouettes.
for idx,(xx,art) in enumerate(((22,refinery),(354,fire),(686,station)),1):
    s=leads[idx]
    text(xx,296,f'0{idx+1} / '+s[4].upper(),10,True,RED)
    end=paragraph(xx,311,s[0],17,313,True,leading=19)
    bounded_art(art,xx,end+5,115,65)
    paragraph(xx+123,end+4,s[1],9,190,leading=11)
    text(xx,430,'['+s[2]+']',8,True,MUTED)
    if idx<3:
        line(xx+322,299,xx+322,442)

# Context band; it is explicitly outside the numbered story sequence.
d.rectangle((22,447,1002,482),fill=INK)
text(31,452,'WHY OIL IS BURNING',12,True,PAPER)
paragraph(221,451,'The US–Iran war is in its ninth month: tanker attacks near the Strait of Hormuz, Houthi strikes on Saudi energy sites — Brent $94.61; OPEC+ meets Sunday on 2027 output. [Reuters / wire]',10,770,fill=PAPER,leading=13)
text(22,488,'THE REST OF THE WORLD',14,True,INK)
text(745,492,'46 BRIEFS / READ DOWN EACH COLUMN',9,True,MUTED)
line(22,508,1002,508,INK)

# A 16 / 15 / 15 rhythm leaves a spare cell for the coverage key.
# Every line is measured and the card height derives from its actual text.
columns = [(22,briefs[:16],0),(354,briefs[16:31],16),(686,briefs[31:],31)]
max_bottom=0
for x,items,offset in columns:
    measured=[]
    for j,s in enumerate(items):
        head,deck,source,region,field,icon=s
        tx=x+22
        width=291-(30 if icon else 0)
        # Headlines maintain a stronger weight; decks include an adjacent source.
        hs=8
        ds=7
        hlines=wrap(head,hs,width,True)
        body=deck+' ['+source+']'
        dlines=wrap(body,ds,width)
        height=len(hlines)*9+len(dlines)*8+3
        measured.append((s,hlines,dlines,height,width))
    available=350
    total=sum(m[3] for m in measured)
    assert total<=available,(x,total)
    gap=(available-total)/max(1,len(measured)-1)
    yy=515.0
    for j,(s,hlines,dlines,height,width) in enumerate(measured):
        top=round(yy)
        text(x,top,f'{offset+j+5:02}',9,True,RED)
        ty=top
        for row in hlines:
            text(x+22,ty,row,8,True)
            ty+=9
        for row in dlines:
            text(x+22,ty,row,7,False,MUTED)
            ty+=8
        if s[5]:
            bounded_art(lambda a,b,w,h: spot(s[5],a,b,w,h),x+293,top+1,27,27,scale=(min(23,height-3),min(23,height-3)))
        line(x,ty+2,x+314,ty+2)
        yy+=height+gap
    max_bottom=max(max_bottom,yy-gap)
for xx in (344,676):
    line(xx,515,xx,866)
assert max_bottom <= 866

# Seven-point UTC desk timeline.
d.rectangle((22,874,1002,918),fill=INK)
text(30,877,'HOW THURSDAY UNFOLDED — UTC',10,True,PAPER)
timeline=[('00:00','Asia wakes to tariffs;','Taipei: 15%, lowest tier'),('01:00','Pakistan’s Ali: first','full day on Tiangong'),('03:00','Cairo fire toll','confirmed at 31'),('05:00','Brent $94.61 after','Ras Tanura claim'),('06:00','India: Constitution Day','& Mumbai anniversary'),('14:00','Thanksgiving parades','begin in New York'),('19:00','OPEC+ ministers gather','ahead of Sunday')]
for i,(t,a,b) in enumerate(timeline):
    xx=30+i*139
    text(xx,891,t,8,True,'#e6b76b')
    text(xx+31,891,a,7,False,PAPER)
    text(xx,902,b,7,False,PAPER)

# Dotted map with numbered references to the actual numbered story cards.
text(22,925,'WHERE IT HAPPENED',10,True)
mapx,mapy=23,942
polys=[[(0,4),(19,0),(32,8),(27,18),(19,23),(11,14)],[(22,24),(35,26),(37,36),(30,47),(25,36)],[(49,9),(60,5),(76,10),(99,5),(127,11),(139,21),(121,29),(107,21),(91,25),(76,19),(62,18)],[(57,22),(75,23),(78,33),(66,45),(57,34)],[(118,35),(134,34),(143,43),(126,48)]]
def inside(px,py,p):
    state=False
    for i in range(len(p)):
        a,b=p[i],p[(i+1)%len(p)]
        if (a[1]>py)!=(b[1]>py) and px<(b[0]-a[0])*(py-a[1])/(b[1]-a[1])+a[0]:
            state=not state
    return state
for xx in range(0,147,3):
    for yy in range(0,49,3):
        if any(inside(xx,yy,p) for p in polys):
            d.ellipse((mapx+xx,mapy+yy,mapx+xx+1,mapy+yy+1),fill=MUTED)
for px,py,num in [(18,12,'1'),(80,25,'2'),(65,22,'3'),(109,18,'4'),(137,32,'5'),(111,8,'6')]:
    d.ellipse((mapx+px-5,mapy+py-5,mapx+px+6,mapy+py+6),fill=RED)
    text(mapx+px-2,mapy+py-5,num,7,True,PAPER)
text(181,944,'01 US · 02 Saudi Arabia',7)
text(181,954,'03 Egypt · 04 Tiangong*',7)
text(181,964,'05 Solomons · 06 N. Korea',7)
text(181,981,'*orbital story; map reference',6,False,MUTED)

# All excluded-news dates are confined to this panel.
line(333,925,333,992)
text(345,925,'DATE CHECK — LEFT OUT AS OLDER NEWS',10,True,RED)
excluded=[
'SOORYAVANSHI’S 53-BALL 204 — 24 Nov',
'HUAWEI GUILTY VERDICT — 24 Nov',
'GIULIANI MEDAL OF FREEDOM — 24 Nov',
'ZELENSKYY LIBYA SINKING CLAIM — 24 Nov',
'UKRAINE HITS SAMARA REFINERIES — 24–25 Nov',
'HASINA SETS DEC 16 RETURN DATE — 24 Nov',
'NETANYAHU JUDGES SUMMON ATTORNEY GENERAL — 24 Nov',
'GERMANY TO BUILD DRONES FOR UKRAINE — 24 Nov',
'CHAMPIONS LEAGUE TUESDAY RESULTS — 24 Nov',
'GUKESH–SINDAROV MATCH OPENS — 24 Nov',
'COP31 COLLAPSES IN ANTALYA — 22 Nov',
'ALCARAZ WINS ATP FINALS — 22 Nov',
]
for i,item in enumerate(excluded):
    xx=345+(i//6)*333
    yy=942+(i%6)*8
    assert d.textlength(item,font=font(6,True))<=324,item
    text(xx,yy,item,6,True,MUTED)
d.rectangle((0,1000,1024,1024),fill=RED)
footer='US tariffs on 14 partners — Houthis claim Ras Tanura, Brent $94.61 — Cairo fire kills 31 — Pakistan’s first astronaut aboard Tiangong.'
assert d.textlength(footer,font=font(10,True))<980
text(22,1005,footer,10,True,PAPER)
im.save(ROOT/'entry.png', optimize=True)
assert (ROOT/'entry.png').stat().st_size<=1048576
print(f'50 stories: 4 leads + {len(briefs)} briefs; {len(regions)} regions; {len(fields)} fields')
print('Regions:', ', '.join(sorted(regions)))
print('Fields:', ', '.join(sorted(fields)))
print('PNG:', im.size, (ROOT/'entry.png').stat().st_size, 'bytes')
