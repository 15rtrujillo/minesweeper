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
        if not self.swept():
            self.status = Tile.SWEPT


    def flag(self) -> int:
        """If the tile is unflagged, it will be marked as flagged and vice-versa
        Returns -1 if the tile was flagged, 1 if the tile was unflagged, or 0 if nothing changed"""
        if self.flagged():
            self.status = Tile.UNSWEPT
            return 1
        elif self.swept():
            return 0
        else:
            self.status = Tile.FLAGGED
            return -1
        

    def swept(self) -> bool:
        """Returns true if the tile has been swept, false otherwise"""
        return self.status == Tile.SWEPT
    

    def flagged(self) -> bool:
        """Returns true if the tile has been flagged, false otherwise"""
        return self.status == Tile.FLAGGED