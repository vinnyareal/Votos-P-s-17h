param (
    [string]$RepoUrl
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Publicador Git para o Repositorio de Analise Eleitoral  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git não está instalado ou não foi encontrado no PATH."
    exit 1
}

# 2. Inicializar se necessário
if (-not (Test-Path ".git")) {
    Write-Host "[1/4] Inicializando repositório Git local..." -ForegroundColor Yellow
    git init -b main
} else {
    Write-Host "[1/4] Repositório Git já inicializado." -ForegroundColor Green
}

# 3. Configurar usuário caso não exista
$userName = git config user.name
$userEmail = git config user.email

if (-not $userName) {
    git config user.name "Vinicius"
    Write-Host "Configurado user.name: Vinicius" -ForegroundColor Gray
}
if (-not $userEmail) {
    git config user.email "vinnyareal@hotmail.com"
    Write-Host "Configurado user.email: vinnyareal@hotmail.com" -ForegroundColor Gray
}

# 4. Adicionar arquivos e commitar
Write-Host "[2/4] Adicionando arquivos ao commit..." -ForegroundColor Yellow
git add .

$status = git status --porcelain
if ($status) {
    Write-Host "[3/4] Criando commit inicial..." -ForegroundColor Yellow
    git commit -m "feat: analise oficial dos votos pos-17h, dataset 2026 e apresentacao em video vertical 9:16"
} else {
    Write-Host "[3/4] Nenhum arquivo novo para commitar." -ForegroundColor Green
}

# 5. Configurar Remote e Push
if ($RepoUrl) {
    Write-Host "[4/4] Conectando ao repositório remoto: $RepoUrl" -ForegroundColor Yellow
    git remote remove origin -ErrorAction SilentlyContinue
    git remote add origin $RepoUrl
    git branch -M main
    Write-Host "Enviando commits para o GitHub (git push -u origin main)..." -ForegroundColor Cyan
    git push -u origin main
    Write-Host "Publicação concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "`n[Próximo Passo para Publicar no GitHub]" -ForegroundColor Magenta
    Write-Host "Para enviar para a sua conta do GitHub, crie um novo repositório em https://github.com/new e execute:" -ForegroundColor White
    Write-Host "  .\setup_git.ps1 -RepoUrl 'https://github.com/SEU_USUARIO/NOME_DO_REPO.git'`n" -ForegroundColor Yellow
}
