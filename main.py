import customtkinter as ctk
import threading
import json
import os
from PIL import Image
from utils import resource_path  # <<<<<< RECURSOS EXE

try:
    from apex import iniciar_bot
except ImportError:
    def iniciar_bot(usuario, password, textbox):
        print("Simulando bot...")

CONFIG_FILE = resource_path("config.json")  # <<<<<< RECURSOS EXE

def guardar_credenciales(usuario, password):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"usuario": usuario, "password": password}, f)

def cargar_credenciales():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("usuario", ""), data.get("password", "")
    return "", ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("APP - EX")
        self.geometry("950x650")

        # Rutas usando resource_path
        self.logo_path_png = resource_path("nick.png")
        self.logo_path_ico = resource_path("nick.ico")
        try:
            self.iconbitmap(self.logo_path_ico)
        except:
            pass

        self.purple_main = "#8A2BE2"
        self.purple_hover = "#7A22D1"
        self.bg_color_total = ("#F2F2F2", "#101010")
        self.text_color = ("#242424", "#FFFFFF")
        self.frame_bg = ("#EBEBEB", "#1A1A1A")
        self.border_color = ("#D0D0D0", "#333333")

        self.configure(fg_color=self.bg_color_total)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== SIDEBAR =====
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0, fg_color="transparent")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo y título
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(self.logo_path_png),
                dark_image=Image.open(self.logo_path_png),
                size=(80, 80)
            )
            self.logo_image_label = ctk.CTkLabel(self.sidebar_frame, image=logo_img, text="")
            self.logo_image_label.grid(row=0, column=0, padx=10, pady=(30,0))
        except:
            pass
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="BOT CAT",
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       text_color=self.purple_main)
        self.logo_label.grid(row=1, column=0, padx=10, pady=(10,20))

        # Botones
        self.btn_login = ctk.CTkButton(self.sidebar_frame, text="Login", height=35,
                                       fg_color="transparent", text_color=self.text_color,
                                       hover_color=("#EAEAEA", "#2B2B2B"), anchor="w",
                                       command=self.mostrar_login)
        self.btn_login.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        self.btn_plantilla = ctk.CTkButton(self.sidebar_frame, text="Plantilla", height=35,
                                           fg_color="transparent", text_color=self.text_color,
                                           hover_color=("#EAEAEA", "#2B2B2B"), anchor="w",
                                           command=self.mostrar_plantilla)
        self.btn_plantilla.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        # Selector de apariencia
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Dark","Light"], height=28,
            fg_color=self.frame_bg, button_color=self.frame_bg,
            text_color=self.text_color, command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=15, pady=20)

        # ===== MAIN FRAME =====
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.setup_login_view()
        self.setup_plantilla_view()
        self.mostrar_login()

    # ===== FUNCIONES LOGIN & PLANTILLA =====
    def setup_login_view(self):
        self.login_view = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.login_card = ctk.CTkFrame(self.login_view, corner_radius=20,
                                       fg_color=self.frame_bg, border_width=2, border_color=self.border_color)
        self.login_card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.login_card, text="ACCESO AL SISTEMA",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=self.text_color).pack(pady=(40,25), padx=60)

        self.usuario_entry = ctk.CTkEntry(self.login_card, width=260, placeholder_text="Usuario",
                                          height=42, fg_color=self.bg_color_total,
                                          border_width=1, text_color=self.text_color)
        self.usuario_entry.pack(pady=10, padx=60)

        self.pass_entry = ctk.CTkEntry(self.login_card, width=260, placeholder_text="Contraseña",
                                       height=42, fg_color=self.bg_color_total,
                                       border_width=1, text_color=self.text_color)
        self.pass_entry.pack(pady=10, padx=60)

        u,p = cargar_credenciales()
        self.usuario_entry.insert(0,u)
        self.pass_entry.insert(0,p)

        self.boton_login = ctk.CTkButton(self.login_card, text="INICIAR BOT",
                                        width=180, height=45, fg_color=self.purple_main,
                                        hover_color=self.purple_hover,
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        command=self.ejecutar_bot)
        self.boton_login.pack(pady=(30,50))

    def setup_plantilla_view(self):
        self.plantilla_view = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.plantilla_view.grid_columnconfigure(0, weight=1)
        self.plantilla_view.grid_rowconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self.plantilla_view, corner_radius=12, border_width=2,
                                      fg_color=self.frame_bg, border_color=self.border_color,
                                      text_color=self.text_color, font=("Consolas",12))
        self.textbox.grid(row=0, column=0, padx=25, pady=25, sticky="nsew")

        self.info_panel = ctk.CTkFrame(self.plantilla_view, width=250, corner_radius=12,
                                       fg_color=self.frame_bg, border_width=2, border_color=self.border_color)
        self.info_panel.grid(row=0, column=1, padx=(0,25), pady=25, sticky="nsew")
        self.info_panel.grid_propagate(False)

        ctk.CTkLabel(self.info_panel, text="INSTRUCCIONES",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=self.text_color).pack(pady=(20,10))

        ctk.CTkLabel(self.info_panel, text="Pega la siguiente plantilla:",
                     font=ctk.CTkFont(size=11, slant="italic"), text_color=self.text_color).pack(padx=20, anchor="w")

        plantilla_ejemplo = "Identificación del cliente\n2xxxxxxxxxxxxxxxxxx\nNúmero llamado\n9xxxxxxxx"
        ctk.CTkLabel(self.info_panel, text=plantilla_ejemplo,
                     fg_color=self.bg_color_total, text_color=self.text_color,
                     corner_radius=8, padx=15, pady=15, justify="left",
                     font=("Consolas",11)).pack(padx=20,pady=20,fill="x")

    # ===== MOSTRAR VIEWS =====
    def mostrar_login(self):
        self.plantilla_view.grid_forget()
        self.login_view.grid(row=0,column=0,sticky="nsew")
        self.btn_login.configure(fg_color=("#E6D8FF","#3D2B56"), text_color=self.purple_main)
        self.btn_plantilla.configure(fg_color="transparent", text_color=self.text_color)

    def mostrar_plantilla(self):
        self.login_view.grid_forget()
        self.plantilla_view.grid(row=0,column=0,sticky="nsew")
        self.btn_plantilla.configure(fg_color=("#E6D8FF","#3D2B56"), text_color=self.purple_main)
        self.btn_login.configure(fg_color="transparent", text_color=self.text_color)

    def ejecutar_bot(self):
        usuario = self.usuario_entry.get()
        password = self.pass_entry.get()
        guardar_credenciales(usuario,password)
        self.boton_login.configure(text="EJECUTANDO...", state="disabled", fg_color="gray")
        threading.Thread(target=iniciar_bot, args=(usuario,password,self.textbox), daemon=True).start()

    def change_appearance_mode_event(self, new_appearance_mode:str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
