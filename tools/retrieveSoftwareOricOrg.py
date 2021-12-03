# http://api.oric.org/0.2/softwares/

import json
import pycurl
import zipfile
import os, sys
from io import BytesIO 
import pathlib
import re


from shutil import copyfile

version_bin="0"
destroot="../build/"
dest="../build/usr/share/basic11/"

destftdos="../build/usr/share/ftdos/"
destsedoric="../build/usr/share/sedoric/"
destroms="../build/usr/share/roms/"
destdloppybuilder="../build/usr/share/fbuilder/"
destmym="../build/usr/share/mym/"
desthrs="../build/usr/share/hrs/"
destpt3="../build/usr/share/pt3/"
destosid="../build/usr/share/osid/"

basic_main_db="basic11.db"
basic_main_db_indexed="basic11i.db"

basic_games_db="games.db"
basic_demos_db="demos.db"
basic_utils_db="utils.db"
basic_unsorted_db="unsorted.db"

destetc="../build/var/cache/basic11/"
destlauncher="../build/var/cache/launcher/"
destetcftdos="../build/var/cache/ftdos/"
destetcsedoric="../build/var/cache/sedoric/"

tmpfolderRetrieveSoftware="build/"
list_file_for_md2hlp=""

def buildDbFileSoftwareSingle(destetc,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    f = open(destetc+"/"+letter+"/"+filenametap8bytesLength+".db", "wb")
    f.write(DecimalToBinary(version_bin))
    f.write(DecimalToBinary(rombasic11))
    f.write(KeyboardMatrix(fire2_joy))
    f.write(KeyboardMatrix(fire3_joy))            
    f.write(KeyboardMatrix(down_joy))
    f.write(KeyboardMatrix(right_joy))
    f.write(KeyboardMatrix(left_joy))
    f.write(KeyboardMatrix(fire1_joy))
    f.write(KeyboardMatrix(up_joy))

    f.write(DecimalToBinary(len(name_software)))
    name_software_bin=bytearray(removeFrenchChars(name_software),'ascii')
    name_software_bin.append(0x00)
    f.write(name_software_bin)
    f.close()



def removeFrenchChars(mystr):

    mystr=mystr.replace("Ã©", "e")
    mystr=mystr.replace("é", "e")
    mystr=mystr.replace("è", "e")
    mystr=mystr.replace("ê", "e")
    mystr=mystr.replace("ë", "e")
    mystr=mystr.replace("ç", "c")
    mystr=mystr.replace("°", " ")

    mystr=mystr.replace("à", "a")
    mystr=mystr.replace("â", "a")

    mystr=mystr.replace("ô", "o")
    mystr=mystr.replace("ï", "i")
    mystr=mystr.replace("î", "i")
    mystr=mystr.replace("©", "")
    mystr=mystr.replace("Ã", "e")
    mystr=mystr.replace(u'\xa0', u'a')
    
    
    return mystr


def buildMdFile(filenametap8bytesLength,dest,letter,name_software,date_software,download_platform_software,programmer_software,junk_software):
    md_software="# "+removeFrenchChars(name_software)+"\n"
    #md_software=md_software+"Type : "+download_platform_software+"\n"
    tdate_software=date_software.split('-')
    year=tdate_software[0]
    md_software=md_software+"Release Date : "+year+"\n"
    md_software=md_software+"Platform : "
    match = re.search('A', download_platform_software)
    doslash="no"
    if match:
        md_software=md_software+"Atmos"
        doslash="yes"
    match = re.search('O', download_platform_software)
    if match:
        if doslash=="yes":
            md_software=md_software+"/"
        md_software=md_software+"Oric-1"
        doslash="no"                

    md_software=md_software+"\n"
            
    md_software=md_software+"Programmer : "+removeFrenchChars(programmer_software)+"\n"
    #md_software=md_software+"Origin : "+programmer_software+"\n"
    md_software=md_software+"Informations : "+removeFrenchChars(junk_software)+"\n"
            
    print(md_software)
            
    md=filenametap8bytesLength+".md"
    file_md_path=dest+"/"+letter+"/"+md
    f = open(file_md_path, "wb")
    md_software = re.sub(u"\u2013", "-", md_software)
    md_software = re.sub(u"\u2019", "'", md_software)
    
    #md_software = md_software.decode('utf-8')
    #md_software = md_software.replace("\u2013", "-") #en dash
    md_bin=bytearray(md_software,'ascii')
    f.write(md_bin)
    f.close()


def DecimalToBinary(num):
    return int(num).to_bytes(1, byteorder='little')

def CreateTargetFolder(dest,destetc,letter):
    folder=dest+'/'+letter
    folderdb=destetc+'/'+letter
    #print(folder)
    directory = os.path.dirname(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("######################## Create "+folder)
    if not os.path.exists(folderdb):
        os.mkdir(folderdb)
        print("######################## Create "+folderdb)

def KeyboardMatrix(num):
    keyboardMatrixTab=[
           #                                        LeftRight
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,172 ,188 , #0..9
           #          RET 
            180 ,156 ,175 ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #10..19
           #                                   ESC 
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,169 ,0   ,0   , #20..29
           #          ESP
            0   ,0   ,132 ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #30..39
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #40..49
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #50..59
           #                         A    B    C    D    E
            140 ,0   ,148   ,0   ,0   ,174 ,146 ,186 ,185 ,158  , #60..69
           #F    G    H    I    J    K    L    M    N    O
            153 ,150 ,142 ,141 ,129 ,131 ,143 ,130 ,136 ,149  , #70..79
           #P    Q    R    S     T    U    V    W    X    Y 
            157 ,177 ,145 ,182 ,137 ,133 ,152 ,180 ,176 ,134 , #80..89
           #Z 
            170 ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    , #90..99

            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #100..109
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #110..119
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #120..129
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #130..139
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #140..149
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #150..159
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #160..169
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #170..179
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #180..189
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #190..199


            ] 
    key=keyboardMatrixTab[int(num)]
    return DecimalToBinary(key)


exist_ok=True
if not os.path.exists(dest):
    pathlib.Path(dest).mkdir(parents=True)
if not os.path.exists(destetc):
    pathlib.Path(destetc).mkdir(parents=True)    

# Launcher
if not os.path.exists(destlauncher):
    pathlib.Path(destlauncher).mkdir(parents=True)        



# ftdos    
if not os.path.exists(destftdos):
    pathlib.Path(destftdos).mkdir(parents=True)
if not os.path.exists(destetcftdos):
    pathlib.Path(destetcftdos).mkdir(parents=True)    

# sedoric
if not os.path.exists(destsedoric):
    pathlib.Path(destsedoric).mkdir(parents=True)
if not os.path.exists(destetcsedoric):
    pathlib.Path(destetcsedoric).mkdir(parents=True)        

if not os.path.exists(tmpfolderRetrieveSoftware):
    pathlib.Path(tmpfolderRetrieveSoftware).mkdir(parents=True)    

print("Retrieve json file from oric.org ...")
b_obj = BytesIO() 
crl = pycurl.Curl() 

# Set URL value
crl.setopt(crl.URL, 'http://api.oric.org/0.2/softwares/?sorts=name_software')

# Write bytes that are utf-8 encoded
crl.setopt(crl.WRITEDATA, b_obj)

# Perform a file transfer 
crl.perform() 

# End curl session
crl.close()

# Get the content stored in the BytesIO object (in byte characters) 
get_body = b_obj.getvalue()

# Decode the bytes stored in get_body to HTML and print the result 
#print('Output of GET request:\n%s' % get_body.decode('utf8')) 

datastore = json.loads(get_body.decode('utf8'))


basic_main_db_str=""
game_db_str=""
demos_db_str=""
utils_db_str=""
unsorted_db_str=""

count=0
#                       low, high
main_db_table_software=[1,0]
lenAddSoftware=0

for i in range(len(datastore)):
    
    #Use the new datastore datastructure
    id_software=datastore[i]["id"]
    tapefile=datastore[i]["download_software"]
    name_software=datastore[i]["name_software"]
    programmer_software=datastore[i]["programmer_software"]
    download_platform_software=datastore[i]["platform_software"]
    category_software=datastore[i]["category_software"]
    junk_software=datastore[i]["junk_software"]
    date_software=datastore[i]["date_software"]
    name_software=name_software.replace("é", "e")
    name_software=name_software.replace("è", "e")
    name_software=name_software.replace("ç", "c")
    name_software=name_software.replace("°", " ")
    name_software=name_software.replace("à", "a")
    name_software=name_software.replace("â", "o")
    joystick_management_state=datastore[i]["joystick_management_state"]
    junk_software=removeFrenchChars(junk_software)

    

    programmer_software=programmer_software.replace("é", "e")
    programmer_software=programmer_software.replace("è", "e")
    programmer_software=programmer_software.replace("ç", "c")
    programmer_software=programmer_software.replace("°", " ")
    programmer_software=programmer_software.replace("à", "a")
    programmer_software=programmer_software.replace("ô", "o")


    rombasic11=datastore[i]["basic11_ROM_TWILIGHTE"]
    up_joy=datastore[i]["up_joy"]
    down_joy=datastore[i]["down_joy"]
    right_joy=datastore[i]["right_joy"]
    left_joy=datastore[i]["left_joy"]
    fire1_joy=datastore[i]["fire1_joy"]
    fire2_joy=datastore[i]["fire2_joy"]
    fire3_joy=0
    #print(datastore[i])
    #print(tapefile)
    if tapefile!="":
        b_obj_tape = BytesIO() 
        crl_tape = pycurl.Curl() 

        # Set URL value
        crl_tape.setopt(crl_tape.URL, 'https://cdn.oric.org/games/software/'+tapefile)
        crl_tape.setopt(crl_tape.SSL_VERIFYHOST, 0)
        crl_tape.setopt(crl_tape.SSL_VERIFYPEER, 0)
        # Write bytes that are utf-8 encoded
        crl_tape.setopt(crl_tape.WRITEDATA, b_obj_tape)

        # Perform a file transfer 
        crl_tape.perform() 

        # End curl session
        crl_tape.close()

        # Get the content stored in the BytesIO object (in byte characters) 
        get_body_tape = b_obj_tape.getvalue()

        # Decode the bytes stored in get_body to HTML and print the result 
        #print('Output of GET request:\n%s' % get_body.decode('utf8')) 

        extension=tapefile[-3:].lower()


        head, tail = os.path.split(tapefile)

        f = open(tmpfolderRetrieveSoftware+"/"+tail, "wb")
        f.write(get_body_tape)
        f.close()
        #tail=tail.lower()
        letter=tail[0:1].lower()


        CreateTargetFolder(dest,destetc,letter)
        
        

        filenametap=tail.lower().replace(" ", "").replace("-", "").replace("_", "")
            
        tcnf=filenametap.split('.')
        print("Generating : "+name_software+"/"+id_software)
        filenametapext=tcnf[1]
        cnf=tcnf[0]+".db"
        filenametapbase=tcnf[0]
        filenametap8bytesLength=filenametapbase[0:8]
        
        print("Filenametap : "+filenametap+" tail : "+tail+" tape file : "+tapefile)

        if extension=="dsk":
            match = re.search('J', download_platform_software)
            print("download_platform_software"+download_platform_software)
            if match:
                # Jasmin
                CreateTargetFolder(destftdos,destetcftdos,letter)
                print ('# jasmin/ftdos dsk file')
                copyfile(tmpfolderRetrieveSoftware+tail,destftdos+"/"+letter+"/"+filenametap8bytesLength+".dsk" )
                if not os.path.exists(destetcftdos+"/"+letter):
                    os.mkdir(destetcftdos+"/"+letter)
                buildMdFile(filenametap8bytesLength,destftdos,letter,name_software,date_software,download_platform_software,programmer_software,junk_software)
                buildDbFileSoftwareSingle(destetcftdos,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
            match = re.search('S', download_platform_software)
            if match:
                # Sedoric
                print ('# Sedoric dsk file')
                CreateTargetFolder(destsedoric,destetcsedoric,letter)
                copyfile(tmpfolderRetrieveSoftware+tail,destsedoric+"/"+letter+"/"+filenametap8bytesLength+".dsk" )
                if not os.path.exists(destetcsedoric+"/"+letter):
                    os.mkdir(destetcsedoric+"/"+letter)
                buildMdFile(filenametap8bytesLength,destsedoric,letter,name_software,date_software,download_platform_software,programmer_software,junk_software)
                buildDbFileSoftwareSingle(destetcsedoric,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)                

        if extension=="zip":
            print("# zip (Skipping) id_software :"+id_software)
            
            #with zipfile.ZipFile(tmpfolderRetrieveSoftware+tail, 'r') as zip_ref:
            #    zip_ref.extractall(dest+"/"+rombasic11+"/"+letter+"")
        if extension=="tap":
            print("# tape")
            #if rombasic11=="0" or rombasic11=="1" rombasic11=="0":
            #print("Copy : "+tmpfolderRetrieveSoftware+tail,dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext)
            copyfile(tmpfolderRetrieveSoftware+tail,dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext )
            
            #Hobbit ROM we copy also the tape file at the root of the sdcard
            if rombasic11=="0":
                copyfile(tmpfolderRetrieveSoftware+tail,destroot+"/"+filenametap8bytesLength+"."+filenametapext )
            if rombasic11!="0" and rombasic11!="1" and rombasic11!="2":    
                rombasic11=1
            if not os.path.exists(destetc+"/"+letter):
                os.mkdir(destetc+"/"+letter)
            buildMdFile(filenametap8bytesLength,dest,letter,name_software,date_software,download_platform_software,programmer_software,junk_software)
            buildDbFileSoftwareSingle(destetc,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)


            count=count+1

            # main db
           
            addSoftware=filenametap8bytesLength.upper()+';'+removeFrenchChars(name_software)+'\0'
            basic_main_db_str=basic_main_db_str+addSoftware
            lenAddSoftware+=len(addSoftware)
            main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
            addSoftwareLauncher=filenametap8bytesLength.upper()+';'+name_software+';'+download_platform_software+'\0'
            if category_software=="1":
                game_db_str=game_db_str+addSoftwareLauncher
            if category_software=="6":
                demos_db_str=demos_db_str+addSoftwareLauncher          
            if category_software=="2":
                utils_db_str=utils_db_str+addSoftwareLauncher
                # For debug
                print("Debug : "+addSoftwareLauncher)
            if category_software=="7":
                unsorted_db_str=unsorted_db_str+addSoftwareLauncher

EOF=0xFF            
print("Write basic11 db")
f = open(destetc+"/"+basic_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

#print(main_db_table_software)
# indexed
f = open(destetc+"/"+basic_main_db_indexed, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_games_db")
f = open(destlauncher+"/"+basic_games_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(game_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_demos_db")
f = open(destlauncher+"/"+basic_demos_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(demos_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_utils_db")
f = open(destlauncher+"/"+basic_utils_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(utils_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_unsorted_db")
f = open(destlauncher+"/"+basic_unsorted_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(unsorted_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()


#basic_utils_db="utils.db"
#basic_unsorted_db="unsorted.db"

