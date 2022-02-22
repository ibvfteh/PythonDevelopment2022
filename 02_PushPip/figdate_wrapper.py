import venv
from tempfile import mkdtemp
from shutil import rmtree
import subprocess
from os.path import join

tmp_dir = mkdtemp()
venv.create(tmp_dir, with_pip=True)

pip_path = join(tmp_dir, "bin", "pip")
subprocess.run([pip_path, "install", "pyfiglet"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

python_path = join(tmp_dir, "bin", "python")
subprocess.run([python_path, "-m", "figdate"])

rmtree(tmp_dir)
