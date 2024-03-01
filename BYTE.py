
def unesi_dimenziju_table():
    print("Unesi dimenziju table: ")
    dimenzija = int(input())
    if (not isinstance(dimenzija, int) or dimenzija < 8 or dimenzija % 2 != 0 or dimenzija > 16 or ((dimenzija*dimenzija-2*dimenzija)/2)%8!=0 ):
        print("Lose izabrana dimenzija table")
        return unesi_dimenziju_table()
    else:
        return dimenzija  

n = unesi_dimenziju_table()

slovaPozicija = {
    'A':0,
    'B':n,
    'C':2*n,
    'D':3*n,
    'E':4*n,
    'F':5*n,
    'G':6*n,
    'H':7*n,
    'I':8*n,
    'J':9*n,
    'K':10*n,
    'L':11*n,
    'M':12*n,
    'N':13*n,
    'O':14*n,
    'P':15*n,
}

brStekovaX = 0
brStekovaO = 0
smerovi = {"DD": [1, 1], "DL": [1, -1], "GD": [-1, 1], "GL": [-1, -1]}

def unesi_prvog_igraca():
    print("Unesi prvog igraca X ili O: ")
    ig=str(input())
    if(ig=='X' or ig=='O'):
        return ig 
    else:
        return unesi_prvog_igraca()
    

def broj_polja(n):
    return n*n

def broj_figura(n): 
     return (n * n - 2*n) / 2 


def broj_stekova(n): 
     return broj_figura(n) / 8 


def unosParametaraIgre():
     dimenzije = unesi_dimenziju_table()
     ko_igra_prvi = unesi_prvog_igraca()
     return dimenzije, ko_igra_prvi


def crno_polje():
    polje=['.','.','.','.','.','.','.','.','.']
    return polje
def belo_polje():
    polje=[' ',' ',' ',' ',' ',' ',' ',' ',' ']
    return polje

#pocetno stanje
def tablaPoc(n):
    tabla=[]
    #s -brojac koji postavlja slova koja oznacavaju vrste
    s=0
    for i in range(n):
        slovo=chr(ord('A') + s)   
        for j in range(n):
            polje=[]
            polje.append(slovo)
            polje.append(j+1)
            #crna polja na tabli su polja kod kojih je i+j deljivo sa 2
            if (j+i)%2==0:
                polje.append(crno_polje())
                if i>0 and i<n-1:
                    if i%2==0:
                        prvi='O'
                    else:
                        prvi='X'
                    polje[2].pop(0)
                    polje[2].insert(0,prvi)
            else:
                polje.append(belo_polje())
            tabla.append(polje)
        s+=1
    return tabla

#Inicijalizacija pocetne tabele
trenutna_tabla=tablaPoc(n)

def unesiPotez():
    print("Unesi potez (Tvoja pozicija slovo, tvoja pozicija broj, od kog elementa prebacujes, koji smer(DD,DL,GD,GL)): ")
    potez = str(input())
    potezList = []
    potezList.append(potez[0])
    potezList.append(potez[2])
    potezList.append(potez[4])
    potezList.append(potez[6]+potez[7])
    da_li_postoji_polje = da_li_postoji(potezList[0],potezList[1],potezList[2],potezList[3])
    da_li_postoji_figura_na_polju = DaLiPostojiFiguraNaPolju(potezList)
    da_li_postoji_figura_na_mestu_u_steku = DaLiPostojiFiguraNaMestuUSteku(potezList)
    da_li_je_smer_validan = DaLiJeSmerValidan(potezList)
    da_li_nije_prva_ili_zadnja_vrsta = DaLiNijePrvaIliZadnjaVrsta(potezList)
    
    if (da_li_postoji_polje==True and da_li_postoji_figura_na_polju==True and 
        da_li_postoji_figura_na_mestu_u_steku==True and da_li_je_smer_validan==True and
        da_li_nije_prva_ili_zadnja_vrsta==True):
        if(DaLiSuSusednaPoljaPrazna(potezList[0], potezList[1])==True):
            if(proveriDaLiIdeKaNajblizem(potezList)==False): #susedna polja su prazna i NE krecemo se ka najblizem steku => los potez, unesi opet
                print("ne kreces se u smeru ka najblizem steku") 
                return unesiPotez()      
        #izvrsavanje poteza
        return(potezList)
    else:
        if(da_li_postoji_figura_na_polju ==False): 
            print("Ne postoji figura na polju")
        return unesiPotez()
