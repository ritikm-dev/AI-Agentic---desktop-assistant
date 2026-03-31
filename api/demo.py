 # file_open =["my files","files","file manager","this pc","local disk","recycle bin","desktop files","file explorer","file"]
    # words = re.findall(r'\b\w+\b',user_input.lower())
    # if any(word in words for word in file_open):
    #         print("Opening File Manager")
    #         subprocess.run("explorer",creationflags=subprocess.CREATE_NO_WINDOW)
    #         return "File Manager opened successfully"
    # elif "turn on wifi and connect to network" in user_input.lower():
    #         cmd='netsh interface set interface "Wi-Fi" enable'
    #         subprocess.run(cmd,shell=True)
    #         print("connecting.....  🚀")
    #         s=input("Which Network ?  🤔..")
    #         subprocess.run(f'netsh wlan connect name={s}',shell=True)
    #         return f"Connected to {s} network"
    # elif "turn off wi-fi" in user_input.lower() or "turn off wifi" in user_input.lower():
    #         print("Turning Off Wifi... 😇")
    #         cmd='netsh interface set interface "Wi-Fi" disable'
    #         run = subprocess.run(cmd,capture_output=True,text=True,shell=True)
    #         print(run.stdout)
    #         return "WiFi turned off" 
    # elif "turn on wifi" in user_input.lower() or "turn on wi-fi" in user_input.lower():
    #         print("Turning On Wifi  😇")
    #         cmd='netsh interface set interface "Wi-Fi" enable'
    #         subprocess.run(cmd,capture_output=True,text=True,shell=True)
    #         return "WiFi turned on"
    # elif "shutdown system" in user_input or "shut down system" in user_input.lower() or "shutdown" in user_input.lower():
    #         subprocess.run(["shutdown","/s","/t","30"])
    #         return "System will shutdown in 30 seconds"
    # elif "restart system" in user_input:
    #         subprocess.run(["shutdown","/r","/t","30"])
    #         return "System will restart in 30 seconds"
    # else: