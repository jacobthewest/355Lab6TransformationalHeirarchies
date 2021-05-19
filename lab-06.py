from gl_base import Renderer
import numpy as np

class Lab6Renderer(Renderer):
    title = "Lab 6: Hierarchical Transformations"

    xpos = 0
    ypos = 0
    zpos = -25
    theta = 0
    ortho = False
    carx = -20
    cary = -4
    carz = -15
    wheely = -3
    wheelOffsetWidth = 2.5
    wheelOffsetLength = 2
    tireAngle = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def poll_keys(self):
        if self.key_pressed[self.keys.A]:  # Move left
            self.xpos -= np.cos(self.theta) * 0.2
            self.zpos -= np.sin(self.theta) * 0.2
        elif self.key_pressed[self.keys.D]:  # Move right
            self.xpos += np.cos(self.theta) * 0.2
            self.zpos += np.sin(self.theta) * 0.2
        elif self.key_pressed[self.keys.S]:  # Move back
            self.zpos -= 0.2
            self.xpos += 0.2
        elif self.key_pressed[self.keys.W]:  # Move forward
            self.zpos += 0.2
            self.xpos -= 0.2
        elif self.key_pressed[self.keys.Q]:  # Turn left
            self.theta += 0.05
        elif self.key_pressed[self.keys.E]:  # Turn right
            self.theta -= 0.05
        elif self.key_pressed[self.keys.R]:  # Move up
            self.ypos += 0.1
        elif self.key_pressed[self.keys.F]:  # Move down
            self.ypos -= 0.1
        elif self.key_pressed[self.keys.P]:  # perspective mode
            self.ortho = False
        elif self.key_pressed[self.keys.O]:  # orthographic mode
            self.ortho = True
        elif self.key_pressed[self.keys.H]:  # return home
            self.xpos = 0
            self.ypos = 0
            self.zpos = -25
            self.theta = 0
            self.tireAngle = 0
            self.carx = -20


    def get_projection(self):  # Gets the projection matrix

        if (self.ortho):  # Return the orthographic projection
            projection = np.array([[1 / 10, 0, 0, 0],
                                   [0, 1 / 10, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 1]])
        else:  # Return the perspective projection
            projection = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 1, 0]])
        return np.transpose(projection)

    def get_view(self):  # Gets the view matrix
        theta = self.theta
        translation = np.array([[1, 0, 0, -self.xpos],
                                [0, 1, 0, -self.ypos],
                                [0, 0, 1, -self.zpos],
                                [0, 0, 0, 1]])
        rotation = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                             [0, 1, 0, 0],
                             [-np.sin(theta), 0, np.cos(theta), 0],
                             [0, 0, 0, 1]])
        transform = np.matmul(rotation, translation)
        return np.transpose(transform)

    def drawHouse(self, xOffset, zOffset, rotationAngle=None):
        translation = np.array([[1, 0, 0, xOffset],
                              [0, 1, 0, 0],
                              [0, 0, 1, zOffset],
                              [0, 0, 0, 1]])
        if not rotationAngle:
            finalView = translation
        else:
            rotation = np.array([[np.cos(rotationAngle), 0, np.sin(rotationAngle), 0],
                             [0, 1, 0, 0],
                             [-np.sin(rotationAngle), 0, np.cos(rotationAngle), 0],
                             [0, 0, 0, 1]])
            finalView = np.matmul(translation, rotation)

        self.push_model_matrix(np.transpose(finalView))
        self.house.render(self.get_model_matrix(), color=np.array([255, 0, 0]))
        self.pop_model_matrix()

    def drawHouses(self):
        #self.drawHouse(xOffset, zOffset, rotationAngle=None)
        self.drawHouse(0, 0, 9.4) # Main House
        self.drawHouse(20, 0, 9.4)  # Right House
        self.drawHouse(-20, 0, 9.4)  # Left House
        self.drawHouse(-40, -20, 39.3)  # End House
        self.drawHouse(-20, -40)  # Back Left House
        self.drawHouse(0, -40)  # Back House
        self.drawHouse(20, -40)  # Back Right House

    def drawTire(self, wheelWidthOffset, wheelLengthOffset):
        tireTranslation = np.array([[1, 0, 0, wheelLengthOffset],
                                    [0, 1, 0, self.wheely],
                                    [0, 0, 1, wheelWidthOffset],
                                    [0, 0, 0, 1]])
        tireRotation = np.array([[np.cos(-self.tireAngle), -np.sin(-self.tireAngle), 0, 0],
                                 [np.sin(-self.tireAngle), np.cos(-self.tireAngle), 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])
        combo = np.matmul(tireTranslation, tireRotation)
        self.push_model_matrix(np.transpose(combo))
        self.tire.render(self.get_model_matrix(), color=np.array([0, 0, 255]))
        self.pop_model_matrix()

    def drawTires(self):
        frontTiresLengthOffset = self.carx + self.wheelOffsetLength
        backTiresLengthOffset = self.carx - self.wheelOffsetLength
        leftWheelsWidthOffset = self.carz - self.wheelOffsetWidth
        rightWheelsWidthOffset = self.carz + self.wheelOffsetWidth
        # Front left tire
        self.drawTire(leftWheelsWidthOffset, frontTiresLengthOffset)
        # Front right tire
        self.drawTire(rightWheelsWidthOffset, frontTiresLengthOffset)
        # Back left tire
        self.drawTire(leftWheelsWidthOffset, backTiresLengthOffset)
        # Back right tire
        self.drawTire(rightWheelsWidthOffset, backTiresLengthOffset)


    def drawCar(self):
        carTranslation = np.array([[1, 0, 0, self.carx],
                                  [0, 1, 0, self.cary],
                                  [0, 0, 1, self.carz],
                                  [0, 0, 0, 1]])
        self.push_model_matrix(np.transpose(carTranslation))
        self.car.render(self.get_model_matrix(), color=np.array([0,255,0]))
        self.pop_model_matrix()
        self.drawTires()


    def render_scene(self, delta_time):
        self.drawHouses()
        self.drawCar()
        self.carx += 0.05
        self.tireAngle += 0.05



if __name__ == "__main__":
    Lab6Renderer.run()

