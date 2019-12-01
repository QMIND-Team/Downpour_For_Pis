'''
5 types of packets:

init W->S
worker notifies server that of its presence
{
	'type': 'init'
}

init_resp S->W
	The server will send this after a worker sends an init packet
	The server must send the worker the parameters of the current model
{
	'type': 'init_resp'
	'id': some kind of ID number
	'model': the model the server wishes the worker to train
}

push W->S
	The worker must extract parameters from its model and send it to the server
	The server must take these parameters and incorporate them into its model
{
	'type': 'push'
	'model': the output of a call to model.save()
}

pull W->S
	worker requests parameters from server
	The server must extract parameters from its model and send it to the worker
{
	'type': 'pull'
}

pull_resp S->W
	server sends worker parameters
{
	'type': 'pull_resp'
	'model': the output of a call to model.save()
}

'''