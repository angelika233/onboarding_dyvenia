from prefect import task, Flow

@task
def Hello_world():
    print("Hello world")
    return "Hello world"

def Prefect_say( string):
    print(string)

with Flow ("First flow") as f:
    r = Hello_world
    s = Prefect_say(r)

f.run()
f.visualize()