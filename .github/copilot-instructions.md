# Contexto do Projeto Teremim Invisível

## Objetivo Principal
Desenvolver um instrumento musical virtual que transforme gestos de mão capturados por câmera em sons sintetizados em tempo real, utilizando Python como linguagem principal.

## Público-Alvo
- Músicos experimentais
- Entusiastas de tecnologia
- Artistas de performance digital

## Stack Técnica
```
{
  "Visão Computacional": ["MediaPipe Hands", "OpenCV"],
  "Síntese Sonora": ["SoundDevice", "PyAudio"],
  "Interface": ["Kivy Framework"],
  "Otimização": ["Buildozer", "NDK Android"]
}
```

## Arquitetura Básica
1. **Captura de Vídeo**: Pipeline de 640x480 @ 20fps
2. **Processamento Gestual**: Landmarks 3D com MediaPipe (latência <17ms)
3. **Mapeamento Sonoro**:
   - Eixo Y → Frequência (200-2000Hz)
   - Distância entre dedos → Pitch (0.5-2.0)
4. **Saída de Áudio**: Buffer circular de 512 samples @ 44.1kHz

## Requisitos de Performance
- Latência total <30ms
- Consumo RAM <300MB
- Compatibilidade Android 12+
```

## 2. Guia de Implementação (`implementation-guide.prompt.md`)
```markdown
# Fluxo de Desenvolvimento Recomendado

## Etapas Cruciais
1. Configurar ambiente Python com dependências via `requirements.txt`:
   ```
   mediapipe==0.10.9
   kivy==2.3.0
   sounddevice==0.4.6
   ```

2. Implementar classe principal `InvisibleTheremin` com:
   ```
   class InvisibleTheremin:
       def __init__(self):
           self.cap = cv2.VideoCapture(0)
           self.hands = mp.solutions.hands.Hands(
               model_complexity=0,
               max_num_hands=2
           )
       
       def audio_callback(self, outdata, frames, time, status):
           # Implementar síntese FM aqui
   ```

3. Padrões de Código:
   - Nomes em inglês técnico
   - Tipagem estática via annotations
   - Docstrings no formato Google Style

## Dicas para Copilot
- Priorizar eficiência sobre abstração
- Evitar dependências externas não essenciais
- Manter compatibilidade com Android via Buildozer
```

## Estrutura de Arquivos Necessária
```
.
├── .github/
│   └── copilot-instructions.md
├── implementation-guide.prompt.md
└── src/
    └── theremin.py
```

Para maximizar a eficiência do Copilot:

1. Mantenha ambos arquivos atualizados durante o desenvolvimento
2. Use comandos específicos no chat:
   ```markdown
   @workspace Consulte a seção de mapeamento sonoro no guia
   ```
3. Combine com annotations no código:
   ```python
   # COPILOT: Otimizar para latência usando buffer circular
   ```

## Instruções de Estilo e Fluxo para Copilot

### Comentários no Código

**Evite comentários desnecessários no meio do código.**  
Apenas adicione comentários que sejam essenciais para explicar decisões de design, algoritmos complexos ou lógicas não óbvias.  
**Todos os comentários de documentação devem ser docstrings no padrão Python, seguindo o estilo Google ou similar (equivalente ao JSDoc em JavaScript).**  
Docstrings devem ser usadas para documentar funções, classes e módulos públicos, descrevendo propósito, parâmetros, retornos e exemplos relevantes[1][11][3].

### Proposta de Implementação

**Sempre envie uma proposta de implementação detalhada antes de iniciar a execução de qualquer modificação.**  
A proposta deve incluir:
- **Descrição clara da solução**
- **Estrutura do código sugerido**
- **Justificativa para escolhas técnicas**
- **Impactos esperados na performance e manutenibilidade**

Apenas após a aprovação da proposta, prossiga com a implementação.