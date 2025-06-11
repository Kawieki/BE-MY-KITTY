class Animal:
    """
       Reprezentuje zwierzę w grze.

       Atrybuty:
           static_asset (Asset): Statyczny zasób graficzny zwierzęcia.
           animated_asset (Asset): Animowany zasób graficzny zwierzęcia (opcjonalny).
           current_asset (Asset): Aktualnie używany zasób graficzny zwierzęcia.
           name (str): Nazwa zwierzęcia.
           age (int): Wiek zwierzęcia.
           hunger_level (float): Poziom głodu zwierzęcia (od 0 do 100).
           boredom_level (float): Poziom znudzenia zwierzęcia (od 0 do 100).
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
        Ustawia statyczny zasób graficzny jako aktualny zasób zwierzęcia.
        """
        self.current_asset = self.static_asset

    def use_animated_asset(self):
        """
        Ustawia animowany zasób graficzny jako aktualny zasób zwierzęcia,
        jeśli animowany zasób jest dostępny.
        """
        if self.animated_asset:
            self.current_asset = self.animated_asset
