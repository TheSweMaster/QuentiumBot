import discord
from discord.ext import commands
from QuentiumBot import GetData, get_translations

# Basic command configs
cmd_name = "listservers"
tran = get_translations()
aliases = [] if not tran[cmd_name]["fr"]["aliases"] else tran[cmd_name]["fr"]["aliases"].split("/")

class ListserversInfos(commands.Cog):
    """List servers command in Informations section"""

    def __init__(self, client):
        self.client = client

    @commands.command(
        name=cmd_name,
        aliases=aliases,
        pass_context=True,
        no_pm=True
    )
    @commands.guild_only()
    async def listservers_cmd(self, ctx):
        # Get specific server data
        if isinstance(ctx.channel, discord.TextChannel):
            data = await GetData.retrieve_data(self, ctx.message.guild)
            lang_server = data[0]
        else:
            lang_server = "en"
        server_id = ctx.message.guild.id
        cmd_tran = tran[cmd_name][lang_server]

        # Doesn't respond to bots
        if not ctx.message.author.bot == True:
            if not server_id == 264445053596991498:  # DBL ID
                data = await GetData.retrieve_data(self, ctx.message.guild, raw=True)
                serv_id = [str(server.id) for server in self.client.guilds]
                serv_id_exist = []
                serv_pos = []

                for serv in data.keys():
                    for server in serv_id:
                        if server == serv:
                            serv_pos.append(list(data).index(serv))
                            serv_id_exist.append(server)

                content = content2 = cmd_tran["msg_title"]
                for pos in range(len(serv_id_exist)):
                    if len(content) < 2000:
                        content += "\n- " + str(self.client.get_guild(int(serv_id_exist[pos]))) + " | " + str(serv_pos[pos])
                    else:
                        content2 += "\n- " + str(self.client.get_guild(int(serv_id_exist[pos]))) + " | " + str(serv_pos[pos])

                embed = discord.Embed(color=0xFF9111)
                embed.title = cmd_tran["msg_servers"].format(len(self.client.guilds))
                embed.description = content
                await ctx.send(embed=embed)
                if content2 != cmd_tran["msg_title"]:
                    embed2 = discord.Embed(color=0xFF9111)
                    embed2.title = None
                    embed2.description = content2
                    await ctx.send(embed=embed2)

def setup(client):
    client.add_cog(ListserversInfos(client))