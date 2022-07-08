start "" python UploadDownload.py 2

set loopcount=1
:loop
start "" python launchTabs2MHs.py https://hub.metaust.link/f9Fsp7W/luminous-usable-outing
set /a loopcount=loopcount-1
if %loopcount%==0 goto exitloop
goto loop
:exitloop

