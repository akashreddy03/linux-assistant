import subprocess
import os
from langchain_core.tools import tool
import threading

out = ''
@tool
def execute_command(command: str):
    """Run a shell LINUX command to perform a certain os task. It can be used to run processes"""
    
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True
    )

    event = threading.Event()


    global out
    out = ''
    def add_line(line: str):
        global out
        out += line

    def get_output(event, chunk_size):
        while True:
            chunk = process.stdout.read(chunk_size)
            if not chunk or event.is_set():
                break  # End of output
            add_line(chunk)

    t = threading.Thread(target=get_output, args=(event, 50,))
    t.start()
    t.join(timeout=8)

    try: 
        process.wait(timeout=8)
        
        if t.is_alive():
            event.set()
            t.join()

        if process.returncode == 0:
            out = "Command executed successfully: " + out
        else:
            out = "Command failed:" + out + process.stderr.read() 
    
    except subprocess.TimeoutExpired:

        if t.is_alive():
            event.set()
            t.join()

        out = "Process is still running in the background and the command probably succeeded " + out

    return out

if __name__ == '__main__':
    execute_command('google-chrome-stable')
