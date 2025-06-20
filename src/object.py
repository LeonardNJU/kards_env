class Object:
    def __init__(self, name:str, HP:int):
        """Initialize an object with a name and hit points (HP).

        Args:
            name (str): The name of the object.
            HP (int): The hit points of the object.
        """
        self.name = name
        self.HP = HP
    def take_damage(self, damage:int) -> int:
        """Reduce the object's HP by the specified damage amount.

        Args:
            damage (int): The amount of damage to apply.
        Returns:
            int: The remaining HP after taking damage. If HP falls below 0, it is set to 0.
        """
        self.HP -= damage
        self.HP = max(self.HP, 0)
        return self.HP
    
    def __str__(self) -> str:
        return f"[{self.name}({self.HP})]"