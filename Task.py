class Task:
	def __init__(self, name, goalDate, startDate=None, endDate=None, state=0):
		self.name = name
		self.startDate = startDate
		self.endDate = endDate
		self.goalDate = goalDate
		self.state = state

	def __str__(self):

		match self.state:
			case 0: state = 'To do'
			case 1: state = 'Running...'
			case 2: state = 'Finished'

		txt = "Name : " + self.name
		txt += "\nGoal : " + str(self.goalDate) if self.goalDate is not None else "\nGoal : No time limit"
		txt += "\nStart : " + str(self.startDate) if self.startDate is not None else "\nStart : Task not started"
		txt += "\nEnd : " + str(self.endDate) if self.endDate is not None and self.startDate is None else "\nEnd : Task still running"
		txt += "\nState : " + state

		return txt
