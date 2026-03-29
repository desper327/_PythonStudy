import subprocess
import os

os.environ["haha"] = "123"

path=os.path.dirname(os.path.abspath(__file__))
subprocess.Popen(["python", f"{path}/b.py"],env={})