# Sistema IASO - Autodiscador Inteligente

![Versão](https://img.shields.io/badge/Versão-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Kotlin](https://img.shields.io/badge/Kotlin-1.8+-orange)
![Status](https://img.shields.io/badge/Status-Produção-success)

## 📋 Sobre o Sistema

O **Sistema IASO** (*Inteligência de Atendimento via Sistema de Orientação*) é uma solução moderna de autodiscagem desenvolvida para otimizar o agendamento e confirmação de exames na rede pública de saúde.

### 🎯 Objetivo Principal
Automatizar o contato com usuários para:
- ✅ Agendamento de exames médicos
- ✅ Confirmação de vagas de atendimento
- ✅ Reagendamento de consultas
- ✅ Redução de faltas e ociosidade na rede

## 🏗 Arquitetura do Sistema

### Backend - Python (`/backend`)
```python
# Estrutura principal
iaso-backend/
├── app/
│   ├── models/          # Modelos de dados
│   ├── services/        # Lógica de negócio
│   ├── api/            # Endpoints REST
│   └── core/           # Configurações
├── scripts/
│   ├── dialer.py       # Gerenciador de discagens
│   └── scheduler.py    # Agendador de tarefas
└── requirements.txt