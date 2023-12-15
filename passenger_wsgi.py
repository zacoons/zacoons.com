import sys, os
INTERP = os.path.join(os.environ["HOME"], "zacoons.com", "venv", "bin", "python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from server import app as application
if __name__ == "__main__":
    application.run(debug=False)