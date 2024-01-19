import random
import salabim as sim

from twinpy import *

colors = ["red", "orange", "green", "tomato", "olive", "gold", "indigo", "pink", "purple", "orchid", "teal", "brown"]

class RobotA(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0,   0,   0]
        joint_angles_b = [0, +45, +90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Move
            self.move_to(joint_angles_c, 2)
            # Pick
            self.state.set("pick")
            self.hold(1)
            # Create and attach
            product = Product(position_controller = self, color = colors[random.randint(0, len(colors) - 1)])
            # Move
            self.move_to(joint_angles_a, 2)
            # Idle
            while not conveyor1.empty_source.get():
                self.wait(conveyor1.empty_source)
            # Move
            self.move_to(joint_angles_b, 2)
            # Place
            self.state.set("place")
            self.hold(1)
            # Drop
            conveyor1.drop(product)
            # Move
            self.move_to(joint_angles_a, 2)

class RobotB(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0,   0,   0]
        joint_angles_b = [0, +45, +90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Idle
            self.state.set("idle")
            while conveyor1.empty_target.get():
                self.wait((conveyor1.empty_target, False))
            # Move
            self.move_to(joint_angles_c, 2)
            # Pick
            self.state.set("pick")
            self.hold(1)
            product = conveyor1.take()
            product.position_controller = self
            # Move
            self.move_to(joint_angles_a, 2)
            # Idle
            while not conveyor2.empty_source.get():
                self.wait(conveyor2.empty_source)
            # Move
            self.move_to(joint_angles_b, 2)
            # Place
            self.state.set("place")
            self.hold(1)
            # Drop
            conveyor2.drop(product)
            # Move
            self.move_to(joint_angles_a, 2)

class RobotC(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0,   0,   0]
        joint_angles_b = [0, +45, +90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Idle
            self.state.set("idle")
            while conveyor2.empty_target.get():
                self.wait((conveyor2.empty_target, False))
            # Move
            self.move_to(joint_angles_c, 2)
            # Pick
            self.state.set("pick")
            self.hold(1)
            product = conveyor2.take()
            product.position_controller = self
            # Move
            self.move_to(joint_angles_a, 2)
            # Idle
            while not conveyor3.empty_source.get():
                self.wait(conveyor3.empty_source)
            # Move
            self.move_to(joint_angles_b, 2)
            # Place
            self.state.set("place")
            self.hold(1)
            # Drop
            conveyor3.drop(product)
            # Move
            self.move_to(joint_angles_a, 2)

# Create simulation environment
env = sim.Environment()
env.modelname("Robotereinsatzplanung")

# Animation (2D)
env.animate(True)
# Window
env.width(1000)
env.height(600)
env.position((100, 100))
# Objects
sim.AnimateRectangle(
    spec = (0, 0, 1000, 100),
    text = "Floor",
    fillcolor = "lightgray",
    textcolor = "black",
    fontsize = 20
)
sim.AnimateRectangle(
    spec = (0, 500, 1000, 600),
    text = "Ceiling",
    fillcolor = "lightgray",
    textcolor = "black",
    fontsize = 20
)

# Define conveyors
conveyor1 = Conveyor(source_position = Vector(171, 150), target_position = Vector(329, 150))
conveyor2 = Conveyor(source_position = Vector(471, 150), target_position = Vector(629, 150))
conveyor3 = Conveyor(source_position = Vector(771, 150), target_position = Vector(929, 150))
# Define robots
robot1 = RobotA(base_position = Vector(100, 100), base_angle = 0)
robot2 = RobotB(base_position = Vector(400, 100), base_angle = 0)
robot3 = RobotC(base_position = Vector(700, 100), base_angle = 0)

# Start simulation with/without video production
if True:
    # Video production disabled
    env.run(sim.inf)
else:
    # Video production enabled
    env.video("test.mp4")
    env.run(till = 30)
    env.video_close()