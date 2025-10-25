# 🚀 Gerenciamento do Servidor Nhandereko

## Visão Geral

O servidor Nhandereko suporta **dois modos de execução**:

1. **Modo Interativo** (padrão): O servidor roda em primeiro plano, mostrando logs no terminal
2. **Modo Daemon**: O servidor roda em segundo plano, liberando o terminal para outros comandos

## 📝 Comandos Disponíveis

### Iniciar Servidor

```bash
# Modo interativo (logs no terminal)
./scripts/start-server.sh

# Modo daemon (segundo plano)
./scripts/start-server.sh -d

# Ver ajuda
./scripts/start-server.sh -h
```

### Parar Servidor

```bash
./scripts/stop-server.sh
```

Funciona tanto para servidor em modo interativo quanto daemon.

### Verificar Status

```bash
./scripts/status-server.sh
```

Mostra:

- ✅ Status do servidor (rodando ou parado)
- 📋 PID do processo
- 🔧 Informações do processo (CPU, memória, tempo de execução)
- 📝 Últimas 10 linhas do log

## 🔄 Fluxo de Trabalho Recomendado

### Desenvolvimento (modo interativo)

```bash
# Iniciar servidor
./scripts/start-server.sh

# Servidor roda em primeiro plano
# Logs aparecem diretamente no terminal
# Pressione Ctrl+C para parar
```

### Produção/Testes (modo daemon)

```bash
# Iniciar em segundo plano
./scripts/start-server.sh -d

# Terminal fica livre para outros comandos
# ✅ Servidor iniciado em segundo plano (PID: 12345)

# Verificar status
./scripts/status-server.sh

# Ver logs em tempo real
tail -f logs/server.log

# Parar quando necessário
./scripts/stop-server.sh
```

## 📂 Arquivos de Controle

Quando executado em modo daemon, o sistema cria:


### `logs/server.pid`


- Armazena o PID do processo do servidor
- Usado para controlar e verificar o processo
- Removido automaticamente quando o servidor para


### `logs/server.log`


- Contém toda a saída do servidor (stdout + stderr)
- Cresce continuamente enquanto o servidor roda
- Use `tail -f logs/server.log` para monitorar em tempo real

## 🛡️ Segurança e Prevenção de Erros

### Servidor já rodando

```bash
$ ./scripts/start-server.sh -d
⚠️  Servidor já está rodando (PID: 12345)
Para parar o servidor, execute: ./scripts/stop-server.sh
```

O sistema previne múltiplas instâncias rodando simultaneamente.

### Processo morto mas PID existe

Se o arquivo PID existe mas o processo não está rodando (ex: kill manual), o sistema:

- Detecta automaticamente a situação
- Remove o arquivo PID obsoleto
- Permite iniciar o servidor normalmente

### Parada graciosa

```bash
$ ./scripts/stop-server.sh
📋 PID do servidor: 12345
🔄 Enviando sinal TERM...
```

O script:

1. Envia `SIGTERM` (parada graciosa)
2. Aguarda até 10 segundos
3. Se não responder, força com `SIGKILL`
4. Remove arquivo PID

## 💡 Dicas de Uso

### Ver logs em tempo real

```bash
# Seguir logs do servidor daemon
tail -f logs/server.log

# Ver apenas últimas 50 linhas
tail -n 50 logs/server.log

# Buscar erros nos logs
grep -i error logs/server.log
```

### Monitorar recursos

```bash
# Ver informações detalhadas do processo
./scripts/status-server.sh

# Ou manualmente
ps aux | grep "python.*main.py"
```

### Rotação de logs

Para evitar que `logs/server.log` cresça indefinidamente:

```bash
# Limpar logs antigos (com servidor parado)
./scripts/stop-server.sh
> logs/server.log  # Esvazia o arquivo
./scripts/start-server.sh -d

# Ou salvar logs antigos
./scripts/stop-server.sh
mv logs/server.log logs/server-$(date +%Y%m%d-%H%M%S).log
./scripts/start-server.sh -d
```

## 🔍 Troubleshooting

### Servidor não inicia

```bash
# Verificar se porta 8000 já está em uso
lsof -i :8000

# Verificar logs de erro
cat logs/server.log
```

### Servidor não para

```bash
# Forçar término manual
kill -9 $(cat logs/server.pid)
rm logs/server.pid
```

### Ver processos Python rodando

```bash
ps aux | grep python
```

## 🎯 Exemplos Práticos

### Desenvolvimento: testar mudanças rapidamente

```bash
# Modo interativo para ver logs imediatamente
./scripts/start-server.sh

# Fazer requisições, ver logs
# Ctrl+C para parar

# Fazer alterações no código

# Reiniciar
./scripts/start-server.sh
```

### Testes automatizados: servidor em background

```bash
# Iniciar servidor
./scripts/start-server.sh -d

# Executar testes
pytest tests/

# Parar servidor
./scripts/stop-server.sh
```

### Servidor permanente: manter rodando

```bash
# Iniciar em daemon
./scripts/start-server.sh -d

# Verificar periodicamente
./scripts/status-server.sh

# Logs em outro terminal
tail -f logs/server.log
```

## 📊 Comparação dos Modos

| Aspecto | Modo Interativo | Modo Daemon |
|---------|----------------|-------------|
| **Comando** | `./scripts/start-server.sh` | `./scripts/start-server.sh -d` |
| **Terminal** | Bloqueado | Livre |
| **Logs** | Console | `logs/server.log` |
| **Parada** | `Ctrl+C` | `./scripts/stop-server.sh` |
| **Controle PID** | Não | Sim (`logs/server.pid`) |
| **Uso recomendado** | Desenvolvimento | Produção/Testes |
| **Monitoramento** | Visual direto | `status-server.sh` / `tail -f` |

## 🎓 Integração com Agentes

Os agentes podem:

1. **Iniciar o servidor automaticamente** antes de executar tarefas
2. **Verificar se está rodando** antes de fazer requisições
3. **Parar o servidor** após concluir o trabalho

Exemplo em Python:

```python
import subprocess
import time
import requests

# Verificar se servidor está rodando
result = subprocess.run(
    ["./scripts/status-server.sh"],
    capture_output=True,
    text=True
)

if "não está rodando" in result.stdout:
    # Iniciar em daemon mode
    subprocess.run(["./scripts/start-server.sh", "-d"])
    time.sleep(5)  # Aguardar inicialização

# Fazer requisições
response = requests.get("http://localhost:8000/health")

# Opcionalmente parar (ou deixar rodando para próximas tarefas)
# subprocess.run(["./scripts/stop-server.sh"])
```

---

**🌱 Nhandereko**: Sistema de Feedback Loops Recursivos para Aprendizado Coletivo
