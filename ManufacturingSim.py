import simpy
import pandas as pd

class ManufacturingLine:
    def __init__(self, env):
        self.env = env
        self.loading = simpy.Resource(env, capacity=10)
        self.machining = simpy.Resource(env, capacity=10)
        self.assembly = simpy.Resource(env, capacity=5)
        self.unloading = simpy.Resource(env, capacity=5)
        self.inspection = simpy.Resource(env, capacity=3)
        self.packaging = simpy.Resource(env, capacity=2)
        self.shift_end = 8*60*60  # 8 hours in seconds
        
        # Data collection
        self.data = []

    def process(self, name, time):
        yield self.env.timeout(time)

    def log_process(self, name, process_name, start_time, end_time):
        self.data.append({
            'Product': name,
            'Process': process_name,
            'Start': start_time,
            'End': end_time,
            'Duration': end_time - start_time
        })
        print(f'{process_name} for {name} completed at {end_time}')

def process_with_logging(env, line, name, process_name, duration, resource):
    start_time = env.now
    with resource.request() as request:
        yield request
        yield env.process(line.process(name, duration))
    end_time = env.now
    line.log_process(name, process_name, start_time, end_time)

def loading_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Loading', 5*60, line.loading))

def machining_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Machining', 30*60, line.machining))

def assembly_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Assembly', 20*60, line.assembly))

def unloading_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Unloading', 5*60, line.unloading))

def inspection_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Inspection', 10*60, line.inspection))

def packaging_process(env, line, name):
    yield env.process(process_with_logging(env, line, name, 'Packaging', 15*60, line.packaging))

def production_process(env, line, name):
    """ Run the complete production process for a single product. """
    yield env.process(loading_process(env, line, name))
    yield env.process(machining_process(env, line, name))
    yield env.process(assembly_process(env, line, name))
    yield env.process(unloading_process(env, line, name))
    yield env.process(inspection_process(env, line, name))
    yield env.process(packaging_process(env, line, name))

def production_line(env, line):
    """ Generate products and process them continuously. """
    i = 0
    while env.now < line.shift_end:
        i += 1
        env.process(production_process(env, line, f'Product {i}'))
        # Wait a small time before starting the next product to avoid overlap
        yield env.timeout(1)  # 1 second delay between starting new products

# Create the environment and start the simulation
env = simpy.Environment()
line = ManufacturingLine(env)
env.process(production_line(env, line))
env.run(until=24*60*60)  # Run for 24 hours

# Convert collected data to a DataFrame for analysis
df = pd.DataFrame(line.data)

# Save the data to a CSV file (optional)
df.to_csv('manufacturing_line_data.csv', index=False)

# Display the DataFrame
print(df.head())
