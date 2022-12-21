from discord import app_commands, SelectOption, Interaction, TextStyle, Embed, Object
from discord.ext import commands
from discord.ui import View, Select, Modal, TextInput

mainOp = {
    "flower": ["HP"],
    "plume": ["ATK"],
    "sand": ["HP%", "ATK%", "DEF%", "Elemental Mastery", "Energy Recharge%"],
    "goblet": ["HP%", "ATK%", "DEF%", "Elemental Mastery", "Elemental Damage Bonus%"],
    "circlet": ["HP%", "ATK%", "DEF%", "Elemental Mastery", "Healing Bonus%", "Crit Rate%", "Crit DMG%"]
}

subOp = [
    "ATK",
    "ATK%",
    "DEF",
    "DEF%",
    "HP",
    "HP%",
    "Elemental Mastery",
    "Energy Recharge%",
    "Crit Rate%",
    "Crit DMG%"
]

class ArtifactBaseSelectView(View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ArtifactBaseSelect())


class ArtifactBaseSelect(Select):
    def __init__(self):
        options = []
        options.append(SelectOption(label="flower", emoji="<:PaleFlameStainlessBloom:1054994317300740216>", description="HP"))
        options.append(SelectOption(label="plume", emoji="<:PaleFlameWiseDoctorsPinion:1054994302478057482>", description="ATK"))
        options.append(SelectOption(label="sand", emoji="<:PaleFlameMomentofCessation:1054994289588981770>", description=",".join(mainOp["sand"])))
        options.append(SelectOption(label="goblet", emoji="<:PaleFlameSurpassingCup:1054994275915534366>", description=",".join(mainOp["goblet"])))
        options.append(SelectOption(label="circlet", emoji="<:PaleFlameMockingMask:1054994253190807552>", description=",".join(mainOp["circlet"])))

        super().__init__(placeholder="select main Artifact types", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        view = View()
        view.add_item(ArtifactSuboptionSelect(self.values[0]))
        await interaction.response.edit_message(content="select sub options.", view=view)

class ArtifactSuboptionSelect(Select):
    def __init__(self, mainType: str):
            self.listSubOption: list[SelectOption] = []
            self.mainType = mainType
            for v in subOp:
                self.listSubOption.append(SelectOption(label=v))
            super().__init__(placeholder="select sub options ※Up to 4 options available", max_values=4, options=self.listSubOption)

    async def callback(self, interaction: Interaction):
        result = []
        for n in self.values:
            result.append(n)
        await interaction.response.send_modal(ArtifactSuboptionValueModal(result, self.mainType))
        print(f"executor:{interaction.user.name}\nartifact - select sub option...")

class ArtifactSuboptionValueModal(Modal):
    def __init__(self, list: list, mainType: str):
        super().__init__(title="numeric entry", timeout=300)
        self.list = list
        self.mainType = mainType

        try:
            self.contentA = TextInput(
                label=f"{self.list[0]}",
                style=TextStyle.short,
                placeholder=f"{self.list[0]} value",
                required=True
            )
            self.add_item(self.contentA)
        except:
            print("Null")
        try:
            self.contentB = TextInput(
                label=f"{self.list[1]}",
                style=TextStyle.short,
                placeholder=f"{self.list[1]} value",
                required=True
            )
            self.add_item(self.contentB)
        except:
            print("Null")
        try:
            self.contentC = TextInput(
                label=f"{self.list[2]}",
                style=TextStyle.short,
                placeholder=f"{self.list[2]} value",
                required=True
            )
            self.add_item(self.contentC)
        except:
            print("Null")
        try:
            self.contentD = TextInput(
                label=f"{self.list[3]}",
                style=TextStyle.short,
                placeholder=f"{self.list[3]} value",
                required=True
            )
            self.add_item(self.contentD)
        except:
            print("Null")

    async def on_submit(self, interaction: Interaction):
        result = {}
        try:
            result[self.list[0]] = self.contentA.value
        except:
            print("Null")
        try:
            result[self.list[1]] = self.contentB.value
        except:
            print("Null")
        try:
            result[self.list[2]] = self.contentC.value
        except:
            print("Null")
        try:
            result[self.list[3]] = self.contentD.value
        except:
            print("Null")

        view = View()
        view.add_item(ArtifactScoreSelectView(result, self.mainType))

        await interaction.response.edit_message(content="Score Calculation Methods", view=view)

class ArtifactScoreSelectView(Select):
    def __init__(self, resultDict: dict, mainType: str):
        options = []
        self.mainType = mainType
        self.subDict = resultDict
        options.append(SelectOption(label="Crit build", description=r"ATK%+Crit Rate%x2+Crit DMG%"))
        options.append(SelectOption(label="HP build", description=r"HP%+Crit Rate%x2+Crit DMG%"))
        options.append(SelectOption(label="DEF build", description=r"DEF%+Crit Rate%x2+Crit DMG%"))
        options.append(SelectOption(label="Energy Recharge build", description=r"Energy Recharge%+Crit Rate%x2+Crit DMG%"))
        options.append(SelectOption(label="Elemental Mastery build", description=r"(Elemental Mastery+Crit Rate%x2+Crit DMG)/2"))

        super().__init__(placeholder="Select a score calculation method", options=options)

    async def callback(self, interaction: Interaction):
        try:
            attack = 0
            rate = 0
            damage = 0
            hp = 0
            defense = 0
            charge = 0
            mastery = 0

            result = 0

            if self.values[0] == "Crit build":
                for k, v in self.subDict.items():
                    if k == "ATK%":
                        attack = v
                    elif k == "Crit Rate%":
                        rate = v
                    elif k == "Crit DMG%":
                        damage = v
                result = float(attack) + float(rate)*2 + float(damage)
            elif self.values[0] == "HP build":
                for k, v in self.subDict.items():
                    if k == "HP%":
                        hp = v
                    elif k == "Crit Rate%":
                        rate = v
                    elif k == "Crit DMG%":
                        damage = v
                result = float(hp) + float(rate)*2 + float(damage)
            elif self.values[0] == "DEF build":
                for k, v in self.subDict.items():
                    if k == "DEF%":
                        defense = v
                    elif k == "Crit Rate%":
                        rate = v
                    elif k == "Crit DMG%":
                        damage = v
                result = float(defense) + float(rate)*2 + float(damage)
            elif self.values[0] == "Energy Recharge build":
                for k, v in self.subDict.items():
                    if k == "Energy Recharge%":
                        charge = v
                    elif k == "Crit Rate%":
                        rate = v
                    elif k == "Crit DMG%":
                        damage = v
                result = float(charge) + float(rate)*2 + float(damage)
            elif self.values[0] == "Elemental Mastery build":
                for k, v in self.subDict.items():
                    if k == "Elemental Mastery":
                        mastery = v
                    elif k == "Crit Rate%":
                        rate = v
                    elif k == "Crit DMG%":
                        damage = v
                result = float(mastery) + float(rate)*2 + float(damage)
                result /= 2

            print(str(round(result, 1)))
            print(self.subDict)

            embed = Embed(title="Artifact score calculation results", color=0x1e90ff, description=f"score: **{str(round(result, 1))}**")
            for key, val in self.subDict.items():
                embed.add_field(name=f"**{key}**", value=val)
            await interaction.response.edit_message(content=None, view=None, embed=embed)
            print(f"executor:{interaction.user.name}\nartifact score - show results...")

        except:
            await interaction.response.edit_message(content="Error: The number entered may have been an incorrect number. Numerical values must be entered in single-byte alphanumeric characters to one decimal place.", view=None, embed=None)
            print(f"executor:{interaction.user.name}\nartifact score - Error")
            print(self.subDict)
            return

class Score(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="score", description="Calculate Artifact score by selecting build.")
    async def score(self, interaction: Interaction):
        await interaction.response.send_message(content="Select your Artifact types", view=ArtifactBaseSelectView())
        print(f"executor:{interaction.user.name}\ncommand - command activate")

async def setup(bot):
    await bot.add_cog(Score(bot), guilds=[Object(id=993066051417944064)])
