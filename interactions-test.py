import interactions
import constants

bot = interactions.Client(token=constants.TOKEN)


@bot.command(
    scope=constants.GUILD_ID
)
async def modal_test(ctx: interactions.CommandContext):
    """Creates a simple modal form"""
    modal = interactions.Modal(
        title="Form",
        custom_id="mod_form",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label="Let's get straight to it: what's 1 + 1?",
                custom_id="text_input_response",
                min_length=1,
                max_length=3,
            )
        ]
    )

    await ctx.popup(modal)


@bot.modal("mod_form")
async def modal_response(ctx: interactions.CommandContext, response: str):
    await ctx.send("Correct" if response == "2" else "WRONG")


bot.start()
