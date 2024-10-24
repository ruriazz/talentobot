module.exports = {
  apps: [
    {
      name: "bot",
      script: "cmd/discordbot.py",
      interpreter: "python",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "2G",
      env: {
        NODE_ENV: "production"
      }
    },
    {
      name: "cron",
      script: "cmd/cron.py",
      interpreter: "python",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "2G",
      env: {
        NODE_ENV: "production"
      }
    },
    {
      name: "api",
      script: "/app/dist/src/index.js",
      interpreter: "node",  // Use node as the interpreter for JavaScript
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "2G",
      env: {
        NODE_ENV: "production"
      }
    }
  ]
};
