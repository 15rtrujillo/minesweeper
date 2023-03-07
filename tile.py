class Tile:
    """Holds information about a specific tile in a Minesweeper board"""

    # Tile status
    UNSWEPT = 0
    SWEPT = 1
    FLAGGED = 2


    def __init__(self, value):
        """Create a new tile
        value: The value of the tile. 'M' for mines or a number relating how many adjacent tiles have mines"""
        self.value = value
        self.status = Tile.UNSWEPT


    def sweep(self):
        """Attempt to mark the tile as swept. Returns true if successful"""
        if self.status == Tile.UNSWEPT or self.status == Tile.FLAGGED:
            self.status = Tile.SWEPT


    def flag(self):
        """If the tile is unflagged, it will be marked as flagged and vice-versa"""
        if self.status == Tile.UNSWEPT:
            self.status = Tile.FLAGGED
        elif self.status == Tile.FLAGGED:
            self.status = Tile.UNSWEPT