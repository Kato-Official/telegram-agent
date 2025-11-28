module.exports = {
    apps: [{
        name: "telegram-agent",
        script: "server.py",
        interpreter: "./.venv/bin/python",
        env: {
            NODE_ENV: "development",
        },
        env_production: {
            NODE_ENV: "production",
        }
    }]
}
