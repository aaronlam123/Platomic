import os
import subprocess
import webbrowser


if __name__ == '__main__':
    subprocess.call(['coverage', 'erase'])
    subprocess.call(['coverage', 'run', '--branch', '--module', 'unittest', 'discover', '-s', '.', '-p', '*_test.py'])
    subprocess.call(['coverage', 'html'])
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(
        "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open("file://" + os.getcwd() + "/htmlcov/index.html", new=2)
