"This script generates a single JSON file containing all the docs and metadata for connections."
from pathlib import Path
from subprocess import check_output

import json
import yaml

connections = {}
connections_dir = Path("connections")

# parse all .yml files in the connections directory and store them in `connections`
for path in connections_dir.glob("**/*.yml"):
    print(f"Loading connection from {path}")
    with open(path, mode="r", encoding="utf-8") as f:
        connection = yaml.safe_load(f)
        connection["file_path"] = str(path)

        # get the last commit date for the connection
        commit_date = check_output(
            f"git log -1 --pretty=format:%cI {path}".split()
        ).decode()
        connection["last_commit_date"] = commit_date

        # if there are any parameters with an example value, make sure the example value is a string
        for parameter in connection.get("parameters", []):
            if "example" in parameter:
                parameter["example"] = str(parameter["example"])

        connections[connection["id"]] = connection

print(f"Loaded {len(connections)} connections. Checking for inheritance...\n")

# then we need to deal with inheritance
for connection in connections.values():
    if "inherit_from" in connection:
        print(
            f"Connection {connection['id']} inherits from {connection['inherit_from']}"
        )

        # if this connection extends another connection, we need to merge the two
        # we do this by copying all the fields from the parent connection into the child connection
        parent = connections[connection["inherit_from"]]
        for key, value in parent.items():
            # if the key is `+parameters`, we need to merge the parameters. we do this later
            if key == "+parameters":
                continue

            # otherwise, we just copy the value from the parent connection
            if key not in connection:
                print(f"\tAdding {key} to {connection['id']}")
                connection[key] = value

        # if there's a `+parameters` field in the child connection, we need to merge it
        # with the parameters from the parent connection
        if "+parameters" in connection:
            print(f"\tMerging parameters from {connection['inherit_from']}")
            for parameter in connection["+parameters"]:
                # if the parameter is not already in the child connection by the
                # param's `airflow_param_name` and `in_extra`, we add it
                if not any(
                    [
                        p["airflow_param_name"] == parameter["airflow_param_name"]
                        and p.get("in_extra", False) == parameter.get("in_extra", False)
                        for p in connection["parameters"]
                    ]
                ):
                    print(
                        f"\t\tAdding parameter {parameter['airflow_param_name']} to {connection['id']}"
                    )
                    connection["parameters"].append(parameter)

            # then delete the `+parameters` field from the child connection
            print(f"\tRemoving `+parameters` from {connection['id']}")
            del connection["+parameters"]

        # and then we need to remove the `inherit_from` field from the child connection
        print(f"Removing `inherit_from` from {connection['id']}\n")
        del connection["inherit_from"]

print("Removing non-visible connections...")

# remove any non-visible connections
for connection in list(connections.values()):
    if not connection.get("visible", True):
        print(f"\tRemoving non-visible connection {connection['id']}")
        del connections[connection["id"]]

print("Done removing non-visible connections.\n")

# finally, we write the connections to a single JSON file
with open("connections.json", mode="w", encoding="utf-8") as f:
    print("Writing connections to connections.json")
    json.dump(list(connections.values()), f, indent=4)
