# 🎹 Teremim Invisível

Transforme seu dispositivo em um instrumento musical virtual usando gestos de mão capturados pela câmera!  
Este projeto utiliza Python, MediaPipe, Kivy e SoundDevice para criar uma experiência lúdica e interativa, permitindo que qualquer pessoa toque um "teremim virtual" sem precisar de hardware especializado.

---

## 🎯 Objetivo

Desenvolver uma aplicação que transforme gestos de mão em sons sintetizados em tempo real, priorizando baixa latência, fluidez e uma interface intuitiva.

---

## ✨ Funcionalidades Principais

- **Captura de vídeo em tempo real** usando a câmera do dispositivo
- **Detecção de gestos de mão** com MediaPipe Hands
- **Controle sonoro intuitivo**:
  - Elevar/descender a mão direita: altera a altura da nota (frequência)
  - Gesto de pinça com a mão esquerda: ajusta o pitch geral do som
- **Geração de sons sintéticos** no estilo synthwave/teremim
- **Feedback visual** simples e intuitivo na tela

---

## 🛠️ Tecnologias

- **Python 3.11+**
- **MediaPipe Hands** para detecção de gestos
- **Kivy** para interface multiplataforma
- **SoundDevice** para síntese sonora de baixa latência
- **OpenCV** para captura de vídeo

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```
   git clone https://github.com/seu-usuario/teremim-invisivel.git
   cd teremim-invisivel
   ```

2. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

3. **Execute o projeto:**
   ```
   python main.py
   ```

---

## 🎛️ Requisitos Técnicos

- **Dispositivo com câmera**
- **Python 3.11+**
- **Permissão de acesso à câmera**
- **Sistema operacional compatível** (Windows, Linux, macOS ou Android via Buildozer)

---

## 📅 Checkpoints de Desenvolvimento

O projeto foi estruturado em etapas granulares para facilitar o acompanhamento e a colaboração:

1. **Configuração do ambiente base**
2. **Captura de vídeo e pipeline inicial**
3. **Detecção de gestos com MediaPipe**
4. **Síntese sonora em tempo real**
5. **Loop principal de integração**
6. **Interface Kivy com feedback visual**
7. **Otimização de performance**
8. **Testes e validação final**

---

## 🤝 Contribua

Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests!

---

## 📄 Licença

[MIT](LICENSE)