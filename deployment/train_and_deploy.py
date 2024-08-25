from rug import RUG

def train_and_deploy(train_data, validation_data):
    model = RUG(train_data, validation_data)
    model.train()
    model.deploy()

if __name__ == "__main__":
    # Load your train_data and validation_data
    train_data = ...
    validation_data = ...
    train_and_deploy(train_data, validation_data)