#ispituje da li je uneseni potez ispravan tj da li su slova,kolone, mesta u steku i smerovi u opsegu
def da_li_postoji(red,kolona,stmesto,smer):
    if red>='A' and red<chr(ord('A')+n) and kolona>='1' and kolona<=str(n) and stmesto>=str(0) and stmesto<=str(8):
        if red=='A'and (smer=='GL' or smer=='GD'):
            print("Nije moguce GL ni GD")
            return False
        if kolona=='1' and (smer=='GL' or smer=='DL'):
            print("Nije moguce GL ni DL")
            return False
        if kolona==str(n) and (smer=='GD' or smer=='DD'):
             print("Nije moguce GD ni DD")
             return False
        if red==chr(ord('A')+n) and (smer=='DL' or smer=='DD'):
             print("Nije moguce DL ni DD")
             return False
        return True
    else:
        False 
        print("Nije dobro> Vrste su od A do "+ chr(ord('A')+n-1)+", kolone su od 1 do "+ str(n)+", a mesta u steku od 0 do 7" )   
    
#stanje trenutne table prilagodjeno za iscrtavanje  
def trenutno_stanje():
    tab=trenutna_tabla
    tabla= [[ ' ' for _ in range(n*4)] for _ in range(n*4)]
    #r- brojac kojim se se uzimaju odgovarajuce liste iz tabele za citanje kolona  
    r=0
    #br- brojac za polja velike matrice koja se iscrtava (tj. broj svih listi u tabeli)
    br=0
    #max je 4*n jer svako polje je predstavljeno sa 4*4(da bi postojali razmaci izmedju polja(ili za pisanje slova ili brojeva) i 3*3 za stek)
    for i in range(0,4*n,4):
        #k -brojac kojim se uzimaju odgovarajuce liste iz tabele za citanje vrsta  
        k=i    
        for j in range(0,4*n,4):   
            #za ispisivanje brojeva
            if i==0 :
                tabla[i][j+2]=tab[k][1]
                k+=1
            #za ispisivanje slova
            if j==0 :
                tabla[i+2][j]=tab[r][0]
                r+=n      
            #za ispisivanje stanja steka
            if i%4==0 and j%4==0:
                polje=tab[br][2]
                if br<n*n:
                    br+=1
                    #z- brojac za pristupanje elementima steka
                    z=0
                    #s i d- za iscrtavanje steka na velikoj tabli
                    for s in range(3):
                        for d in range(3):
                            tabla[i+1+s][j+1+d]=polje[z]
                            z+=1
    return tabla

#iscrtavanje table u terminalu
def print_tab(tabla):
    for row in tabla:
        for element in row:
            print(element,end=" ")
        print()

##########################################################################Neda

def DaLiPostojiFiguraNaPolju(potezList):
    #Proveriti da li postoje figure na zadatom polju(ono sa kojeg smo izabrali da se pomerimo)
    potez = 0; #potez je pozicija na kojoj smo
    #potez se racuna kao pomeraj u matrici u odnosu na slovo vrste u kojoj smo + pomeraj u odnisu na broj kolone
    potez+=slovaPozicija[str(potezList[0])]
    potez+=int(potezList[1])-1
    ima = False 
    
    for i in range(9):
        if(trenutna_tabla[potez][2][i]=='X' or trenutna_tabla[potez][2][i]=='O'): 
            ima = True
  
    return ima

