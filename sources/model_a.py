import salabim as sim

from twinpy import *

class RobotA(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Move
            self.move_to(joint_angles_c, 2)
            # Pick
            self.state.set("pick")
            self.hold(1)
            # Create and attach
            product = Product(position_controller = self)
            # Move
            self.move_to(joint_angles_b, 4)
            # Idle
            while not conveyor1.empty_source.get():
                self.wait(conveyor1.empty_source)
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
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
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
            self.move_to(joint_angles_b, 4)
            # Idle
            while not conveyor2.empty_source.get():
                self.wait(conveyor2.empty_source)
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
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
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
            self.move_to(joint_angles_b, 4)
            # Idle
            while not conveyor3.empty_source.get():
                self.wait(conveyor3.empty_source)
            # Place
            self.state.set("place")
            self.hold(1)
            # Drop
            conveyor3.drop(product)
            # Move
            self.move_to(joint_angles_a, 2)

class RobotD(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Motion sequence
            self.move_to(joint_angles_b, 2)
            self.move_to(joint_angles_c, 4)
            self.move_to(joint_angles_a, 2)

class RobotE(Robot):
    def process(self):
        # Define target positions
        joint_angles_a = [0, 0, 0]
        joint_angles_b = [0, 45, 90]
        joint_angles_c = [0, -45, -90]
        # Process loop
        while True:
            # Move
            self.move_to(joint_angles_c, 2)
            # Pick
            self.state.set("pick")
            self.hold(1)
            # Create and attach
            product = Product(position_controller = self)
            # Move
            self.move_to(joint_angles_b, 4)
            # Place
            self.state.set("place")
            self.to_store(machine1.store_in, product)
            # Move
            self.move_to(joint_angles_a, 2)
            # Idle
            self.state.set("idle")
            product: Product = self.from_store(machine1.store_out)
            # Move
            self.move_to(joint_angles_b, 2)
            # Attach
            product.position_controller = self
            # Move
            self.move_to(joint_angles_c, 4)
            # Idle
            while not conveyor1.empty_source.get():
                self.wait(conveyor1.empty_source)
            # Place
            self.state.set("place")
            self.hold(1)
            # Drop
            conveyor1.drop(product)

# Create simulation environment
env = sim.Environment()
env.modelname("Robotereinsatzplanung")

# Setup 2D or 3D animation
if True:
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
else:
    # Animation (3D)
    env.animate3d(True)
    # Window
    env.width3d(800)
    nv.height3d(600)
    env.position3d((100, 100))
    # Objects
    sim.Animate3dGrid(x_range=range(-2, 2, 1), y_range=range(-2, 2, 1))

# Define conveyors
conveyor1 = Conveyor(source_position = Vector(100, 300), target_position = Vector(300, 300))
conveyor2 = Conveyor(source_position = Vector(400, 300), target_position = Vector(600, 300))
conveyor3 = Conveyor(source_position = Vector(700, 300), target_position = Vector(900, 300))
# Define machines
machine1 = Machine(position = Vector( 50, 300))
machine2 = Machine(position = Vector(350, 300))
machine3 = Machine(position = Vector(650, 300))
machine4 = Machine(position = Vector(950, 300))
# Define robots
robot1 = RobotA(base_position = Vector(200, 100), base_angle = 0)
robot2 = RobotB(base_position = Vector(500, 100), base_angle = 0)
robot3 = RobotC(base_position = Vector(800, 100), base_angle = 0)
robot4 = RobotD(base_position = Vector(200, 500), base_angle = 180)
robot5 = RobotD(base_position = Vector(500, 500), base_angle = 180)
robot6 = RobotD(base_position = Vector(800, 500), base_angle = 180)

# Start simulation with/without video production
if True:
    # Video production disabled
    env.run(sim.inf)
else:
    # Video production enabled
    env.video("test.mp4")
    env.run(till = 30)
    env.video_close()