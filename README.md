# APP---EX
sistema automatizado para la creacion de oportunidad de un cliente en la tipifiaccion para la empresa CLARO


PARA SU GENERACIONES USAR EN CONSOLA:

pyinstaller --noconsole --onedir --icon=nick.ico --add-data "config.json;." --add-data "nick.png;." --add-data "chromedriver.exe;." --collect-all selenium main.py