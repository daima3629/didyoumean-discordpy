from discord.ext import commands
import difflib
from message_generator import DefaultMessageGenerator, MessageGenerator
from typing import Optional, Mapping, List


class DidYouMean:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.matcher_dict: Mapping[str, difflib.SequenceMatcher] = {}
        self.max_suggest = 3
        self._message_generator = DefaultMessageGenerator

    def set_message_generator(self, generator) -> None:
        if not isinstance(generator, MessageGenerator):
            raise TypeError("Message generator must extend 'MessageGenerator'.")

        self._message_generator = generator

    def create_matcher(self, command_name: str) -> difflib.SequenceMatcher:
        matcher = difflib.SequenceMatcher(None, command_name)
        self.matcher_dict[command_name] = matcher
        return matcher

    def similar_factor_extraction(self, command_name: str) -> Optional[List[str]]:
        matcher = self.matcher_dict.get(command_name) or self.create_matcher(command_name)
        cmd_name_generator = (c.name for c in self.bot.walk_commands())
        similar_cmd_list = []
        for name in cmd_name_generator:
            matcher.set_seq2(name)
            ratio = matcher.ratio()
            if ratio > 0.6:
                similar_cmd_list.append((name, ratio))

        similar_cmd_list.sort(key=lambda c: c[1], reverse=True)
        return [c[0] for c in similar_cmd_list][:self.max_suggest]

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err) -> None:
        if not isinstance(err, commands.CommandNotFound):
            await self.bot.on_command_error(ctx, err)
            return

        similar_list = self.similar_factor_extraction(ctx.command.name)
        if similar_list is None:
            return

        await self._message_generator(similar_list).send(ctx)


def setup(bot):
    bot.add_cog(DidYouMean(bot))
