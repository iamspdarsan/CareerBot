import os
import shutil
import sys
import modules as core


username=os.getenv("USERNAME")
des=f'C:\\Users\\{username}\\CareerBot'
bat=f'C:\\Users\\{username}\\Desktop\\CareerBot.bat'
daemon=des+'\\daemon.bat'

#initiating file for logs
try:
    with open('log.txt','r'):pass
except:
    with open('log.txt','w'):pass


#installation
def install():
    print("Installation process started")
    src=os.getcwd()
    shutil.copytree(src,des)
    #creating shortcut on desktop
    with open(bat,'w')as file:
        file.writelines(f'cd {des}\npython "{des}\\main.py"')
    print("Desktop shortcut created")
    input(f"CareerBot is installed at {des}")
    sys.exit()


def uninstall():
    print("Uninstall process started")
    shutil.rmtree(des)
    os.system(f'del C:\\Users\\{username}\\Desktop\\CareerBot.bat')
    input("Uninstalled successfully\npress enter to close")
    sys.exit()


def getinput():
    os.system('cls')
    print("##########################################\n")
    opt=int(input(
        "What to do?\n"+
        "1.Login\n"+
        "2.Set job filter\n"+
        "3.Schedule CareerBot\n"+
        "4.Delete CareerBot schedule\n"+
        "5.Uninstall\n"+
        "6.Exit\n"+
        "\n##########################################\n"+
        "Input: "))
    return opt


def installation_check():
    if not os.path.isdir(des) or len(os.listdir(des))==0:
        #installation prompt
        if os.path.isdir(des):
            shutil.rmtree(des)
        input("Let start with installation\npress enter to continue")
        install()
    else:
        if des != os.getcwd():
            print(f"Already installed in {des}\n open desktop shortcut to use")
            sys.exit()


def delete_schedule():
    cmd='schtasks /delete /tn "CareerBot" /f'
    os.system(cmd)
    input("press enter to back to main menu")
    start_cli()


def start_cli():
    try:
        inp=getinput()
    except:
        print("Number input only")
        inp=getinput()

    if inp == 1:
        while 1:
            email=input("Enter your email: ")
            password=input("Enter your password: ")
            prompt=input(f"Verify your credential\nemail: {email}\npassword: {password}\nCan we proceed? Y or N\n")
            if prompt.lower() == 'y':
                core.login(email,password)
            start_cli()
            
    elif inp == 2:
        core.setjoburl()
        input("press enter to back to main menu")
        start_cli()

    elif inp == 3:
        while 1:
            time=input("Set time for CareerBot execution: ( HOURS-MINUTES ) 24H format\n")
            if "-" not in time:
                print("Wrong input\nExample(HH-MM): 24-59")
                continue
            hh=time[:time.find("-")]
            mm=time[time.find("-")+1::]
            command=f'schtasks /create /sc daily /tn "CareerBot" /tr "{daemon}" /st {hh}:{mm}'
            #print(command)
            os.system(command)
            input("press enter to back to main menu")
            start_cli()

    elif inp == 4:
        delete_schedule()


    elif inp == 5:
        uninstall()
    
    elif inp == 6:
        sys.exit()
    

installation_check()
start_cli()