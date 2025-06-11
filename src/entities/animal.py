class Animal:
    """
    Reprezentuje zwierzę w grze.

    Atrybuty:
        static_asset (Asset): Statyczna wizualna reprezentacja zwierzęcia.
        animated_asset (Asset, optional): Animowana wizualna reprezentacja zwierzęcia.
        current_asset (Asset): Aktualnie aktywna wizualna reprezentacja zwierzęcia.
        name (str): Nazwa zwierzęcia.
        age (int): Wiek zwierzęcia.
        hunger_level (float): Poziom głodu zwierzęcia, w zakresie od 0 do 100.
        boredom_level (float): Poziom znudzenia zwierzęcia, w zakresie od 0 do 100.
        """
    def __init__(self, static_asset, animated_asset=None, name="none", age=0):
        self.static_asset = static_asset
        self.animated_asset = animated_asset
        self.current_asset = static_asset
        self.name = name
        self.age = age
        self.hunger_level = 100.0
        self.boredom_level = 100.0

    def use_static_asset(self):
        """
            Przełącza aktualny zasób na statyczną wizualną reprezentację.
        """
        self.current_asset = self.static_asset

    def use_animated_asset(self):
        """
            Przełącza aktualny zasób na animowaną wizualną reprezentację, jeśli jest dostępna.
        """
        if self.animated_asset:
            self.current_asset = self.animated_asset