def DaLiPostojiFiguraNaMestuUSteku(potezList):
    #Proveriti da li postoje figure na zadatom polju(ono sa ojeg smo izabrali da se pomerimo)
    potez = 0; #potez je pozicija na kojoj smo
    potez+=slovaPozicija[str(potezList[0])]
    potez+=int(potezList[1])-1
    #print(potez)
    ima = False 
    stekMesto = int(potezList[2])
    if(trenutna_tabla[potez][2][stekMesto]=='X' or trenutna_tabla[potez][2][stekMesto]=='O'):
        ima = True
    else:
        print("Ne postoji figura na tom mestu u steku") 
    return ima

def DaLiJeSmerValidan(potezList):
    #Proveriti da li je smer jedan od četiri moguća
    smer = potezList[3]
    validan = False
    if(smer=="DD" or smer == "DL" or smer=="GL" or smer=="GD"):
        validan=True
    else:
        print("Nije validan smer")
    return validan

def DaLiJeKrajIgre():
    #da li je tabla prazna
    prazna = DaLiJeTablaPrazna()
    #da li bilo kkoji igrac ima barem max_stekova/2+1 stekova
    max_stekova = broj_stekova(n)
    max_br_stekova_jedan_igrac = (int)(max_stekova//2)+1
    if(prazna==True or (brStekovaO>=max_br_stekova_jedan_igrac or brStekovaX>=max_br_stekova_jedan_igrac)):
        if(brStekovaO>=max_br_stekova_jedan_igrac):
            print("KRAJ IGRE! POBEDNIK JE O")
        else:
            print("KRAJ IGRE! POBEDNIK JE X")
        return True
       
    return False

def DaLiNijePrvaIliZadnjaVrsta(potezlist): #vraca true ako potez NE PRELAZI u prvu ili zadnju vrstu
    slovo = potezlist[0]
    smer = potezlist[3]
    if(n==8):
        novoslovo = 'G'
    if(n==10):
        novoslovo = 'I'
    if(n==16):
        novoslovo = 'O'
    if(slovo=='B' and (smer == "GL" or smer == "GD")):
       print("ne mozete se kretati gore sa ove pozicije")
       return False
    if(slovo==novoslovo and (smer=="DL" or smer == "DD")):
        print("ne mozete se kretati dole sa ove pozicije")
        return False
    return True



def DaLiJeTablaPrazna():
    #s -brojac koji postavlja slova koja oznacavaju vrste
    s=1
    for i in range(1,n-1):
        slovo=chr(ord('A') + s) 
        for j in range(n):
            #crna polja na tabli su polja kod kojih je i+j deljivo sa 2
            #a crna polja su ona na kojima se nalaze figure
            if (j+i)%2==0:
                lista = [slovo, j+1, 0,0]#simuliramo slanje poteza funkciji da li postoji figura na polju,
                #a tu nam 3 i 4 parametar nisu bitni pa saljemo 0
                if(DaLiPostojiFiguraNaPolju(lista)==True):
                    
                    return False
        s+=1
    print("tabla JESTE prazna")
    return True
    


#Funkcija koja proverava da li su susedna polja prazna:

def DaLiSuSusednaPoljaPrazna(slovo, broj): 
    redovi = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'] 
    indeks_slova = slovaPozicija[slovo] 
    indeks_reda = redovi.index(slovo) 
    indeks_kolone = (int)(broj) - 1
    
    dijagonalna_polja = []
    # proverava da li trenutna pozicija nije na prvom redu i nije u prvoj koloni. Ako nije, dodaje se koordinata polja gore-levo u listu dijagonalna_polja
    if indeks_reda > 0 and indeks_kolone > 0:
        dijagonalna_polja.append([redovi[indeks_reda-1], indeks_kolone-1])
    #proverava da li trenutna pozicija nije na prvom redu i nije u poslednjoj koloni. Ako nije, dodaje se koordinata polja gore-desno u listu dijagonalna_polja
    if indeks_reda > 0 and indeks_kolone < (n-1):
        dijagonalna_polja.append([redovi[indeks_reda-1], indeks_kolone+1])
    #proverava da li trenutna pozicija nije na poslednjem redu i nije u prvoj koloni. Ako nije, dodaje se koordinata polja dole-levo u listu dijagonalna_polja
    if indeks_reda < (n-1) and indeks_kolone > 0:
        dijagonalna_polja.append([redovi[indeks_reda+1], indeks_kolone-1])
    #da li trenutna pozicija nije na poslednjem redu i nije u poslednjoj koloni. Ako nije, dodaje se koordinata polja dole-desno u listu dijagonalna_polja
    if indeks_reda < (n-1) and indeks_kolone < (n-1):
        dijagonalna_polja.append([redovi[indeks_reda+1], indeks_kolone+1])
    
    #Za svako polje, uzima se prva komponenta koordinate (red) i druga komponenta (kolona). Pozicija polja se određuje kao slovaPozicija[red] + kolona.
    #Proverava se da li je vrednost polja trenutne_table na odgovarajućoj poziciji [pozicija][2][0] različita od '.'. Ako jeste, to znači da polje nije prazno, pa se funkcija odmah prekida i vraća se False
    for polje in dijagonalna_polja:
        red = polje[0]
        kolona = polje[1]
        pozicija = slovaPozicija[red] + kolona
    
        if trenutna_tabla[pozicija][2][0] != '.':
            return False
    #Ako svi uslovi provere za dijagonalna polja prođu, znači da su sva susedna polja prazna. Zato se na kraju vraća True.
    return True


#####Realizovati funkcije koje na osnovu konkretnog poteza i stanje igre proveravaju da li on vodi ka jednom od najbližih stekova (figura)
import heapq
def nadji_najblizi_stek(pozicija, tabla):#vraca listu pozivija najblizih stekova na koje MOZE da se prebaci
    red = pozicija[0]
    kolona = int(pozicija[1])-1#-1 jer je tabla nacrtana od 1-n, a nama je od 0-n-1
    poz=[red,kolona]
    min_heap = []
    def rastojanje(p1, p2):
        return max(abs(ord(p1[0]) - ord(p2[0])), abs(p1[1] - p2[1]))
    
    #rastojanje svih stekova koji postoje na koje nas moze da se pomeri
    for i in range(n):
        for j in range(n):
            if (i!=red and j!=kolona and (j+i)%2==0 and (tabla[n*i+j][2][0]=='X' or tabla[n*i+j][2][0]=='O') and DaLiJeDozvoljenoPomeranjeSteka(pozicija,tabla[slovaPozicija[red]+kolona][2],tabla[n*i+j][2])==True):
                distanca = rastojanje(poz, (chr(i+65), j))
                heapq.heappush(min_heap, (distanca, (chr(i+65), j+1)))
    
    listaNajblizih = []
    while min_heap:
        dist, najPoz = heapq.heappop(min_heap)#prvi je najblizi(najmanja distanca)
        listaNajblizih.append(najPoz)
        #proverava da li je jos neki stek na istoj udaljenosti
        if min_heap and min_heap[0][0] == dist:
            continue
        else:
            break
    return listaNajblizih

def proveriDaLiIdeKaNajblizem(potez):#uzima pozicije najblizih stekova i u zavisnosti od njih preracunava da li smer odgovara
    najblizi=nadji_najblizi_stek(potez, trenutna_tabla)
    if(najblizi==[]):
        print("Nema najblizih stekova preci na sledeceg igraca")
        return False
    kolona=int(potez[1])
    for l in najblizi:
        if l[0]<potez[0]:#najblizi je iznad 
            if l[1]<kolona:
                if potez[3]=='GL':
                    return True
            if l[1]==kolona:
                if potez[3]=='GL' or potez[3]=='GD':
                    return True
            if l[1]>kolona:
                if potez[3]=='GD':
                    return True
        if l[0]==potez[0]:#najblizi u istom redu
            if l[1]<kolona:
                if potez[3]=='GL' or potez[3]=='DL':
                    return True
            if l[1]>kolona:
                if potez[3]=='GD'or potez[3]=='DD':
                    return True
        if l[0]>potez[0]:#najblizi je ispod
            if l[1]<kolona:
                if potez[3]=='DL':
                    return True
            if l[1]==kolona:
                if potez[3]=='DL' or potez[3]=='DD':
                    return True
            if l[1]>kolona:
                if potez[3]=='DD':
                    return True         
    return False
#funkcije koje na osnovu zadatog igrača na potezu i zadatog stanje igre (table) formiraju sve moguće poteze->listu sa listom dobrih i listom losih poteza
def moguciPoteziIgrac(igrac):
    dobri=[]
    losi=[]
    #obilazi se cela tabla i posecuju crna polja
    for i in range(n):
        for j in range(n): 
            if (j+i)%2==0:
                red=trenutna_tabla[n*i+j][0]
                kolona=trenutna_tabla[n*i+j][1]
                stek=trenutna_tabla[n*i+j][2]
                pozicijaFigureUSteku=0
                if(stek[0]=='X'or stek[0]=='O'):#da li postoji figura na polju
                    while stek[pozicijaFigureUSteku]!='.':#prolazi kroz sve figure u steku
                        
                        if stek[pozicijaFigureUSteku]==igrac:#proverava da li je figura od zadatog igraca
                            if pozicijaFigureUSteku==0:#samo ako je nulta pozicija proverava da li su sva susedna polja prazna,jer ni jedna sa vecom pozicijom ne moze na prazno polje
                                if DaLiSuSusednaPoljaPrazna(red,kolona)==True: #ako su susedna polja prazna
                                    #proveravamo za slucajeve koji nisu granicni
                                    pote=[red,kolona,pozicijaFigureUSteku,'GL'] 
                                    if int(kolona)-1!=0 and red!='B':
                                        if proveriDaLiIdeKaNajblizem(pote):
                                            dobri.append(pote)
                                        else:
                                            losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'GD'] 
                                    if int(kolona)!=n and red!='B':
                                        if proveriDaLiIdeKaNajblizem(pote):
                                            dobri.append(pote)
                                        else:
                                            losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'DL']
                                    if int(kolona)-1!=0 and red!=chr(n+65-2): 
                                        if proveriDaLiIdeKaNajblizem(pote):
                                            dobri.append(pote)
                                        else:
                                            losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'DD'] 
                                    if int(kolona)!=n and red!=chr(n+65-2):
                                        if proveriDaLiIdeKaNajblizem(pote):
                                            dobri.append(pote)
                                        else:
                                            losi.append(pote)
                            #granici slucajevi
                            if red=='B': 
                                    losi.append([red,kolona,pozicijaFigureUSteku,'GL'])
                                    losi.append([red,kolona,pozicijaFigureUSteku,'GD'])
                                    pote=[red,kolona,pozicijaFigureUSteku,'DL']
                                    if int(kolona)-1!=0  and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j-1][2]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'DD']
                                    if  int(kolona)!=n and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j+1]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                            if int(kolona)-1==0: 
                                    losi.append([red,kolona,pozicijaFigureUSteku,'GL'])
                                    losi.append([red,kolona,pozicijaFigureUSteku,'DL'])
                                    pote=[red,kolona,pozicijaFigureUSteku,'GD']
                                    if red!='B' and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j+1][2]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'DD']
                                    if  red!=chr(n+65-2) and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j+1]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                            if red==chr(n+65-2):#pretposlednje slovo  
                                    losi.append([red,kolona,pozicijaFigureUSteku,'DD'])
                                    losi.append([red,kolona,pozicijaFigureUSteku,'DL'])
                                    pote=[red,kolona,pozicijaFigureUSteku,'GL']
                                    if int(kolona)-1!=0  and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j-1][2]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'GD']
                                    if  int(kolona)!=n and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j+1]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                            if int(kolona)==n: 
                                    losi.append([red,kolona,pozicijaFigureUSteku,'DD'])
                                    losi.append([red,kolona,pozicijaFigureUSteku,'GD'])
                                    pote=[red,kolona,pozicijaFigureUSteku,'GL']
                                    if red!='B' and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j-1][2]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                                    pote=[red,kolona,pozicijaFigureUSteku,'DL']
                                    if  red!=chr(n+65-2) and DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j-1]):
                                        dobri.append(pote)
                                    else:
                                        losi.append(pote)
                            #svi ostali slucajevi
                            if red!='B' and red!=chr(n+65-2) and int(kolona)-1!=0 and int(kolona)!=n:
                                pote=[red,kolona,pozicijaFigureUSteku,'GL'] 
                                if DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j-1][2]):
                                    dobri.append(pote)
                                else:
                                    losi.append(pote)
                                pote=[red,kolona,pozicijaFigureUSteku,'GD'] 
                                if DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i-1)+j+1][2]):
                                    dobri.append(pote)
                                else:
                                    losi.append(pote)
                                pote=[red,kolona,pozicijaFigureUSteku,'DL'] 
                                if DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j-1][2]):
                                    dobri.append(pote)
                                else:
                                    losi.append(pote)
                                pote=[red,kolona,pozicijaFigureUSteku,'DD'] 
                                if DaLiJeDozvoljenoPomeranjeSteka(pote,stek,trenutna_tabla[n*(i+1)+j+1][2]):
                                    dobri.append(pote)
                                else:
                                    losi.append(pote)
                        pozicijaFigureUSteku+=1
    #Izbacivanje ako se ponavlja nesto ->set
    tupleDob = tuple(tuple(inner_list) for inner_list in dobri)
    setDobri = set(tupleDob)
    tupleLos = tuple(tuple(inner_list) for inner_list in losi)
    setLosi = set(tupleLos)
    #vracamo sve el kao liste
    samoDobri=[]
    for el in setDobri:
        samoDobri.append(list(el))
    samoLosi=[]
    for el in setLosi:
        samoLosi.append(list(el))
    listaPoteza=[sorted(samoDobri),sorted(samoLosi)]                    
    return listaPoteza


