import datetime
import os
import random
import string
from colorama import Fore

def print_ascii_art():
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

# ─────────────────────────────
# Timestamp formatado
# ─────────────────────────────
def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ─────────────────────────────
# Gerador de string aleatória
# ─────────────────────────────
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ─────────────────────────────
# Verificador de admin no Windows
# ─────────────────────────────
def is_admin():
    try:
        return os.getuid() == 0  # Linux
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # Windows

# ─────────────────────────────
# Logger de comandos executados
# ─────────────────────────────
def log_command(bot_id, cmd, response):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"bot_{bot_id}.log")

    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = get_timestamp()
        f.write(f"[{timestamp}] CMD: {cmd}\n")
        f.write(f"[{timestamp}] RES: {response}\n\n")
