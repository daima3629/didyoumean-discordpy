from discord.ext import commands
import textwrap
from typing import List


class MessageGenerator:
    """
    Base class for the message generator.
    You should inherit from this class to implement your message generator.

    Parameters
    ----------
    invalid_command_name : str
        The invalid command name.
    similar_cmd_list : List[str]
        The similar command name list to `invalid_cmd_name`.

    Attributes
    ----------
    invalid_command_name : str
        The invalid command name.
    similar_cmd_list : List[str]
        The similar command name list to `invalid_cmd_name`.
    """
    def __init__(self, invalid_cmd_name: str, similar_cmd_list: List[str]) -> None:
        self.invalid_cmd_name = invalid_cmd_name
        self.similar_cmd_list = similar_cmd_list

    async def send(self, ctx: commands.Context):
        """
        The method to be called when sending a message.
        You must override this method.

        Parameters
        ----------
        ctx : commands.Context
            The context that should be used to send message.

        """
        raise NotImplementedError


class DefaultMessageGenerator(MessageGenerator):
    async def send(self, ctx):
        text = textwrap.dedent(
            f"""\
            Command `{self.invalid_cmd_name}` not found.
            did you mean: """
        )
        wrapped_similar_cmd_list = [f"`{c}`" for c in self.similar_cmd_list]
        text += ", ".join(wrapped_similar_cmd_list)
        await ctx.send(text)
