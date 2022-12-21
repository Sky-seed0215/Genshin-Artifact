import datetime
from discord import app_commands, SelectOption, Interaction, TextStyle, Embed, Object
from discord.ext import commands
from discord.ui import View, Select, Modal, TextInput

dt_now = datetime.datetime.now()

mainOp = {
    "生の花": ["HP"],
    "死の羽": ["攻撃力"],
    "時の砂": ["HP%", "攻撃力%", "防御力%", "元素熟知", "元素チャージ効率"],
    "空の杯": ["HP%", "攻撃力%", "防御力%", "元素熟知", "元素ダメージバフ"],
    "理の冠": ["HP%", "攻撃力%", "防御力%", "元素熟知", "与える治癒効果%", "会心率", "会心ダメージ"]
}

subOp = [
    "攻撃力",
    "攻撃力%",
    "防御力",
    "防御力%",
    "HP",
    "HP%",
    "元素熟知",
    "元素チャージ効率",
    "会心率",
    "会心ダメージ"
]

class ArtifactBaseSelectView(View):
    def __init__(self):
        super().__init__(timeout=90)
        self.add_item(ArtifactBaseSelect())


class ArtifactBaseSelect(Select):
    def __init__(self):
        options = []
        options.append(SelectOption(label="生の花", emoji="<:PaleFlameStainlessBloom:1054994317300740216>", description="HP"))
        options.append(SelectOption(label="死の羽", emoji="<:PaleFlameWiseDoctorsPinion:1054994302478057482>", description="攻撃力"))
        options.append(SelectOption(label="時の砂", emoji="<:PaleFlameMomentofCessation:1054994289588981770>", description=",".join(mainOp["時の砂"])))
        options.append(SelectOption(label="空の杯", emoji="<:PaleFlameSurpassingCup:1054994275915534366>", description=",".join(mainOp["空の杯"])))
        options.append(SelectOption(label="理の冠", emoji="<:PaleFlameMockingMask:1054994253190807552>", description=",".join(mainOp["理の冠"])))

        super().__init__(placeholder="聖遺物を選んでください", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        view = View()
        view.add_item(ArtifactSuboptionSelect(self.values[0]))
        await interaction.response.edit_message(content="サブオプションを選んでください", view=view)

class ArtifactSuboptionSelect(Select):
    def __init__(self, mainType: str):
            self.listSubOption: list[SelectOption] = []
            self.mainType = mainType
            for v in subOp:
                self.listSubOption.append(SelectOption(label=v))
            super().__init__(placeholder="サブオプションを選択 ※最高4つまで選択できます", max_values=4, options=self.listSubOption)

    async def callback(self, interaction: Interaction):
        result = []
        for n in self.values:
            result.append(n)
        await interaction.response.send_modal(ArtifactSuboptionValueModal(result, self.mainType))
        print(f"executor:{interaction.user.name}\nartifact - select sub option...")

class ArtifactSuboptionValueModal(Modal):
    def __init__(self, list: list, mainType: str):
        super().__init__(title="数値を入力してください", timeout=300)
        self.list = list
        self.mainType = mainType

        try:
            self.contentA = TextInput(
                label=f"{self.list[0]}",
                style=TextStyle.short,
                placeholder=f"{self.list[0]}の数値",
                required=True
            )
            self.add_item(self.contentA)
        except:
            pass
        try:
            self.contentB = TextInput(
                label=f"{self.list[1]}",
                style=TextStyle.short,
                placeholder=f"{self.list[1]}の数値",
                required=True
            )
            self.add_item(self.contentB)
        except:
            pass
        try:
            self.contentC = TextInput(
                label=f"{self.list[2]}",
                style=TextStyle.short,
                placeholder=f"{self.list[2]}の数値",
                required=True
            )
            self.add_item(self.contentC)
        except:
            pass
        try:
            self.contentD = TextInput(
                label=f"{self.list[3]}",
                style=TextStyle.short,
                placeholder=f"{self.list[3]}の数値",
                required=True
            )
            self.add_item(self.contentD)
        except:
            pass

    async def on_submit(self, interaction: Interaction):
        result = {}
        try:
            result[self.list[0]] = self.contentA.value
        except:
            pass
        try:
            result[self.list[1]] = self.contentB.value
        except:
            pass
        try:
            result[self.list[2]] = self.contentC.value
        except:
            pass
        try:
            result[self.list[3]] = self.contentD.value
        except:
            pass

        view = View()
        view.add_item(ArtifactScoreSelectView(result, self.mainType))

        await interaction.response.edit_message(content="スコアの計算方式を選択してください", view=view)

class ArtifactScoreSelectView(Select):
    def __init__(self, resultDict: dict, mainType: str):
        options = []
        self.mainType = mainType
        self.subDict = resultDict
        options.append(SelectOption(label="会心ビルド", description=r"攻撃力%+会心率×2+会心ダメージ"))
        options.append(SelectOption(label="HPビルド", description=r"HP%+会心率×2+会心ダメージ"))
        options.append(SelectOption(label="防御力ビルド", description=r"防御力%+会心率×2+会心ダメージ"))
        options.append(SelectOption(label="元素チャージ効率ビルド", description=r"元素チャージ効率+会心率×2+会心ダメージ"))
        options.append(SelectOption(label="元素熟知ビルド", description=r"(元素熟知+会心率×2+会心ダメージ)÷2"))

        super().__init__(placeholder="選択してください", options=options)

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

            if self.values[0] == "会心ビルド":
                for k, v in self.subDict.items():
                    if k == "攻撃力%":
                        attack = v
                    elif k == "会心率":
                        rate = v
                    elif k == "会心ダメージ":
                        damage = v
                result = float(attack) + float(rate)*2 + float(damage)
            elif self.values[0] == "HPビルド":
                for k, v in self.subDict.items():
                    if k == "HP%":
                        hp = v
                    elif k == "会心率":
                        rate = v
                    elif k == "会心ダメージ":
                        damage = v
                result = float(hp) + float(rate)*2 + float(damage)
            elif self.values[0] == "防御力ビルド":
                for k, v in self.subDict.items():
                    if k == "防御力%":
                        defense = v
                    elif k == "会心率":
                        rate = v
                    elif k == "会心ダメージ":
                        damage = v
                result = float(defense) + float(rate)*2 + float(damage)
            elif self.values[0] == "元素チャージ効率ビルド":
                for k, v in self.subDict.items():
                    if k == "元素チャージ効率":
                        charge = v
                    elif k == "会心率":
                        rate = v
                    elif k == "会心ダメージ":
                        damage = v
                result = float(charge) + float(rate)*2 + float(damage)
            elif self.values[0] == "元素熟知ビルド":
                for k, v in self.subDict.items():
                    if k == "元素熟知":
                        mastery = v
                    elif k == "会心率":
                        rate = v
                    elif k == "会心ダメージ":
                        damage = v
                result = float(mastery) + float(rate)*2 + float(damage)
                result /= 2

            print(str(round(result, 1)))
            print(self.subDict)

            r_value = ["攻撃力", "防御力", "HP", "元素熟知"]
            embed = Embed(title="聖遺物スコア", color=0x1e90ff, description=f"**{self.mainType}**\nスコア: **{str(round(result, 1))}**")
            embed.set_footer(text=f"{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}/{self.values[0]}")
            for key, val in self.subDict.items():
                if key not in r_value:
                    embed.add_field(name=f"**{key}**", value=f"{val}%")
                else:
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

    @app_commands.command(name="score", description="聖遺物スコアをビルド選択方式で算出します。")
    async def score(self, interaction: Interaction):
        await interaction.response.send_message(content="聖遺物のタイプを選択してください", view=ArtifactBaseSelectView())
        print(f"executor:{interaction.user.name}\ncommand - command activate")


async def setup(bot):
    await bot.add_cog(Score(bot), guilds=[Object(id=993066051417944064)])
