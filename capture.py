import sys
from multiprocessing import Process
import time
import subprocess
import getpass
import os
import signal

if __name__ == "__main__":
  if len(sys.argv) is not 6:
    print('Run: python capture.py [network interface] [label]     [target domain]         [iterations] [timeout (sec)]')
    print('i.e: python capture.py wlo1                duckduckgo  https://duckduckgo.com  5            5')
    exit(0)
  interface = sys.argv[1]
  label = sys.argv[2]
  target = sys.argv[3]
  i, j= 0, int(sys.argv[4])
  timeout = int(sys.argv[5])

  print('starting capture process:')
  print(f'    interface: {interface}')
  print(f'    label: {label}')
  print(f'    target: {target}')
  print(f'    pcap count: {j}')
  print(f'    timeout: {timeout}')

  while i < j:
    i += 1
    print(f'\nPacket {i}')

    #### Capture
    print(f'started capture process')
    capture_process = subprocess.Popen(
                        ['./pcaps/capture.sh', interface, label],
                        preexec_fn=os.setsid,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                      )
    capture_process_pid = capture_process.pid

    #### lynx
    print(f'started lynx process')
    lynx_process = subprocess.Popen(
                      ['lynx', target],
                      preexec_fn=os.setsid,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.STDOUT
                    )
    lynx_process_pid = lynx_process.pid

    #### Wait till lynx finishes loading
    time.sleep(timeout)
    
    #### Kill capture
    os.system('sudo kill -9 %s' % (capture_process_pid))
    os.killpg(os.getpgid(capture_process_pid), signal.SIGTERM)
    print('capture killed')

    #### Kill lynx
    os.system('sudo kill -9 %s' % (lynx_process_pid))
    os.killpg(os.getpgid(lynx_process_pid), signal.SIGTERM)
    print('lynx killed')

  #### Give user permission to read/write the generated pcap files
  os.chmod('pcaps/%s' % (label), 0o777)
