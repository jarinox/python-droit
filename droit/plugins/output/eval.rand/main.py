import random

# Choose a random answer
# Example DDS v0.4: SRTX!danke->EVAL!rand.text(gerne, bitte)

def text(data, variables, db):
    rint = random.randint(0, len(data) - 1)
    return data[rint], variables, db
