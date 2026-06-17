import os
import discord
from discord.ext import commands

CLIENT_ID = 
AVATAR_URL = (
    f"https://cdn.discordapp.com/avatars/{CLIENT_ID}/1eee7c7e0bba69ddfe8f8c3136c1bc89.png?size=4096&ignore=true)."
)
INVITE_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}"
SUPPORT_URL = "https://discord.gg/{URL FOR DISCORD SERVER}"
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID", "0"))


class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Menú principal", value="principal"),
            discord.SelectOption(
                label="Comandos de información",
                description="/ping, /help, /avatar, /invite",
                value="info",
                emoji="ℹ️",
            ),
            discord.SelectOption(
                label="Comandos de Música",
                description="/play, /queue, /skip, /stop, /set-volume",
                value="music",
                emoji="🎵",
            ),
        ]
        super().__init__(
            custom_id="menu",
            placeholder="Selecciona una categoria",
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Aquí va la lógica para cada categoría seleccionada (info, music, etc.)
        value = self.values[0]
        await interaction.response.send_message(
            f"Seleccionaste: {value}", ephemeral=True
        )


class BugReportModal(discord.ui.Modal, title="Reportar un Bug"):
    bug_title = discord.ui.TextInput(
        label="Título del bug",
        style=discord.TextStyle.short,
        placeholder="Ej: El comando /ping no responde",
        required=True,
        max_length=100,
    )
    bug_description = discord.ui.TextInput(
        label="Descripción",
        style=discord.TextStyle.paragraph,
        placeholder="Describe el bug con el mayor detalle posible...",
        required=True,
        max_length=1000,
    )
    bug_steps = discord.ui.TextInput(
        label="Pasos para reproducirlo",
        style=discord.TextStyle.paragraph,
        placeholder="1. Usa el comando...\n2. Haz click en...\n3. El error aparece...",
        required=False,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        steps = self.bug_steps.value or "No especificado"

        report_embed = discord.Embed(
            title="Nuevo Bug Reportado",
            color=0xFF0000,
            timestamp=discord.utils.utcnow(),
        )
        report_embed.add_field(name="📌 Título", value=self.bug_title.value, inline=False)
        report_embed.add_field(
            name="📝 Descripción", value=self.bug_description.value, inline=False
        )
        report_embed.add_field(
            name="🔁 Pasos para hacer el bug", value=steps, inline=False
        )
        report_embed.add_field(
            name="👤 Reportado por",
            value=f"{interaction.user} ({interaction.user.id})",
            inline=False,
        )
        report_embed.add_field(
            name="🌐 Servidor",
            value=(
                f"{interaction.guild.name} ({interaction.guild.id})"
                if interaction.guild
                else "DM / Canal privado"
            ),
            inline=False,
        )
        report_embed.set_thumbnail(url=interaction.user.display_avatar.url)

        try:
            # Enviar el reporte por MD al developer
            developer = await interaction.client.fetch_user(DEVELOPER_ID)
            await developer.send(embed=report_embed)

            await interaction.response.send_message(
                "✅ ¡Gracias! Tu reporte ha sido enviado correctamente.",
                ephemeral=True,
            )
        except Exception as err:
            print(f"❌ No se pudo enviar el reporte al developer: {err}")
            await interaction.response.send_message(
                "❌ Hubo un error al enviar el reporte. Inténtalo más tarde.",
                ephemeral=True,
            )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(f"❌ Error en el modal de bug report: {error}")
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "❌ Hubo un error al procesar el reporte.", ephemeral=True
            )


class BugReportButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Reportar Bug",
            custom_id="bug_report",
            style=discord.ButtonStyle.danger,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugReportModal())


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())
        self.add_item(
            discord.ui.Button(
                label="Invitar a kodi.py",
                style=discord.ButtonStyle.link,
                url=INVITE_URL,
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Servidor de Soporte",
                style=discord.ButtonStyle.link,
                url=SUPPORT_URL,
            )
        )
        self.add_item(BugReportButton())


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="❔ Lista de comandos del bot.")
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=(
                f"Bienvenido al panel de ayuda, te permite ver los comandos "
                f"disponibles de <@{CLIENT_ID}>."
            ),
            color=discord.Color.yellow(),
        )
        embed.set_author(name="kodi.py", icon_url=AVATAR_URL)
        embed.add_field(
            name="Comandos",
            value="> ``Puedes ver los comandos disponibles usando el menú de abajo``",
            inline=False,
        )
        embed.set_footer(text="made by kodidev", icon_url=AVATAR_URL)

        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
