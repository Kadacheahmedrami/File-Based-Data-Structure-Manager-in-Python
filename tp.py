from pickle import dumps, loads
from sys import getsizeof
global b
global tnom
global tprénom 
global tmat
global tniveau 
global tsupprimer
global bufsize 
b = 2
tmat = 20
tnom = 20
tprenom = 20
tniveau = 10
tsupprimer = 1
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tsupprimer)
buf = [0, [etud1] * b,-1] 
bufsize = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) 


def affecter_entete(f, offset, val):
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return

def ecrireBloc(f, ind, buff):
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

def lirebloc(f, ind) :
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    buf = f.read(bufsize)
    return (loads(buf))

from os.path import getsize 


def entete(f, ind):
    if getsize(f.name) == 0:
        return 0  # Return 0 si le fichier est vide

    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)

# recherche aux niveu de l index 
def recher_dicho(v,indexprim):
    trouve =False
    low=0
    high = len(indexprim) - 1

    while low <= high:
        mid = (low + high) // 2
        matricul_courant = int(indexprim[mid][0])

        if matricul_courant == v:
            trouve=True
            return [indexprim[mid],trouve]
        elif matricul_courant < v:
            low = mid + 1 
        else:
            high = mid - 1 


    return [indexprim[low],trouve]

# recherche sequentiel aux niveu de fichier principale et fichier de debordement
def recherche_seq(filename,i,clee):
    clee=str(clee)
    trouve=False
    f=open(filename+".txt",mode='rb')
    buf=lirebloc(f,i)
    j=0
    while (j < buf[0] and trouve==False):
        e= buf[1][j]
        Matricule = e[0:tmat].replace('#','')
        if(Matricule==clee):
            e=afficher_enreg(e)
            trouve=True
        j=j+1
    if (trouve== True):
        f.close()
        return[e,trouve,i,j]
    else:
        if(buf[2]==-1):
            f.close()
            return["vide0",trouve,i,j]
        else:
            fdeb=open(filename+"_deb.txt",mode='rb')
            d=buf[2]
            while(d != -1 and trouve ==False ):
                buf=lirebloc(fdeb,d)
                j=0
                while (j < buf[0] and trouve==False):
                    e= buf[1][j]
                    Matricule = e[0:tmat].replace('#','')
                    
                    if(Matricule==clee):
                        e=afficher_enreg(e)
                        trouve=True
                    j=j+1
                d=buf[2]  # d = buf.suiv
            if (trouve== True):
               f.close()
               return[e,trouve,i,j]
            else:
               f.close()
               return["vide1",trouve,i,j]
  
def recherche(index,v,file_name):
      
       R=recher_dicho(v,index)  #recherche deichotomique retourner adresse de energe
       print(recherche_seq(file_name,R[0][1],v)) # recherche sequentielle aux niveu de bloc et zone debordement
        
def resize_chaine(chaine, maxtaille):
   
    for i in range(len(chaine),maxtaille):
          chaine = chaine + '#' 
    return chaine



def afficher_enreg(e):
    Matricule = e[0:tmat].replace('#','')
    Nom = e[tmat:tnom+tmat].replace('#','')
    Prenom = e[tmat+tnom:tnom+tmat+tprenom].replace('#','') # eroor Prenom = e[tmat+tnom:tprenom].replace('#',' ')
    Niveau = e[tmat+tnom+tprenom:len(e) - 1].replace('#','')
    Supprimer = e[-1]
    return "matricule : "+Matricule + '       ' + "nom : "+Nom + '       ' +"prenom : "+ Prenom + '        ' + "niveu  : "+Niveau + '         '+ "supression : " + str(Supprimer)



# cette fonction est pour le fichier principale seulment
# on peut pas utuliser cette fonction dans le fichier de debordement
def afficher_fichier_deb():
    fn = input('Entrer le nom du fichier à afficher: ')
    filen=fn
    fn=fn+".txt"
    f = open(fn,'rb')
    nbrblock = entete(f,1) 
    print(f'votre fichier contient {nbrblock} block \n')
    for i in range (0,nbrblock):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n  zonne deb: {buf[2]} \n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): 
                print(afficher_enreg(buf_tab[j] +'\n'))
        #aficher le partie de zone de debordement
        if(buf[2] != -1):
            print("\n partie zone de debodement:\n")
            fdeb=open(filen+"_deb.txt",mode='rb+')
            d=buf[2]
            while(d != -1 ):
                buf=lirebloc(fdeb,d)
                buf_tab=buf[1]
                for j in range(buf_nb):
                    if (buf_tab[j][-1] == '0'): 
                        print(afficher_enreg(buf_tab[j]))
                d=buf[2] 
            fdeb.close()
        print('\n\n')   
        
    f.close()
    return