def SvaMogucaStanja():
    stanja=moguciPoteziIgrac('X'),moguciPoteziIgrac('O')
    return stanja

#Proverava da li figura(i sve iznad nje) iz steka1 moze da se prebaci na stek2 
def DaLiJeDozvoljenoPomeranjeSteka(potez,stek1,stek2):
    brFig1=0
    brFig2=0
    for e in stek1:
        if e !='.':
            brFig1+=1
    for l in stek2:
        if l !='.':
            brFig2+=1
    
    if(DaLiSuSusednaPoljaPrazna(potez[0], int(potez[1]))==False):
        
        #Ovde ovo prvo brFig2 predstavlja poziciju novog steka na koju se smestaju figura iz starog ovo je uvedeno zbog pravila na 15. slajdu
        if (brFig2>int(potez[2]) and brFig1+brFig2<=8):
            return True
        else:
            return False
    else:
        return True #ako su susedna prazna pomeri
    

#omogucava da se stek sa jednog polja obrise i premesti na drugo polje
def promena_stanja(potez):
        stariStek=[]
        stariStek=trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1][2]
        
        lSlPozicija=smerovi[potez[3]]
        noviStek=trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1+lSlPozicija[0]*n+lSlPozicija[1]][2]
        #brFig odredjuje br figura na novom polju,tj. pozicija na steku novog polja na koju se nadovezuju figure koje zelimo da pomerimo 
        brFig=0
        for el in noviStek:
            if el!='.':
                brFig+=1

        if(DaLiJeDozvoljenoPomeranjeSteka(potez,stariStek,noviStek)==True):
            stPom=[]
            i=int(potez[2])
            v=stariStek[i]
            #uzimju se samo figure sa polja koje zelimo da pomerimo,pocevsi od pozicije v koju smo naveli u potezu 
            while v !='.':
                stPom.append(v)
                i+=1
                v=stariStek[i]
            
            b=int(potez[2])
            #prakticno se figure koje zelimo da pomerimo brisu
            for b in range(int(potez[2]),9):
                trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1][2][b]='.'
            #figura/e koje smo pomerili sa starog polja, nadovezujemo na stek novog polja
            for j in stPom:
                trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1+lSlPozicija[0]*n+lSlPozicija[1]][2][brFig]=j
                brFig+=1
            
            if(brFig==8):
                if(trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1+lSlPozicija[0]*n+lSlPozicija[1]][2][brFig-1]=='X'):
                    global brStekovaX 
                    brStekovaX+=1
                    print("broj stekova X: ")
                    print(brStekovaX)
                else:
                    global brStekovaO
                    brStekovaO+=1
                    print("broj stekova O: ")
                    print(brStekovaO)
                trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1+lSlPozicija[0]*n+lSlPozicija[1]][2]=crno_polje() 


            return trenutna_tabla
        else:
            
            return 0

