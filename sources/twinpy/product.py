import salabim as sim

class Product(sim.Component):
    def setup(self, position_controller, color = "red"):
        # Position
        self.position_controller = position_controller
        # State
        self.state = sim.State("state")
        # Rectangle
        self.rectangle = sim.AnimateRectangle(
            spec = lambda t: self.calculate_rectangle_spec(t),
            text = "P",
            fillcolor = color,
            textcolor = "white"
        )
    
    def calculate_rectangle_spec(self, time: float):

        from .conveyor import Conveyor
        from .machine import Machine
        from .robot import Robot
        from .vector import Vector

        if isinstance(self.position_controller, Robot):
            x = self.position_controller.calculate_joint_circle_x(3, time)
            y = self.position_controller.calculate_joint_circle_y(3, time)

        elif isinstance(self.position_controller, Machine):
            x = self.position_controller.position.x
            y = self.position_controller.position.y

        elif isinstance(self.position_controller, Conveyor):
            position = self.position_controller.calculate_product_position(self, time)
            x = position.x
            y = position.y

        elif isinstance(self.position_controller, Vector):
            x = self.position_controller.x
            y = self.position_controller.y

        return [x - 10, y - 10, x + 10, y + 10]

    def process(self):
        pass