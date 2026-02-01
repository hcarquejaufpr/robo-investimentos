# 🐳 Docker - Guia de Uso

## 📋 Pré-requisitos

Windows 10/11 com WSL 2 e Docker Desktop instalados.

## 🚀 Instalação do Docker

Execute como **Administrador**:

```powershell
.\install-docker.ps1
```

**Após instalação:**
1. ✅ Reinicie o computador
2. ✅ Inicie o Docker Desktop
3. ✅ Aguarde aparecer "Docker is running" na bandeja

## 🏗️ Comandos Docker

### Build e Start da Aplicação

```bash
# Build e inicia container
docker-compose up --build

# Modo detached (background)
docker-compose up -d --build
```

### Gerenciamento

```bash
# Para container
docker-compose down

# Ver logs
docker-compose logs -f

# Restart
docker-compose restart

# Ver containers rodando
docker ps
```

### Acesso

Após iniciar, acesse:
```
http://localhost:8501
```

## 🔧 Desenvolvimento com Hot Reload

O projeto usa **volumes** - mudanças no código refletem automaticamente no container (hot reload do Streamlit).

## 🗑️ Limpeza

```bash
# Remove containers e volumes
docker-compose down -v

# Remove imagens não usadas
docker system prune -a
```

## 📂 Estrutura Docker

- **Dockerfile**: Define imagem Python com dependências
- **docker-compose.yml**: Orquestra serviços e configurações
- **.dockerignore**: Arquivos excluídos do build

## ⚠️ Troubleshooting

**Container não inicia:**
```bash
docker-compose logs
```

**Porta 8501 ocupada:**
```bash
# Mude no docker-compose.yml:
ports:
  - "8502:8501"  # Acesse em localhost:8502
```

**Rebuild forçado:**
```bash
docker-compose build --no-cache
docker-compose up
```

## 🎯 Vantagens

✅ Ambiente isolado e reproduzível  
✅ Fácil deploy em cloud  
✅ Sem conflitos de dependências  
✅ Um comando para rodar tudo
