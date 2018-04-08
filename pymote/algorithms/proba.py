from pymote.algorithm import NodeAlgorithm
from pymote.message import Message


class Komunikacija(NodeAlgorithm):
	required_params = ('informationKey',)
	default_params = {'neighborsKey': 'Neighbors'}

	def initializer(self):
		ini_nodes = []
		for node in self.network.nodes():
			node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
			node.status = 'IDLE'
			node.memory['Izmjereno'] = node.compositeSensor.read()['Izmjereno']
			if self.informationKey in node.memory:
				node.status = 'INITIATOR'
				node.memory['MaxTemp'] = node.memory['Izmjereno']
				ini_nodes.append(node)
		for ini_node in ini_nodes:
			self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI, destination=ini_node))

	def initiator(self, node, message):
		if message.header == NodeAlgorithm.INI:
			node.send(Message(header='Information', data=node.memory[self.informationKey]))
			node.status = 'IDLE'

	def idle(self, node, message):
		if message.header == 'Information':
			if (message.data > node.memory['MaxTemp']):
				node.memory['MaxTemp'] = message.data
				destination_nodes = list(node.memory[self.neighborsKey])
				destination_nodes.remove(message.source)
				#print (destination_nodes)
				if destination_nodes:
					node.send(Message(destination=destination_nodes, header='Information', data=message.data))

	STATUS = {
            'INITIATOR': initiator,
            'IDLE': idle,
            }

            
class Komunikacija_v2(NodeAlgorithm):
	required_params = ('informationKey',)
	default_params = {'neighborsKey': 'Neighbors'}

	def initializer(self):
		ini_nodes = []
		brojac = 1
		br_ini = 3
		pom_var = len(self.network.nodes())
		for node in self.network.nodes():
			node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
			node.status = 'IDLE'
			node.memory['Izmjereno'] = node.compositeSensor.read()['Izmjereno']
			if self.informationKey in node.memory:
				node.memory['MaxTemp'] = node.memory['Izmjereno']
				if (brojac % pom_var == 0):
					node.status = 'INITIATOR'
					ini_nodes.append(node)
			brojac += 1
		for ini_node in ini_nodes:
			self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI, destination=ini_node))

	def initiator(self, node, message):
		if message.header == NodeAlgorithm.INI:
			node.send(Message(header='Information', data=node.memory[self.informationKey]))
			node.status = 'IDLE'

	def idle(self, node, message):
		if message.header == 'Information':
			if (message.data > node.memory['MaxTemp']):
				node.memory['MaxTemp'] = message.data
				destination_nodes = list(node.memory[self.neighborsKey])
				destination_nodes.remove(message.source)
				#print (destination_nodes)
				if destination_nodes:
					node.send(Message(destination=destination_nodes, header='Information', data=message.data))
			elif (node.memory['MaxTemp'] > message.data):
				destination_nodes = list(node.memory[self.neighborsKey])
				if destination_nodes:
					node.send(Message(destination=destination_nodes, header='Information', data=node.memory['MaxTemp']))

	STATUS = {
            'INITIATOR': initiator,
            'IDLE': idle,
            }





