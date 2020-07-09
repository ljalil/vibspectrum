import math

class Bearing:
    """Bearing
    ======
    Tools for bearings vibration analysis.

    Parameters:
    ----------
    rpm : int or float
        number of revolutions per minute for the rotating shaft on which the bearing is mounted
    inner_diameter : float
        inner diameter of the bearing, in mm
    outer_diameter : float
        outer diameter of the bearing, in mm
    balls_number : int
        number of rolling elements, in the bearing
    ball_diameter : float
        diameter of rolling elementi, in mm
    contact_angle : float
        angle between a plane perpendicular to the bearing axis and a line joining the two contact points between the ball and outer raceway, in degrees
    """

    def __init__(self, rpm = 0, inner_diameter = 0, outer_diameter = 0, ball_diameter = 0, balls_number = 0, contact_angle = 0):

        if inner_diameter < 0 or outer_diameter < 0 or ball_diameter < 0:
            raise ValueError("Diameters can't have negative values")

        if inner_diameter > outer_diameter:
            raise ValueError("Inner diameter can't be larger than outer diameter")

        if balls_number < 0:
            raise ValueError("Rolling elements number can't be negative")

        self.rpm            =   rpm
        self.inner_diameter  =   inner_diameter
        self.outer_diameter  =   outer_diameter
        self.balls_number    =   balls_number
        self.ball_diameter   =   ball_diameter
        self.contact_angle   =   contact_angle

    def bpfo(self):
        """Ball Pass Frequency Outer (BPFO) or outer race fault frequency"""
        self.bpfo = self.rpm * (self.balls_number / 2) * ( 1 - (self.ball_diameter / ((self.inner_diameter + self.outer_diameter) /2)) * math.cos(self.contact_angle) )
        return self.bpfo

    def bpfi(self):
        """Ball Pass Frequency Inner (BPFI) or inner race fault frequeny"""
        self.bpfi = self.rpm * (self.balls_number / 2) * (1 + (self.ball_diameter / ((self.inner_diameter + self.outer_diameter) /2)) * math.cos(self.contact_angle))
        return self.bpfi

    def bsf(self):
        """Ball Spin Frequency (BSF) or rolling element fault frequency"""
        self.bsf = self.rpm * (((self.inner_diameter + self.outer_diameter) /2) / self.ball_diameter) * (1 - math.pow((self.ball_diameter/((self.inner_diameter + self.outer_diameter) /2))*math.cos(self.contact_angle),2))
        return self.bsf

    def ftf(self):
        """Fundamental Train Frequency (FTF)"""
        self.ftf = self.rpm * (1/2) * (1 - (self.ball_diameter / ((self.inner_diameter + self.outer_diameter) /2)) * math.cos(self.contact_angle))
        return self.ftf