# on peut utuliser cette fonction pour aficher qlq fichier
# on peut l'utuliser pour aficher le fichier de debordement
def afficher_fichier():
    fn = input('Entrer le nom du fichier à afficher: ')
    filen=fn
    fn=fn+".txt"
    f = open(fn,'rb')
    nbrblock = entete(f,1) 
    print(f'votre fichier contient {nbrblock} block \n')
    for i in range (0,nbrblock):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n  zonne deb: {buf[2]} \n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): 
                print(afficher_enreg(buf_tab[j] +'\n'))
    
        
    f.close()
    return




def Chargement_initial(fname):
 
    j = 0 
    i = 0 
    n = 0 
    fn_deb= fname + "_deb.txt"
    fn= fname +".txt"
    buf_tab = [etud1]*b
    buf_nb = 0 
    try:
        f = open(fn, "wb")
        fdeb= open(fn_deb,"wb")
    except:
        print("Creation du fichier est impossible ")
    rep = 'O'
    indexprim= []
    while (rep.upper() == 'O'):
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')

        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)

        e = Matricule + Nom + Prenom + Niveau + '0' 
        n += 1
        if(j < b): # index sera cree dans le meme temps MC
            index= [Matricule,i,j,'fp'] # fp indique que l'engestrement existe dans le fichier principale
            indexprim.append(index)
            buf_tab[j] = e
            buf_nb += 1 
            j += 1
           
        else: 
            index= [Matricule,i+1,0,'fp'] # fp indique que l'engestrement existe dans le fichier principale
            indexprim.append(index)
            buf=[buf_nb, buf_tab,-1]   
            ecrireBloc(f, i, buf)
            buf_tab=[etud1] * b 
            buf_nb = 1 
            buf_tab[0] = e
            j = 1
            i += 1 
        rep = input("do you want to add another student O/N ? ")
    
    buf=[j,buf_tab,-1]
    ecrireBloc(f, i, buf) 
    affecter_entete(f, 0, n) 
    affecter_entete(f, 1, i+1)
    f.close()
    fdeb.close()
    return indexprim






def creeindex(fname):
    try:
        f = open(fname+".txt", "rb")
    except:
        print("Creation du fichier est impossible ")
    indexprim= []
    nbrblock = entete(f,1) 
    for i in range (0,nbrblock):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        for j in range(buf_nb):
            e=buf_tab[j]
            Matricule = e[0:tmat].replace('#','')
            Matricule= int(Matricule)
            index= [Matricule,i,j,'fp'] # fp indique que l'engestrement existe dans le fichier principale

            indexprim.append(index)
    f.close()
    
    
    try:
        f = open(fname+"_deb.txt", "rb")  # on ajoute les elemtns de zone de debordement dans l index 
    except:
        print("Creation du fichier est impossible ")
   
    nbrblock = entete(f,1) 
    if(nbrblock != 0):
        for i in range (0,nbrblock):
            buf = lirebloc(f,i)
            buf_nb = buf[0]       
            buf_tab = buf[1]
            for j in range(buf_nb):
                e=buf_tab[j]
                Matricule = e[0:tmat].replace('#','')
                Matricule= int(Matricule)
                index= [Matricule,i,j,'fd'] # fd indique que l'engestrement existe dans le fichier de debordement
                indexprim.append(index)
                
    f.close()
    sorted_index = sorted(indexprim, key=lambda x: x[0])

    return sorted_index      




    

