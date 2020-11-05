# CofC-Auto-Registration

Hey! My name is Ethan, and I am (as of the time of writing this) a student at the College of Charleston. Each semester the registration system is opened via MyCharleston to various students on different days, depending on how many credits they have completed at the time of their registration. Registration opens at 8:00am, and I personally don't like to wake up and sit at the computer hoping that I can be the first to register for the classes I really need. With that in mind, I decided that it should be possible to create a script that registers for me using Python. Well, that is this script! Best of all, you don't have to spend painstaking hours trying to get it to work (hopefully) because I already did that for you! That, said there are still some things you have to do to run this script which I will outline below. Other than that, enjoy! Oh, and if you like this project, why don't you leave it a star on GitHub? That would make me happy. You want me to be happy, right?

## Instructions

### Disclaimer

This script is intended to run on MacOS or Linux, but not necessarily Windows. While I will provide some tips about what I \*think\* will work for Windows users, I cannot guaruntee compatibility. So, if you find a problem with this script on Windows, go ahead and [open up an issue](https://github.com/EGuthrieWasTaken/CofC-Auto-Registration/issues) so I can look into it.

As for MacOS users, you may notice that your Python3 environment does not work as expected if you installed Python using Homebrew. In my opinion Homebrew installations of Python should be avoided if at all possible, but if you already have it there I suggest installing Python again from Python.org and then calling this fresh installation of Python explicitly (i.e. ``/usr/bin/python3`` or ``/usr/bin/pip3`` rather than simply ``python3`` or ``pip3``, respectively). Beyond this advice, **I will not support any issues involving running this script with the Homebrew installation of Python.**

And finally, Linux users. You guys should have a pretty easy time running this script, as the Python installation from any of the major package managers works just fine. Beyond that, you may hate Google Chrome (and I can't blame you for that), but unfortunately you will have to either get over it, or you're welcome to edit the code you pull to explicitly use a different browser. Again, however, **I will not support any issues resulting from making changes to the most up-to-date script available on this repository.**

### Requirements

1) A version of [Python3](https://python.org/downloads/) with Pip. All versions of Python3 3.4 or newer should have this tool already. Otherwise, you can download/install Pip by following [this tutorial from PyPi](https://pip.pypa.io/en/stable/installing/). After this, you must install the Selenium module for Python3 using Pip. Regardless of your operating system, this can be accomplished by runnign the following command:

```bash
pip3 install selenium
```

2) A recent version of [Google Chrome](https://www.google.com/chrome/). Any version of Chrome for which a ChromeDriver is available should work (see requirement #2), but older issues may have unforeseen problems.
3) The corresponding version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) to your version of Chrome. You can find your Chrome version by selecting the 3 dots icon on the top right of the browser, and then selecting Help -> About Google Chrome. The full version number is listed there, but you only need the first number (ex: 86.X.X.X). For version 86 of Chrome, you would want version 86 of ChromeDriver, and so on.
4) It isn't enough to simply download ChromeDriver; you have to place it in your ``PATH``. For Linux and MacOS, this can generally be accomplished by running the following command:  
**Important Note**: Make sure the file named ``chromedriver`` is in your current user's ``Downloads`` directory before using either of the below commands. Otherwise the commands will fail.

```bash
sudo mv ~/Downloads/chromedriver /usr/local/bin/
```

As for Windows, you may have some luck with the following command:

```batch
move %HOMEPATH%\Downloads\chromedriver C:\WINDOWS\system32
```

At this point, you should be all set to run the script with the following command from the directory of this project:

```bash
python3 autoRegister.py -e [arguments]
```

You can always simply run the above command with ``-h`` as the only argument to disply usage instructions. However, simply running the script without any arguments will cause the program to run in interactive mode, wherein it will prompt you for all necessary information. I also recommend using the ``-e`` option, which causes the program to run headless (i.e. it doesn't open a new window for Chrome), and this usually helps with program stability. For those with little knowledge of using tools such as this, this is recommended.
