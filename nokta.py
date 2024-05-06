class Nokta:
	def __init__(self, x=0, y=0):
		self.x=x
		self.y=y

	def str(self):
		return str(self.x)+","+str(self.y)

	def __eq__(self, x2):
		return (self.x == x2.x and self.y == x2.y)
		
	def __neq__(self, x2):
		return not (self.x == x2.x and self.y == x2.y)
