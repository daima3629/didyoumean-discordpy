from discord.ext import commands
import textwrap
from typing import List


class MessageGenerator:
    def __init__(self, command_name: str, similar_cmd_list: List[str]) -> None:
        self.command_name = command_name
        self.similar_cmd_list = similar_cmd_list

    async def send(self, ctx: commands.Context):
        raise NotImplementedError


class DefaultMessageGenerator(MessageGenerator):
    async def send(self, ctx):
        text = textwrap.dedent(
            f"""\
            Command `{self.command_name}` not found.
            did you mean: """
        )
        wrapped_similar_cmd_list = [f"`{c}`" for c in self.similar_cmd_list]
        text += ", ".join(wrapped_similar_cmd_list)
        await ctx.send(text)
