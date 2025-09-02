# Polymarket -> Discord Alert Bot

Bot simple que vigila la API pública de Polymarket y envía una alerta a un canal de Discord
(via Webhook) cuando aparece un **mercado nuevo**. Pensado para desplegarse **gratis** en Render.

## 🚀 Despliegue rápido (Render)
1. Crea un repo en GitHub con estos archivos.
2. En Render: **New > Blueprint** y selecciona este repo (o **New > Background Worker**).
3. Render leerá `render.yaml` y creará un **Worker**.
4. En **Environment** añade `DISCORD_WEBHOOK` con la URL del webhook de tu canal de Discord.
5. Deploy. El bot empezará a vigilar y publicar alertas.

### Variables de entorno
- `DISCORD_WEBHOOK` (**obligatoria**): URL del webhook de tu canal de Discord.
- `POLYMARKET_POLL_SEC` (opcional): segundos entre consultas (por defecto 60).
- `KEYWORDS` (opcional): coma-separadas; si se define, solo alerta mercados cuyo título contenga alguna palabra (e.g., `bitcoin, election, eth`).
- `STATE_FILE` (opcional): archivo donde persiste el set de mercados ya vistos (por defecto `state.json`).

### ¿Cómo crear webhook en Discord?
- En tu servidor > canal > Editar canal > Integraciones > Webhooks > Nuevo webhook > Copiar URL.

## 🧪 Ejecución local (opcional)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/xxxxx/xxxxx"
python bot.py
```

## 🔒 Notas de seguridad
- **Nunca** subas tu `DISCORD_WEBHOOK` al repo.
- Configura el secret directamente en Render (o en variables de entorno locales).
