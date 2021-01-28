cd ..
cd build
cd telemetry-files

echo "Telservice build..."
python -m nuitka --follow-imports ../../python-files/listener/telservice.py
echo " "

echo "rmodule build..."
python -m nuitka --follow-imports ../../python-files/rmmodules/rmodule/rmodule.py
echo " "

echo "mmodule build..."
python -m nuitka --follow-imports ../../python-files/rmmodules/mmodule/mmodule.py
echo " "

echo "Launch manager build..."
python -m nuitka --follow-imports ../../python-files/launchers/launch-manager.py
echo " "

echo "Config generator build..."
python -m nuitka --follow-imports ../../python-files/launchers/config-generator.py
echo " "

cd ..
cd startup

echo "Startup build..."
python -m nuitka --follow-imports ../../python-files/startup/telstartup.py
echo " "

cd ..

echo "Installer build..."
python -m nuitka --follow-imports ../python-files/installer/installer.py
echo " "

echo "Done."