#proverava da li je figura koja treba da se pomeri od odgovarajuceg igraca
def daLiIgracMozeDaPomeriFiguru(igrac,potez):
    figura=trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1][2][int(potez[2])]
    if(figura==igrac):
        return True
    else:
        print("Ova figura ne pripada igracu "+ igrac)
        return False
    


import math
def minimax(igrac, dubina, alpha, beta, max_igrac, potez, naj_potez = None):
    if dubina == 1:
        return heuristika(potez, igrac, max_igrac), potez

    if max_igrac:
        max_heuristika = float('-inf')
        svi_potezi = moguciPoteziIgrac(igrac)[0] #dobri potezi
        
        for pot in svi_potezi:
            tr_heuristika, _ = minimax(igrac, dubina + 1, alpha, beta, False, pot, naj_potez)
            if tr_heuristika > max_heuristika:
                max_heuristika = tr_heuristika
                naj_potez = pot
            alpha = max(alpha, tr_heuristika)
            if beta <= alpha:
                break
        print("max naj je: "+ str(naj_potez)+ "MAX heuristika je: " + str(max_heuristika))
        return max_heuristika, naj_potez
    else:
        min_heuristika = float('inf')
        svi_potezi = moguciPoteziIgrac(igrac)[0]
        naj_potez = None

        for pot in svi_potezi:
            tr_heuristika, _ = minimax(igrac, dubina + 1, alpha, beta, True, pot, naj_potez)
            if tr_heuristika < min_heuristika:
                min_heuristika = tr_heuristika
                naj_potez = pot
            beta = min(beta, tr_heuristika)
            if beta <= alpha:
                break
        print("min naj je: "+ str(naj_potez) + "min heuristika je: " + str(min_heuristika))
        return min_heuristika, naj_potez


