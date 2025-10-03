from client.engine.features.network.commands import SendNetworkRequest
from client.engine.features.network.worker import NetworkWorker
from client.engine.general_state.options import Options
from client.engine.general_state.queue import QueueManager


def on_sucess(response):
    print("Success")
    print(response)


def on_error(response):
    print("Error")
    print(response)


if __name__ == "__main__":
    QueueManager().initialize()
    Options().initialize()
    network_thread = NetworkWorker(
        name="Network",
        queue=QueueManager().get("network"),
    )

    network_thread.start()
    SendNetworkRequest({"hello": "world"}, on_sucess, on_error).execute()
