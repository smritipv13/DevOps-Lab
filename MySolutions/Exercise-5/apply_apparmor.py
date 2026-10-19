import docker

client = docker.from_env()

print("Building Docker image...")
client.images.build(path=".", tag="flask-apparmor")

print("Starting container with AppArmor profile...")
container = client.containers.run(
    "flask-apparmor",
    detach=True,
    ports={"5000/tcp": 5000},
    security_opt=["apparmor=my-apparmor-profile"]
)

container.reload()
print("Container:", container.name)
print("Security options:", container.attrs["HostConfig"]["SecurityOpt"])

input("Press Enter to stop the container...")
container.stop()
container.remove()
client.close()
print("Container stopped and removed.")