def heuristika( potez, igrac, max_igrac):  
    a=0
    b=0
    c=0
    visina = potez[2] 
    a = (8-visina)*3  
    
    pozicija = 0; #pozicija na mesto na tabli gde smo
    pozicija+=slovaPozicija[str(potez[0])]
    pozicija+=int(potez[1])-1
    trenutni_stek = trenutna_tabla[pozicija][2]
    figura=''
    for pot in reversed(trenutni_stek):
        if(pot != '.'):
            figura = pot #figura je figura na vrhu steka
            break
    
    visinapom=visina
    visina_stek_prvi = 0
    while(visinapom<9):
        if(trenutna_tabla[pozicija][2][visinapom]!='.'):
            visina_stek_prvi+=1
        visinapom+=1
    
    if(DaLiSuSusednaPoljaPrazna(potez[0],potez[1]) ==False): #ako susedna polja nisu prazna
        smer=smerovi[potez[3]]
        noviStek=trenutna_tabla[slovaPozicija[potez[0]]+int(potez[1])-1+smer[0]*n+smer[1]][2]
    else: #susedna polja su prazna
        najblizi=nadji_najblizi_stek(potez, trenutna_tabla)
        najblizi_stek=[] 
        if(najblizi==[]): 
            print("Nema najblizih stekova preci na sledeceg igraca")
            return False
        kolona=int(potez[1])
        for l in najblizi: #proveravamo da li se kolona unetog poteza slaze sa kolonom u nekom od poteza koji vode ka najblizim stekovima
            if l[0]<potez[0]:#najblizi je iznad 
                if l[1]<kolona:
                    if potez[3]=='GL':
                        najblizi_stek.append(l)
                if l[1]==kolona:
                    if potez[3]=='GL' or potez[3]=='GD':
                        najblizi_stek.append(l)
                if l[1]>kolona:
                    if potez[3]=='GD':
                        najblizi_stek.append(l)
            if l[0]==potez[0]:#najblizi u istom redu
                if l[1]<kolona:
                    if potez[3]=='GL' or potez[3]=='DL':
                        najblizi_stek.append(l)
                if l[1]>kolona:
                    if potez[3]=='GD'or potez[3]=='DD':
                        najblizi_stek.append(l)
            if l[0]>potez[0]:#najblizi je ispod
                if l[1]<kolona:
                    if potez[3]=='DL':
                        najblizi_stek.append(l)
                if l[1]==kolona:
                    if potez[3]=='DL' or potez[3]=='DD':
                        najblizi_stek.append(l)
                if l[1]>kolona:
                    if potez[3]=='DD':
                        najblizi_stek.append(l)
        noviStek=najblizi_stek      
    visina_stek_drugi = 0
    for x in noviStek:
        if(x!='.'):
            visina_stek_drugi+=1
    visina_novog_steka = visina_stek_prvi + visina_stek_drugi
   
    if(figura==igrac):
        b=31
        c = visina_novog_steka * 7 
    else:
        c = visina_novog_steka * 5
        b=17
    
    heuristic = a+b+c
    print("HEURISTIKA ZA POTEZ: "+ str(potez) + " JE :  "+ str(heuristic))
    if(max_igrac):
        return -heuristic
    else:
        return heuristic


