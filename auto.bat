if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "D:\your\bat\location" && exit
... script logic here ...
set exDir="D:\folder\of\project\location"
set exFile="memberblog.py"
set root="D:\folder\of\Anaconda"
call %root%\Scripts\activate.bat %root%
cd /d %exDir%
python %exFile%
pause

