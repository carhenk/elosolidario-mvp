# 🤝 EloSolidário — Gestão de Doações e Voluntariado

MVP desenvolvido para a disciplina **Experiência Prática – Projeto de Software**, voltado ao apoio operacional de organizações comunitárias na arrecadação, controle de estoque e distribuição justa de cestas básicas.

## 🌍 Alinhamento com os ODS da ONU
* **ODS 2 — Fome Zero e Agricultura Sustentável:** Redução do desperdício de alimentos perecíveis por meio de alertas automáticos de validade e estoque mínimo, além de histórico unificado de atendimentos para distribuição equitativa.

## 🏗️ Arquitetura e Stack Tecnológica
* **Padrão Arquitetural:** Monólito em Camadas (MVC)
* **Linguagem & Framework:** Python 3.12 + Flask 3.0
* **Interface Responsiva:** Bootstrap 5.3 (*Mobile-First*)
* **Persistência:** SQLAlchemy 2.0 + PostgreSQL (Supabase) / SQLite (Testes)
* **Segurança:** Werkzeug (`PBKDF2-HMAC-SHA256`), Flask-Login, Flask-WTF (CSRF)
* **Qualidade & Testes:** Pytest 8.0 (Padrão AAA)

## 📋 Funcionalidades Principais do MVP
* **RF01:** Autenticação segura com perfis (`Coordenador` e `Voluntário`).
* **RF02:** Controle de estoque com alertas visuais de saldo crítico e vencimento em 7 dias.
* **RF03:** Cadastro de famílias (CPF único) e registro de entregas com trava de 30 dias.
* **RF04:** Painel automático de necessidades urgentes compartilhável via WhatsApp.
