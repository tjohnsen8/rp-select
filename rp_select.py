


def get_activity_multiplier(description):
	if description == 'sedentary':
		return 1.1
	elif description == 'light':
		return 1.2
	elif description == 'moderate':
		return 1.35
	elif description == 'very':
		return 1.45
	elif description == 'extra':
		return 1.7
	else:
		return 1.1

def get_tdee_calories_katch(weight, bf_pct, activity):
	LBM = weight/2.2*(1-bf_pct)
	bmr = 370 + (21.6 * LBM) 
	return int(bmr * get_activity_multiplier(activity))

def get_tdee_calories_mifflin(weight, height, age, sex, activity):
	weight_kg = weight / 2.2
	height_cm = height * 2.54
	sex = sex.lower()[0]
	mifflin = 10*weight_kg + 6.25*height_cm - 5*age
	if sex == 'm':
		mifflin += 5
	elif sex == 'f':
		mifflin -= 151
	return int(mifflin * get_activity_multiplier(activity))


class Macro(object):
	def __init__(self, _cals, _grams=0, _type='None'):
		self.type = _type
		self.cals_per_gram = _cals
		self.grams =  _grams
		
	def calories(self):
		return self.cals_per_gram * self.grams

class Protein(Macro):
	def __init__(self):
		super().__init__(4, 0, 'lean animal')
	def __init__(self, _grams):
		super().__init__(4, _grams, 'lean animal')

class Carbohydrate(Macro):
	def __init__(self):
		super().__init__(4, 0, 'low glycemic')
	def __init__(self, _grams):
		super().__init__(4, _grams, 'low glycemic')

class Fat(Macro):
	def __init__(self):
		super().__init__(9, 0, 'peanut butter')	
	def __init__(self, _grams):
		super().__init__(9, _grams, 'low glycemic')

class Macros(object):
	def __init__(self):
		self.protein = Protein(0)
		self.carbs = Carbohydrate(0)
		self.fat = Fat(0)

	def get_totals(self):
		return 
		{
		'p': self.protein.calories(),
		'c': self.carbs.calories(),
		'f': self.fat.calories()	
		}

class Training(object):
	def __init__(self):
		self.type = 'none'
		self.time = 'morning'

	def __init__(self, _type, _time):
		self.type = _type
		self.time = _time

	def morning_training(self):
		self.time = 'morning'

	def evening_training(self):
		self.time = 'evening'

	def rest_day(self):
		self.type = 'none'

	def light_day(self):
		self.type = 'light'

	def moderate_day(self):
		self.type = 'moderate'

	def intense_day(self):
		self.type = 'intense'


class MealPlan(object):
	def __init__(self, num_meals=5):
		self.macros = Macros()
		self.training = Training()
		self.num_meals = num_meals
		self.weight = 0
		self.calories = 0
		self.meals = []

	def __init__(self, weight, calories, training_type, training_time, num_meals=5):
		self.training = Training(training_type, training_time)
		self.num_meals = num_meals
		self.calories = calories
		self.weight = weight
		self.macros = Macros()
		self.macros.protein = Protein(self.weight * 0.9)
		self.set_carbs_and_fat()

	def set_carbs_and_fat(self):
		if self.training.type == 'none':
			self.macros.carbs = Carbohydrate(self.weight * 0.5)
		elif self.training.type == 'light':
			self.macros.carbs= Carbohydrate(self.weight * 1)
		elif self.training.type == 'moderate':
			self.macros.carbs = Carbohydrate(self.weight * 1.5)
		elif self.training.type == 'intense':
			self.macros.carbs = Carbohydrate(self.weight * 2)
		fat_cals = self.calories - self.macros.protein.calories() - self.macros.carbs.calories()
		self.macros.fat.grams = fat_cals / self.macros.fat.cals_per_gram


class Template(object):
	def __init__(self):
		self.meal_plan = MealPlan()
		self.weight = 0
		self.caloric_balance = 'eucaloric'

	def __init__(self, params):
		self.weight = params['weight']
		self.calories_per_day = params['tdee']
		# set balance and cals per day
		if params['goal'] == 'cut':
			self.caloric_balance = 'hypocaloric'
			self.calories_per_day -= 250
		elif params['goal'] == 'bulk':
			self.caloric_balance = 'hypercaloric'
			self.calories_per_day += 250
		else:
			self.caloric_balance = 'eucaloric'
		self.meal_plan = MealPlan(self.weight, self.calories_per_day, params['workout'], params['time'])

	def set_goal(self, goal):
		if goal == 'cut':
			self.caloric_balance = 'hypocaloric'
		elif goal == 'bulk':
			self.caloric_balance = 'hypercaloric'
		else:
			self.caloric_balance = 'eucaloric'

	def print_meals(self):
		pass

	def print_macros(self):
		print(self.meal_plan.macros.protein.grams)
		print(self.meal_plan.macros.carbs.grams)
		print(self.meal_plan.macros.fat.grams)


if __name__ == "__main__":
	change = input('has your weight or bf pct changed? ').upper()
	if change == 'Y' or change == 'YES':
		print(get_tdee_calories_katch(185, .15, 'light'))
		print(get_tdee_calories_mifflin(185, 70, 32, 'male', 'light'))
		weight_lbs = int(input('enter weight in lbs '))
		af = input('enter activity factor <sedentary|light|moderate|very|extra> ')
		hasLbm = input('do you have your bf_pct? ')
		if hasLbm == 'y':
			bf_pct = float(input('enter bf_pct '))
			tdee = get_tdee_calories_katch(weight_lbs, bf_pct/100, af)
		else:
			height_in = int(input('enter height in inches '))
			age = int(input('enter age '))
			sex = input('enter sex ')
			tdee = get_tdee_calories_mifflin(weight_lbs, height_in, age, sex, af)
	else:
		tdee = int(input('what is your tdee '))
		weight_lbs = int(input('what is your weight in lbs '))

	print('{} at {}'.format(tdee, weight_lbs))

	goal = input('cut bulk or neither? ').lower()

	# using the calc or input tdee, select the calorie break down
	workout = input('are you working out today ').upper()
	time = ''
	if workout == 'Y' or workout == 'YES':
		time = input('when <morning|evening>').lower()
		workout = input('intensity? <light|moderate|intense>').lower()
	else:
		workout = 'none'

	# things we needs: 
	# weight, tdee, goal, workout, time
	params = {}
	params['tdee'] = tdee
	params['workout'] = workout
	params['time'] = time
	params['goal'] = goal
	params['weight'] = weight_lbs
	template = Template(params)
	template.print_macros()
