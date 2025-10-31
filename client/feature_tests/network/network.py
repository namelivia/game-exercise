from engine.features.network.commands import SendNetworkRequest
from engine.features.network.worker import NetworkWorker
from engine.queue import QueueManager


def on_sucess(event, response):
    print("Success")
    print(event.__dict__)
    print(response.__dict__)


def on_error(event):
    print("Error")
    print(event.__dict__)


if __name__ == "__main__":
    QueueManager().initialize()
    network_thread = NetworkWorker(
        name="Network",
        queue=QueueManager().get("network"),
    )

    network_thread.start()
    SendNetworkRequest({"hello": "world"}, on_sucess, on_error).execute()
