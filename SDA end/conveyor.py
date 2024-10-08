class Conveyor:
    def __init__(self, velocity=0, length=0, width=0, position=0):
        """
        Constructor to initialize the Conveyor attributes.
        :param velocity: Speed of the conveyor (int)
        :param length: Length of the conveyor (int)
        :param width: Width of the conveyor (int)
        :param position: Current position of the conveyor (int)
        """
        self.velocity = velocity
        self.length = length
        self.width = width
        self.position = position

    def setVelocity(self, velocity):
        """
        Set the velocity of the conveyor.
        :param velocity: Speed to be set (int)
        """
        self.velocity = velocity

    def getLength(self):
        """
        Get the length of the physical conveyor.
        :return: Length of the conveyor (int)
        """
        return self.length

    def getWidth(self):
        """
        Get the width of the physical conveyor.
        :return: Width of the conveyor (int)
        """
        return self.width

    def setPosition(self, position):
        """
        Set the current position of the conveyor.
        :param position: Position to be set (int)
        """
        self.position = position

    def getLoadingPosition(self):
        """
        Get the loading position of the conveyor (might depend on business logic).
        :return: The loading position (int)
        """
        # Assuming the loading position is at the start of the conveyor
        return 0

    def goToEndPos(self):
        """
        Move the conveyor to the end position.
        :return: None
        """
        # Assuming the end position is equal to the length of the conveyor
        self.position = self.length
        print(f"Conveyor moved to end position: {self.position}")
