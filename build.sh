CWD=$(pwd)


# build linux executeable
pyinstaller --onefile pyPath/gui.py

WINEPREFIX=$CWD/_wineprefix
export WINEPREFIX="$WINEPREFIX"
# create the wineprefix if it is not
if [ ! -d "$WINEPREFIX" ]; then
    mkdir -p "$WINEPREFIX"
fi

# get python for wineprefix
wget -nc https://www.python.org/ftp/python/3.8.9/python-3.8.9.exe -O $WINEPREFIX/python-3.8.9.exe
# install python into the prefix
wine $WINEPREFIX/python-3.8.9.exe /passive PrependPath=1
# run windows build script
wine $CWD/build.bat

cp $CWD/_wineprefix/drive_c/dist/gui.exe $CWD/dist/gui.exe