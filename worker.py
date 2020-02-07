"""Worker"""

import json
import comms.client as client
from messages import Message, Init, Init_Response, Push, Fetch, Fetch_Response, Terminate

# TODO: Rename these functions to reflect what we're actually pushing and pulling.
# i.e. choose one of: push/pull_weights, push/pull_parameters, push/pull_gradients


def send_and_receive(message: Message, cl: client):
    """Prepare the message and send it through the client"""
    message_dict = message.__dict__
    message_json = json.dumps(message_dict)
    response = cl.send(message_json)
    # Determine the type of message and bring it back to an object
    resp_dict = json.loads(response)
    if resp_dict["type"] == "init_resp":
        response = Init_Response(resp_dict)
    elif resp_dict["type"] == "fetch_resp":
        response = Fetch_Response(resp_dict)
    elif resp_dict["type"] == "terminate":
        response = Terminate(resp_dict)
    else:
        raise TypeError("Didn't receive a known message type")
    return response



def push_weights(model, cl: client):
    """Push *thing* up to manager"""
    message = Push()
    # Model.save
    message.weights = "whatever"
    response = send_and_receive(message, cl)
    if response.type == "terminate":
        return False
    return True



def pull_parameters(model, cl: client):
    """Pull *things* from manager"""
    message = Fetch()
    response = send_and_receive(message, cl)

    if response.type == "terminate":
        return False

    # Check the response type
    # Update parameters or gradients or whatever

    return True


def do_ml(model, cl: client):
    while True:
        # do machine learning
        # the downpour stuff yeah

        # When it's time
        if not push_weights(model, cl):
            # Allow for early exits
            break

        # When it's time
        if not pull_parameters(model, cl):
            # Early exit
            break

        # And we're done
        break



def initialize_model(Init_Response: Init_Response):
    # Do the stuff to initialize the model

    model = "Keras Model"   # Make the model

    return model



def main():
    """Main Method"""
    # Initialize
    cl = client.Client()

    init = Init()

    init_response = None
    while init_response is None:
        init_response = send_and_receive(init, cl)

    print(init_response)

    # Connected

    model = initialize_model(init_response)

    # Ready, time to do Downpour

    do_ml(model, cl)

    # We're done
    # Print out the model or write it to a file or do a prediction or something



if __name__ == "__main__":
    main()
