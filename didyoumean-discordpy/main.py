from discord.ext import commands
import difflib
from .message_generator import DefaultMessageGenerator, MessageGenerator
from typing import Optional, Mapping, Set, List


class DidYouMean(commands.Cog):
    """
    Core class of this library.

    Attributes
    ----------
    bot
        The bot object.
    matcher_dict : Mapping[str, difflib.SequenceMatcher]
        A dict for storing matchers.
    max_suggest : int
        Maximum number of suggestions.

    """
    def __init__(self, bot) -> None:
        self.bot = bot
        self.matcher_dict: Mapping[str, difflib.SequenceMatcher] = {}
        self.max_suggest = 3
        self._command_names: Set[str] = set()
        self._listup_commands(self.bot)
        self._max_command_length = max((len(c) for c in self._command_names))
        self._message_generator = DefaultMessageGenerator

    def set_message_generator(self, generator) -> None:
        """
        The function to set message generator.

        Parameters
        ----------
        generator
            This class inherits from the `MessageGenerator` class.

        Raises
        ------
        TypeError
            If the class does not inherit from `MessageGenerator`.

        """
        if not isinstance(generator, MessageGenerator):
            raise TypeError("Message generator must extend 'MessageGenerator'.")

        self._message_generator = generator

    def create_matcher(self, command_name: str) -> difflib.SequenceMatcher:
        matcher = difflib.SequenceMatcher(None, command_name)
        self.matcher_dict[command_name] = matcher
        return matcher

    def similar_factor_extraction(self, command: str) -> Optional[List[str]]:
        matcher = self.matcher_dict.get(command) or self.create_matcher(command)
        similar_cmd_list = []
        for name in self._command_names:
            matcher.set_seq2(name)
            ratio = matcher.ratio()
            if ratio > 0.6:
                similar_cmd_list.append((name, ratio))

        similar_cmd_list.sort(key=lambda c: c[1], reverse=True)
        if not similar_cmd_list:
            return

        return [c[0] for c in similar_cmd_list][:self.max_suggest]

    def _listup_commands(self, group, prefix=None) -> None:
        if prefix is None:
            prefix = []

        prefix_str = ' '.join(prefix) + ' ' if len(prefix) > 0 else ''

        for command in group.commands:
            if command.hidden:
                continue

            elif isinstance(command, commands.Group):
                names = [command.name] + list(command.aliases)
                for name in names:
                    self._command_names.add(prefix_str + name)
                    prefix.append(command.name)
                    self._listup_commands(command, prefix)
                    prefix.pop()

            elif isinstance(command, commands.Command):
                names = [command.name] + list(command.aliases)
                for name in names:
                    self._command_names.add(prefix_str + name)

    @commands.Cog.listener()
    async def on_ready(self):
        self._listup_commands(self.bot)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err) -> None:
        if not isinstance(err, commands.CommandNotFound):
            return

        invalid_command = ctx.message.content.lstrip(ctx.prefix)[:self._max_command_length]
        similar_list = self.similar_factor_extraction(invalid_command)
        if similar_list is None:
            return

        await self._message_generator(invalid_command[:len(similar_list[0])], similar_list).send(ctx)


def setup(bot):
    bot.add_cog(DidYouMean(bot))
