class Element:

    color = "#ffffff"
    name = "defaultName"

    def __init__(self, name: str) -> None:
        self.name = name


elements = [Element("This"), Element("is"), Element("ScriptFrame")]
