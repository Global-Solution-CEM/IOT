// Configuração PM2 para Aprenda Plus API
module.exports = {
  apps: [{
    name: 'aprenda-plus-api',
    script: 'main.py',
    interpreter: 'python',
    cwd: __dirname,
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      PORT: 8000,
      PYTHONUNBUFFERED: '1'
    },
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_file: './logs/pm2-combined.log',
    time: true
  }]
}

