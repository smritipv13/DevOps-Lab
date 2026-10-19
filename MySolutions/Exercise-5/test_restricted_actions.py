import docker
import time

client = docker.from_env()
container = None

try:
    print("Starting container with AppArmor profile...")

    container = client.containers.run(
        "flask-apparmor",
        detach=True,
        security_opt=["apparmor=my-apparmor-profile"]
    )

    time.sleep(2)
    container.reload()

    if container.status != "running":
        print("Container exited before testing.")
        print(container.logs().decode(errors="replace"))
    else:
        tests = [
            ["cat", "/etc/passwd"],
            ["/usr/bin/bash", "-c", "echo Bash executed"]
        ]

        for command in tests:
            print(f"\nTesting: {command}")

            try:
                result = container.exec_run(command)
                print("Exit code:", result.exit_code)
                print("Output:", result.output.decode(errors="replace"))
            except docker.errors.APIError as error:
                print("Execution failed:", error)

finally:
    if container is not None:
        try:
            container.stop(timeout=2)
        except docker.errors.APIError:
            pass
        try:
            container.remove(force=True)
        except docker.errors.APIError:
            pass

    client.close()
    print("\nContainer cleanup complete.")