def insertion(fn,index):
    
    Nom = input('Donner le nom : \n')
    Prenom = input('Donner le prenom : \n')
    Matricule = input('Donner le matricule : \n')
    Niveau = input('Donner le niveau : \n')
    Matricule = resize_chaine(Matricule, tmat)
    Nom = resize_chaine(Nom, tnom)
    Prenom = resize_chaine(Prenom, tprenom)
    Niveau = resize_chaine(Niveau, tniveau)
    e = Matricule + Nom + Prenom + Niveau + '0'
    Matricule=Matricule.replace("#",'')
    v=int(Matricule) 
    R=recher_dicho(v,index)
    if(R[1]==True):
    
        (print("on peut pas inserer"))
    else:

       

        try:
            f = open(fn+".txt",'rb+')
        except:
            print("impossible d'ouvrir le fichier en mode d'écriture ")
            return
        
        
        
        nbrblock=entete(f,1)
       
        if(R[0][1]==nbrblock-1):
            buf=lirebloc(f,nbrblock-1)
            buf_nb=buf[0]
            if (buf_nb==b):
                buf_tab = [etud1]*b
                buf_nb = 1
                buf_tab[0]=e
                buf=[buf_nb,buf_tab,-1]
                ecrireBloc(f,nbrblock,buf)
                affecter_entete(f,1,nbrblock+1)
                

            else:
                buf_tab=buf[1]
                buf_tab[buf_nb]= e 
                buf_nb=buf_nb+1
                buf=[buf_nb,buf_tab,buf[2]]
                ecrireBloc(f,nbrblock-1,buf)
              
        else:
            
            fdeb=open(fn+"_deb.txt",'rb+')
            buf=lirebloc(f,R[0][1])
            nbrblock=entete(fdeb,1)

            if(buf[2]== -1):
                buf[2]=nbrblock
                ecrireBloc(f,R[0][1],buf)
                buf_tab=[etud1]*b
                buf_tab[0]=e
                buf_nb=1
                buf=[buf_nb,buf_tab,-1]
                affecter_entete(fdeb,1,nbrblock+1)
               
                ecrireBloc(fdeb,nbrblock,buf)
               
                
            else:
                
                d=buf[2]
                x=d # sauvgarder l'indice de tete 
                buf=lirebloc(fdeb,d) 
                d=buf[2]
                while(d != -1):
                    x=d # sauvgarder l indice de precedent dans la boucle
                    buf=(lirebloc(fdeb,d))
                    d=buf[2]

                buf_nb=buf[0]
                if (buf_nb==b):
                    buf[2]=nbrblock  # buf.suiv = indice de neuveu bloc allouer 
                    ecrireBloc(fdeb,x,buf)
                    buf_tab = [etud1]*b
                    buf_nb = 1
                    buf_tab[0]=e
                    buf=[buf_nb,buf_tab,-1]
                    ecrireBloc(fdeb,nbrblock,buf)
                    affecter_entete(fdeb,1,nbrblock+1)
                   

                else:
                    
                    buf_tab=buf[1]
                    buf_tab[buf_nb]= e 
                    buf_nb=buf_nb+1
                    buf=[buf_nb,buf_tab,-1]
                    ecrireBloc(fdeb,x,buf)

            fdeb.close()

                
               

        #insertion aux niveu de la table index
        index=creeindex(fn)
        f.close()
        return index
        


def suppression_Logique(fn,v,index):
    clee=int(v)
    R = recher_dicho(clee,index)
    if(R[1]==True):
        try:
            f = open(fn+".txt", 'rb+')
        except:
            print("Impossible d'ouvrir le fichier en mode écriture.")
        
        trouve=False
        
        buf=lirebloc(f,R[0][1])
        j=0
        while (j < buf[0] and trouve==False):
            e= buf[1][j]
            Matricule = e[0:tmat].replace('#','')
            if(Matricule==v):
                e=e[0:tmat + tnom + tprenom + tniveau]+'1'
                buf[1][j]=e
                ecrireBloc(f,R[0][1],buf)
                e=afficher_enreg(e)
                trouve=True
            j=j+1
        if (trouve== True):
            f.close()
            return
        else:
            if(buf[2]==-1):
                f.close()
                return
            else:
                fdeb=open(fn+"_deb.txt",mode='rb+')
                d=buf[2]
               
                while(d != -1 and trouve ==False ):
                    buf=lirebloc(fdeb,d)
                    j=0
                    while (j < buf[0] and trouve==False):
                        e= buf[1][j]
                        Matricule = e[0:tmat].replace('#','')
                        
                        if(Matricule==v):
                            e=e[0:tmat + tnom + tprenom + tniveau]+'1'
                            buf[1][j]=e
                            ecrireBloc(f,d,buf)
                            trouve=True
                        j=j+1
                  
                    d=buf[2]  # d = buf.suiv
                if (trouve== True):
                    f.close()
                    return
                else:
                    f.close()
                    return  

    else:
        print("cette element n'existe pas")

