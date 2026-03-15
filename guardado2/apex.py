#apex.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_bot(usuario, password, textbox):
    """
    Función principal del bot para automatizar la gestión de contactabilidad.
    Args:
        usuario (str): Usuario para login.
        password (str): Contraseña para login.
        textbox (tk.Text): Textbox de Tkinter donde se mostrarán los logs y se pegarán las plantillas.
    """

    # Función auxiliar para mostrar logs en el textbox
    def log(msg):
        textbox.insert("end", msg + "\n")
        textbox.see("end")

    # Configurar opciones de Chrome
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")

    # Iniciar el navegador
    driver = webdriver.Chrome(options=options)
    driver.get(
        "https://gestorcampanas.claro.com.pe/ords/r/ws_usrcampana/gesti%C3%B3n-de-campa%C3%B1as-con-discadores174156/login"
    )

    wait = WebDriverWait(driver, 10)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])

    # =====================
    # LOGIN
    # =====================
    wait.until(EC.element_to_be_clickable((By.ID, "P9999_USERNAME"))).send_keys(usuario)
    wait.until(EC.element_to_be_clickable((By.ID, "P9999_PASSWORD"))).send_keys(password)
    driver.find_element(By.ID, "P9999_PASSWORD").submit()

    # Esperar menú principal
    buscar_cliente = wait.until(EC.element_to_be_clickable((By.ID, "t_MenuNav_1i")))
    buscar_cliente.click()

    log("BOT INICIADO")
    log("Ya puedes pegar tu plantilla y presionar Enter...")

    while True:
        identificador = None
        numero = None

        # =====================
        # ESPERAR PLANTILLA
        # =====================
        while True:
            plantilla = textbox.get("1.0", "end").strip()
            if plantilla:
                break
            time.sleep(0.3)

        lineas = plantilla.split("\n")
        for i, linea in enumerate(lineas):
            if "Identificación" in linea and i + 1 < len(lineas):
                identificador = lineas[i + 1].strip()
            if "Número llamado" in linea and i + 1 < len(lineas):
                numero = lineas[i + 1].strip()

        # Validar plantilla
        if not (identificador and numero and numero.isdigit()):
            log("❌ Plantilla incorrecta. Vuelve a pegarla completa.")
            textbox.delete("1.0", "end")
            continue

        textbox.delete("1.0", "end")
        log(f"Identificador detectado: {identificador}")
        log(f"Número detectado: {numero}")

        # =====================
        # BUSCAR CLIENTE
        # =====================
        select = wait.until(EC.presence_of_element_located((By.ID, "P5_SELECT_TIPO_BUSQUEDA")))
        Select(select).select_by_value("2")

        campo_busqueda = wait.until(EC.element_to_be_clickable((By.ID, "P5_BUSCA")))
        campo_busqueda.clear()
        campo_busqueda.send_keys(numero)

        # Limpiar campo teléfono y hacer clic en buscar
        driver.execute_script("document.getElementById('P5_PHONE').innerText=''")
        driver.find_element(By.ID, "boton").click()

        # =====================
        # ESPERAR RESULTADO
        # =====================
        telefono_encontrado = ""
        log("Esperando resultado de búsqueda...")

        for _ in range(30):
            try:
                resultado = driver.find_element(By.ID, "P5_PHONE")
                telefono_encontrado = resultado.text.strip()
                if telefono_encontrado == numero:
                    log("Número verificado correctamente")
                    break
            except:
                pass
            time.sleep(0.5)

        log(f"Teléfono encontrado: {telefono_encontrado}")
        if telefono_encontrado != numero:
            log("ERROR: El número encontrado no coincide con la búsqueda.")
            continue

        log("PROCEDIENDO CON CREACION DE CONTACTABILIDAD")

        # =====================
        # NUMERO ORIGEN
        # =====================
        campo_origen = wait.until(EC.element_to_be_clickable((By.ID, "P5_NUMERO_ORIGEN_LLAMADA")))
        campo_origen.clear()
        campo_origen.send_keys(numero)

        # =====================
        # SERIAL
        # =====================
        base_serial = identificador[:15]
        campo_serial = wait.until(EC.element_to_be_clickable((By.ID, "P5_SERIAL_NUMBER")))
        boton_guardar = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[text()='Guardar Contactabilidad']/..")
        ))

        serial_valido = None
        for i in range(10):
            serial_prueba = base_serial + str(i)
            campo_serial.clear()
            campo_serial.send_keys(serial_prueba)
            time.sleep(1)
            if boton_guardar.is_enabled():
                serial_valido = serial_prueba
                log(f"Serial válido: {serial_valido}")
                break

        if serial_valido is None:
            log("No se pudo generar serial válido.")
            continue

        # =====================
        # GUARDAR CONTACTABILIDAD
        # =====================
        boton_guardar.click()
        confirmar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'js-confirmBtn')]")
        ))
        confirmar.click()
        time.sleep(2)
        log("CONTACTABILIDAD GUARDADA")

        # =====================
        # BOTON FINAL
        # =====================
        log("Esperando habilitación de oportunidad...")
        boton_final = wait.until(EC.element_to_be_clickable((By.ID, "btn-genera-contactadosPostpago")))
        boton_final.click()
        log("YA PUEDES TERMINAR TU CHISTE")
        log("Ya puedes pegar la siguiente plantilla y presionar Enter...")
