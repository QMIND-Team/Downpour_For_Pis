import client as cli

if __name__ == '__main__':
    model = 'weights and biases'
    status = cli.send(model, "localhost")
    print(status)
    print("done")