def Reorganisation(fn):
    energtable=[]
    filen=fn
    fn=fn+".txt"
    f = open(fn,'rb')
    nbrblock = entete(f,1) 
    for i in range (0,nbrblock):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n  zonne deb: {buf[2]} \n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): # pour eliminer les enegestrement suprimer logiquement
                energtable.append(buf_tab[j])  #recupirer les energ dans un tableu

        if(buf[2] != -1):
            print("\n partie zone de debodement:\n")
            fdeb=open(filen+"_deb.txt",mode='rb+')
            d=buf[2]
            while(d != -1 ):
                buf=lirebloc(fdeb,d)
                buf_tab=buf[1]
                for j in range(buf_nb):
                    if (buf_tab[j][-1] == '0'):  # pour eliminer les enegestrement suprimer logiquement
                         energtable.append(buf_tab[j]) #recupirer les energ de debordement dans un tableu

                d=buf[2] 
            fdeb.close()
        print('\n\n')   
        
    f.close()
    sorted_table = sorted(energtable, key=lambda x: int(x[:tmat].replace('#', '')))


    j = 0 
    i = 0 
    n = 0 
    fn_deb= filen + "_organiser_deb.txt"
    fn= filen +"_organiser.txt"
    buf_tab = [etud1]*b
    buf_nb = 0 
    try:
        fo = open(fn, "wb")
        fodeb= open(fn_deb,"wb")
    except:
        print("Creation du fichier est impossible ")
    
    indexprim= []
    for e in sorted_table:
        
        Matricule= e[0:tmat].replace("#",'')
        Matricule=int(Matricule)
        n += 1
        if(j < b): # index sera cree dans le meme temps MC
            index= [Matricule,i,j,'fp'] # fp indique que l'engestrement existe dans le fichier principale
            indexprim.append(index)
            buf_tab[j] = e
            buf_nb += 1 
            j += 1
           
        else: 
            index= [Matricule,i+1,0,'fp'] # fp indique que l'engestrement existe dans le fichier principale
            indexprim.append(index)
            buf=[buf_nb, buf_tab,-1]   
            ecrireBloc(fo, i, buf)
            buf_tab=[etud1] * b 
            buf_nb = 1 
            buf_tab[0] = e
            j = 1
            i += 1 
        
    
    buf=[j,buf_tab,-1]
    ecrireBloc(fo, i, buf) 
    affecter_entete(fo, 1, i+1)
    fo.close()
    fodeb.close()

    return indexprim


def requette_intervall(fn, bi ,bs ,index):
    result = []

    for i in range(0, len(index)):
        if(index[i][0] >= bi and index[i][0] <= bs):
            result.append(index[i])

   
    flen=fn+'_deb.txt'
    fn=fn+".txt"
   
    print(result)
    for x in result:
        if(x[-1]=='fp'):
            f = open(fn,'rb')
            i=x[1]
            j=x[2]
            buf = lirebloc(f,i)
                
            buf_tab = buf[1]
            if (buf_tab[j][-1] != '1'): 
                print(afficher_enreg(buf_tab[j] +'\n')) 
            f.close()
        elif (x[-1]=='fd'):
            f = open(flen,'rb')
            i=x[1]
            j=x[2]
            buf = lirebloc(f,i)
            buf_tab = buf[1]
            if (buf_tab[j][-1] != '1'): 
                print(afficher_enreg(buf_tab[j] +'\n'))
            f.close()
        
   


    
c=True
x=0
while (c):
    x=x+1
    print(x)

global index


index=[]
while(c):
    input("taper qlq chose por aficher le menu : \n")
    print("\nMenu: \n")
    print("0. quiter la boucle")
    print("1. crier le fichier")
    print("2. aficher le contenue sans la zone de debordement")
    print("3. aficher le contenue avec la zone de debordement")
    print("4. inserer un element")
    print("5. cree table index")
    print("6. supression Logique d'un element")
    print("7. recherche dans l index")
    print("8. aficher la table d'index")
    print("9. Reorganiser le fichie ")
    print("10 . requette intervalle [A,B]\n")


    ch = input("\n entrez votre choix (0-10): ")

    if(ch=='0'):
        c=False
        print("vous avez exiter le programme")
        break
    elif ch == '1':
        file_name = input("entrez le nom de fichier : ")
        index=Chargement_initial(file_name)
        print(index)
    elif ch == '2':
       
        afficher_fichier()
    elif ch == '3':
    
        afficher_fichier_deb()
    elif ch == '4':
        file_name = input("entrez le nom de fichier : ")
        index=creeindex(file_name)
        index=insertion(file_name,index)
    elif ch == '5':
        file_name = input("entrez le nom de fichier : ")
        index=creeindex(file_name)
        print("\n table d'index : \n")
        for item in index:
            print(item)
        print('\n')
    elif ch == '6':
        file_name = input("entrez le nom de fichier : ")
        v = input("Donner le nombre qui vous voulze suprimez : \n")
        index=creeindex(file_name)
        suppression_Logique(file_name,v,index)

    elif ch == '7':  
        v=input("entrez v : ")
        v=int(v)
        fn=input( "donnez le nom de fichier f :")
        index=creeindex(fn)
        recherche(index,v,fn)
    elif ch == '8':
        if(index==[]):
            print(("la table d index est vide utliser l'outile numero 5"))
        else:
            for item in index:
                print(item)

    elif ch=='9':
        fn=input( "donnez le nom de fichier f :")
        index = Reorganisation(fn)
    
    elif ch=='10':
        fn=input( "donnez le nom de fichier f :")
        l= input("\n donner la valleur petite :  ")
        h = input("\n donner la valler grand :  ")
        l=int(l)
        h=int(h)
        R = requette_intervall(fn,l,h,index)
        print(R)

    else:
        print("cette choix n'existe pas")
