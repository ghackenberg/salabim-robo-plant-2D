import salabim as sim

class Conveyor(sim.Component):

    from .vector import Vector
    from .product import Product

    def setup(self, source_position: Vector, target_position: Vector):

        from .product import Product

        # Positions
        self.source_position = source_position
        self.target_position = target_position

        # Distance
        self.distance = source_position.substract(target_position).length()

        # Direction
        self.direction = self.target_position.substract(self.source_position).normalize()

        # Speed
        self.speed_default = 10
        self.speed_current = 0

        # States
        self.empty = sim.State(name = "empty", value = True)
        self.empty_source = sim.State(name = "empty_source", value = True)
        self.empty_target = sim.State(name = "empty_target", value = True)

        # Products
        self.products: list[Product] = []
        self.product_distances: dict[Product, float] = {}
        self.product_distance_times: dict[Product, float] = {}

        # Line
        self.line = sim.AnimateLine(
            spec = [source_position.x, source_position.y, target_position.x, target_position.y],
            linecolor = "black",
            linewidth = 2
        )
    
    def calculate_product_position(self, product: Product, time: float):

        product_distance = self.product_distances[product]
        product_distance_time = self.product_distance_times[product]

        delta = time - product_distance_time
        
        return self.source_position.add(self.direction.mulitply(product_distance + delta * self.speed_current))
    
    def update(self):

        # Initialize empty state values
        empty = len(self.products) == 0
        empty_source = True
        empty_target = True

        # Update distances and distance times
        for product in self.products:
            # Read previous distance and time
            product_distance = self.product_distances[product]
            product_distance_time = self.product_distance_times[product]
            # Calculate current distance and time
            current_product_distance = product_distance + (self.env.now() - product_distance_time) * self.speed_current
            current_product_time = self.env.now()
            # Write current distance and time
            self.product_distances[product] = current_product_distance
            self.product_distance_times[product] = current_product_time
            # Update empty state values
            empty_source = empty_source and current_product_distance > 14.9
            empty_target = empty_target and current_product_distance < self.distance - 0.1

        # Update empty states
        self.empty.set(empty)
        self.empty_source.set(empty_source)
        self.empty_target.set(empty_target)
    
    def drop(self, product: Product):
        
        # Set product position controller
        product.position_controller = self

        # Update product members
        self.products.append(product)
        self.product_distances[product] = 0
        self.product_distance_times[product] = self.env.now()

        # Update state and restart process
        self.update()
        self.cancel()
        self.activate()
    
    def take(self):

        # Update product members
        product = self.products.pop(0)
        self.product_distances.pop(product)
        self.product_distance_times.pop(product)

        # Update state and restart process
        self.update()
        self.cancel()
        self.activate()

        # Return product
        return product
    
    def process(self):

        # Process loop
        while True:

            # Wait for product at the source place
            while self.empty.get():
                self.wait((self.empty, False))
            
            # Update current speed
            self.speed_current = self.speed_default

            # Calculate time of next event
            time = sim.inf

            # Iterate through products
            for product in self.products:
                # Get travelled distance
                product_distance_now = self.product_distances[product]
                # Calculate next interesting distance
                product_distance_next = 15 if product_distance_now < 14.9 else self.distance
                # Calculate time to next interesting distance
                product_time = (product_distance_next - product_distance_now) / self.speed_current
                # Update time
                time = min(time, product_time)
            
            # Wait for the calculated amount of time
            self.hold(time)

            # Update state
            self.update()
            
            # Update current speed
            self.speed_current = 0

            # Wait for target place to become empty
            while not self.empty_target.get():
                self.wait(self.empty_target)