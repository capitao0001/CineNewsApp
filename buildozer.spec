[app]

# Nome do app (aparece no celular)
title = CineNews

# Nome do pacote (identificador único)
package.name = cinenews

# Domínio do pacote
package.domain = org.cinenews.app

# Versão
version = 1.0.0

# Arquivo principal do app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Versão do Android
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b

# ==========================================
# PERMISSÕES - CÂMERA E INTERNET
# ==========================================
android.permissions = CAMERA, INTERNET, ACCESS_NETWORK_STATE

# Ícone do app
icon.filename = icone.png

# Linguagem
android.strings = 

# Requisitos (bibliotecas que o app precisa)
requirements = python3,kivy,requests,Pillow

# Orientação
orientation = portrait

# Modo fullscreen (remove barra superior)
fullscreen = 0

# ==========================================
# CONFIGURAÇÕES DO BUILD
# ==========================================

# Versão do Python
android.python_version = 3

# Compressão
android.gradle_dependencies = 

# Log level
android.log_lvl = 2

# Argumentos
android.add_jars = 
android.gradle_api_level = 30
android.library_references = 

# Meta-dados
android.long_name = CineNews - Notícias e Filmes
android.description = Fique por dentro das últimas notícias, filmes e séries
android.author = CineNews Studio
