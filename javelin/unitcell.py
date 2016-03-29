import numpy as np


class UnitCell(object):
    def __init__(self, *args):
        self.a = 1
        self.b = 1
        self.c = 1
        self.alpha = np.radians(90)
        self.beta = np.radians(90)
        self.gamma = np.radians(90)
        self.ra = 1  # a*
        self.rb = 1  # b*
        self.rc = 1  # c*
        self.ralpha = np.radians(90)  # alpha*
        self.rbeta = np.radians(90)   # beta*
        self.rgamma = np.radians(90)  # gamma*
        self.__G = np.matrix(np.eye(3))
        self.__Gstar = np.matrix(np.eye(3))
        if args:
            self.set_cell(args)

    def set_cell(self, *args):
        args = np.asarray(args).flatten()
        if args.size == 1:  # cubic
            self.a = self.b = self.c = np.float(args)
            self.alpha = self.beta = self.gamma = np.radians(90)
        elif args.size == 3:  # orthorhombic
            self.a = np.float(args[0])
            self.b = np.float(args[1])
            self.c = np.float(args[2])
            self.alpha = self.beta = self.gamma = np.radians(90)
        elif args.size == 6:
            self.a = np.float(args[0])
            self.b = np.float(args[1])
            self.c = np.float(args[2])
            self.alpha = np.radians(args[3])
            self.beta = np.radians(args[4])
            self.gamma = np.radians(args[5])
        else:
            raise ValueError("Invalid number of variables, unit cell unchanged")
        self.__calculateG()
        self.__calculateReciprocalLattice()

    def get_cell(self):
        return (self.a, self.b, self.c,
                np.degrees(self.alpha),
                np.degrees(self.beta),
                np.degrees(self.gamma))

    cell = property(get_cell, set_cell)

    def get_G(self):
        return self.__G

    def get_Gstar(self):
        return self.__G.getI()

    def get_ReciprocalCell(self):
        return (self.ra, self.rb, self.rc,
                np.degrees(self.ralpha),
                np.degrees(self.rbeta),
                np.degrees(self.rgamma))

    def __calculateReciprocalLattice(self):
        Gstar = self.get_Gstar()
        self.ra = np.sqrt(Gstar[0, 0])
        self.rb = np.sqrt(Gstar[1, 1])
        self.rc = np.sqrt(Gstar[2, 2])
        self.ralpha = np.arccos(Gstar[1, 2] / (self.rb*self.rc))
        self.rbeta = np.arccos(Gstar[0, 2] / (self.ra*self.rc))
        self.rgamma = np.arccos(Gstar[0, 1] / (self.ra*self.rb))

    def __calculateG(self):
        if ((self.alpha > self.beta + self.gamma) or
                (self.beta > self.alpha + self.gamma) or
                (self.gamma > self.alpha + self.beta)):
            raise ValueError("Invalid angles")
        self.__G[0, 0] = self.a**2
        self.__G[1, 1] = self.b**2
        self.__G[2, 2] = self.c**2
        self.__G[0, 1] = self.a * self.b * np.cos(self.gamma)
        self.__G[0, 2] = self.a * self.c * np.cos(self.beta)
        self.__G[1, 2] = self.b * self.c * np.cos(self.alpha)
        self.__G[1, 0] = self.__G[0, 1]
        self.__G[2, 0] = self.__G[0, 2]
        self.__G[2, 1] = self.__G[1, 2]