def igra():
    print("izaberi svog igraca.")
    ig=unesi_prvog_igraca() #ig je moj igrac, i on igra prvi
    racunar=''
    if(ig=='X'):
        racunar='O'
    else: racunar='X'
    print("moj igrac je " + ig + ", a racunar je " + racunar)
    print_tab(trenutno_stanje())
    while (DaLiJeKrajIgre()==False):
        if(racunar!=ig): 
            print("IGRAC "+ig)
            print("DOBRI POTEZI ")
            print(moguciPoteziIgrac(ig)[0]) 
            print("LOSI POTEZI ")
            print(moguciPoteziIgrac(ig)[1])
            if(moguciPoteziIgrac(ig)[0] != []):
                #ako igrac ima dobre poteze koje moze da odigra
                potez=unesiPotez()
                print("potez je:")
                print(potez)
                if daLiIgracMozeDaPomeriFiguru(ig,potez)==True:
                    while(promena_stanja(potez) == False):
                        potez = unesiPotez()
                    print_tab(trenutno_stanje())
                else:
                    potez=unesiPotez()
                    while daLiIgracMozeDaPomeriFiguru(ig,potez)==False:
                        potez=unesiPotez()
                    promena_stanja(potez)
                    print_tab(trenutno_stanje())
            else:
                print("NEMA DOBRIH POTEZA KOJI SE MOGU ODIGRATI, PROTIVNIK JE NA POTEZU!")

        else:
            poc_potez = ['B', 2, 0, 'DD'] 
            vraca_h, najj = minimax(ig, 0, float('-inf'), float('inf'), True, poc_potez)
            print(najj)
            promena_stanja(najj)
            print_tab(trenutno_stanje())
        if ig=='X':
            ig='O'
        else:
            ig='X'



igra()
    



