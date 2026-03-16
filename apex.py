from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import os
import traceback

# Para que funcione en PyInstaller
from utils import resource_path


def iniciar_bot(usuario, password, textbox):
    """
    Bot para automatizar la gestión de contactabilidad.
    """

    def log(msg):
        textbox.insert("end", msg + "\n")
        textbox.see("end")

    try:

        log("===== INICIANDO BOT =====")

        log(f"Directorio actual: {os.getcwd()}")

        try:
            archivos = os.listdir(os.getcwd())
            log(f"Archivos en carpeta actual: {archivos}")
        except:
            log("No se pudo listar archivos")

        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        log("Configuración de Chrome creada")

        # -----------------------------
        # SISTEMA HÍBRIDO DE DRIVER
        # -----------------------------

        driver_path = resource_path("chromedriver.exe")

        log(f"Ruta del driver detectada: {driver_path}")

        driver = None

        if os.path.exists(driver_path):

            log(" chromedriver.exe encontrado, usando driver local")

            service = Service(driver_path)

            log("Creando instancia del navegador con driver local...")

            driver = webdriver.Chrome(service=service, options=options)

        else:

            log("⚠ chromedriver.exe NO encontrado")
            log("Intentando usar Selenium Manager (automático)...")

            driver = webdriver.Chrome(options=options)

        log(" Navegador iniciado correctamente")

        driver.get(
            "https://gestorcampanas.claro.com.pe/ords/r/ws_usrcampana/gesti%C3%B3n-de-campa%C3%B1as-con-discadores174156/login"
        )

        log("Página de login cargada")

        wait = WebDriverWait(driver, 10)

        driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.element_to_be_clickable((By.ID, "P9999_USERNAME"))).send_keys(usuario)
        wait.until(EC.element_to_be_clickable((By.ID, "P9999_PASSWORD"))).send_keys(password)

        driver.find_element(By.ID, "P9999_PASSWORD").submit()

        wait.until(EC.element_to_be_clickable((By.ID, "t_MenuNav_1i"))).click()

        log("BOT INICIADO")
        log("Ya puedes pegar tu plantilla y presionar Enter...")

        # -------------------------
        # Procesar plantilla
        # -------------------------

        def procesar_plantilla(plantilla):

            try:

                identificador = None
                numero = None

                lineas = plantilla.split("\n")

                for i, linea in enumerate(lineas):

                    if "Identificación" in linea and i + 1 < len(lineas):
                        identificador = lineas[i + 1].strip()

                    if "Número llamado" in linea and i + 1 < len(lineas):
                        numero = lineas[i + 1].strip()

                if not (identificador and numero and numero.isdigit()):
                    log("T.T Plantilla incorrecta. Vuelve a pegarla completa.")
                    return

                log(f"Identificador detectado: {identificador}")
                log(f"Número detectado: {numero}")

                select = wait.until(
                    EC.presence_of_element_located((By.ID, "P5_SELECT_TIPO_BUSQUEDA"))
                )

                Select(select).select_by_value("2")

                campo_busqueda = wait.until(
                    EC.element_to_be_clickable((By.ID, "P5_BUSCA"))
                )

                campo_busqueda.clear()
                campo_busqueda.send_keys(numero)

                driver.execute_script(
                    "document.getElementById('P5_PHONE').innerText=''"
                )

                driver.find_element(By.ID, "boton").click()

                log("Esperando resultado de búsqueda...")

                telefono_encontrado = ""

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
                    return

                log("PROCEDIENDO CON CREACION DE CONTACTABILIDAD")

                campo_origen = wait.until(
                    EC.element_to_be_clickable((By.ID, "P5_NUMERO_ORIGEN_LLAMADA"))
                )

                campo_origen.clear()
                campo_origen.send_keys(numero)

                base_serial = identificador[:15]

                campo_serial = wait.until(
                    EC.element_to_be_clickable((By.ID, "P5_SERIAL_NUMBER"))
                )

                boton_guardar = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[text()='Guardar Contactabilidad']/..")
                    )
                )

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
                    return

                boton_guardar.click()

                confirmar = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class,'js-confirmBtn')]")
                    )
                )

                confirmar.click()

                time.sleep(2)

                log("CONTACTABILIDAD GUARDADA")

                log("Esperando habilitación de oportunidad...")

                boton_final = wait.until(
                    EC.element_to_be_clickable((By.ID, "btn-genera-contactadosPostpago"))
                )

                boton_final.click()

                log("YA PUEDES TERMINAR MUCHANCHO")
                log("Ya puedes pegar la siguiente plantilla y presionar Enter...")

            except Exception as e:

                log(" ERROR DURANTE EL PROCESO")
                log(str(e))
                log(traceback.format_exc())

        def on_enter(event=None):

            plantilla = textbox.get("1.0", "end").strip()

            if plantilla:

                threading.Thread(
                    target=procesar_plantilla,
                    args=(plantilla,)
                ).start()

                textbox.delete("1.0", "end")

            return "break"

        textbox.bind("<Return>", on_enter)

    except Exception as e:

        log(" ERROR CRÍTICO AL INICIAR EL BOT")
        log(str(e))
        log(traceback.format_exc())