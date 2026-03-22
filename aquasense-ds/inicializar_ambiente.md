## Configuração do ambiente (Aquasense DS)

### 1) Entrar na pasta do projeto

```bash
cd aquasense-ds
```

### 2) Criar ambiente virtual

```bash
python3 -m venv .venv
```

### 3) Ativar ambiente virtual

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

### 4) Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Reprodutibilidade entre máquinas

Para recriar exatamente o mesmo ambiente de quem configurou primeiro, use também o lock de versões:

```bash
pip install -r requirements-lock.txt
```