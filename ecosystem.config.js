module.exports = {
  apps : [{
    name: "talentobot",
    script: "main.py",
    interpreter: "python",
    interpreter_args: "main.py",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "1G",
    env: {
      NODE_ENV: "production"
    }
  }]
};
