## Text menu in Python 
# 
# v0.2
# Started:          6/12/2017
# Last Modified:    6/14
#
# Description:  command-line menu front-end for the Ethera eGX-1000 system
#
import os,platform
import time

#pip install readchar
import readchar as rch
    
  

def get_main_menu_choice(bLoop=True):  
    while bLoop:          ## While loop which will keep going until loop = False
        ## Displays menu
        print 15 * "-" , "eGX-1000 Stimulation System Menu" , 15 * "-"
        print "1. System Configuration"
        print "2. Configure EC Stim Units"
        print "3. Configure MC Stim Units"
        print "4. System Status & Monitoring"
        print "5. Exit"
        print 37 * "-"
        choice = input("Enter your choice [1-5]: ")
         
        if choice==1:     
            print "SYSTEM CONFIGURATION"
            
        elif choice==2:
            print "EC STIM UNIT CONFIGURATION"
            # Select Protocol --> Protocol Modes (if applicable) --> Channel [1-4] --> Addresses (TBD) --> Start
            stim_menu_selection__protocol(stim_type="EC")
            
        elif choice==3:
            print "MC STIM UNIT CONFIGURATION"
            # Select Protocol --> Protocol Modes (if applicable) --> Channel [1-4] --> Addresses (TBD) --> Start
            stim_menu_selection__protocol(stim_type="MC")
            
        elif choice==4:
            print "SYSTEM STATUS & MONITORING"
            
        elif choice==5:
            clear_screen()
            print "EXITING..."
            # Make sure that any transient states are saved.
            bLoop=False # This will make the while loop to end as not value of loop is set to False
            
        else:
            # Any integer inputs other than values 1-5 we print an error message
            raw_input("Wrong option selection. Enter any key to try again..")

# 2nd Menu Stage 
# next stage --> channel            
def stim_menu_selection__protocol(stim_type="EC"):
    bLoop_protocol=True
    while bLoop_protocol:
    
        print 15 * "-" , " Select Protocol for " + stim_type + "units:", 15 * "-"
        # 
        # [ ] Add routine to read from protocol database, showing the
        #     protocol name & description in a max 20-item list.  The # 
        #     corresponds to a protocol_ID that's stored.
        # [ ] Filter to only show protocols of compatibility: "stim_type" or "both"
        #
        
        # Loop     
        print "1. Test Protocol 1"
        print "2. Test Protocol 2"
        print "3. Return to previous menu"
        print 40 * "-"
    
        choice = input("Enter your choice [1-3]: ")
         
        if choice==1:     
            print "Test Protocol 1 selected"
            bLoop_protocol=False
            get_choice__EC_stim_menu__channel(iProtocol=1, stim_type)
            
        elif choice==2:
            print "Test Protocol 2 selected"
            bLoop_protocol=False
            get_choice__EC_stim_menu__channel(iProtocol=2, stim_type)
            
        elif choice==3:
            print "Exiting to previous menu..."
            
            clear_screen()
            time.sleep(1)
            bLoop_protocol=False 
            get_main_menu_choice()
            

        else:
            # Any integer inputs other than accepted values, we print an error message
            raw_input("Wrong option selection. Enter any key to try again..")
    
# 3rd Menu Stage 
# next stage --> summary+send    
def get_choice__EC_stim_menu__channel(iProtocol, stim_type):
    bLoop_channel=True
    print "For the stimulation unit of type: " + stim_type + ", "
    print "Selected protocol was " + str(iProtocol)

    while bLoop_channel:
    
        print 15 * "-" , " Apply to channel: " , 15 * "-"
        # Loop
        print "1-4. Channel Number"
        print "5.   Return to previous menu"
        print 40 * "-"
    
        choice = input("Enter your choice [1-5]: ")
        CHANNEL_LIST = [1,2,3,4]
        if choice in CHANNEL_LIST:     
            print "Channel " + str(choice) + " selected"
            bLoop_channel=False
            # Prepare to send...
            stim_menu__pre_send(stim_type, iProtocol, iChannel):
            
        elif choice==5:
            print "Exiting to previous menu..."
            clear_screen()
            time.sleep(1)
            bLoop_protocol=False 
            get_choice__EC_stim_menu__protocol()            
           
        else:
            # Any integer inputs other than accepted values, we print an error message
            raw_input("Wrong option selection. Enter any key to try again..")
            
# 4th Menu Stage 
# next stage --> Verification; Get status
def stim_menu__pre_send(stim_type, iProtocol, iChannel):
    bLoop_pre_send=True
       
    print 15 * "-" , " EC Stimulation Command Summary " , 15 * "-"
    print "Selected protocol was " + str(iProtocol)
    print "\t Protocol description: " + "THIS IS A TEST"
    print "\n"
    print "To be applied to all EC units on channel: " + iChannel + "\n"
    print 40 * "-"
    print "\n"
    print "Send command sequence?  Press [ Y ] to Send or any other key to cancel: "    
    choice = rch.readchar()
    
    if choice in ["Y", "y"]:
        # --> send_stim_command(stim_type, iProtocol, iChannel)
        #       - Needs to send only to units of a given type.
        print "command sequence sent"
        
        # verify_stim_command_channel_all()
        # Verifies all units on the channel are programmed with the desired protocol 
        #   and all associated operating parameters
        # --> verify_stim_command_channel_all(iProtocol,iChannel) 
        print "All units on channel " + iChannel + " have been verified as being properly programmed."
        time.sleep(1)
        
        # Return to main menu
        get_main_menu_choice()
    else:
        print "Send command ABORTED... returning to main menu...
        time.sleep(1)
        get_main_menu_choice()
        
            
# Requires:  os,platform
def clear_screen():
    if platform.system()=="Windows":
        os.system("cls")
    elif platform.system()=="Linux":
        os.system("clear")
    print "\n"

    
get_main_menu_choice()