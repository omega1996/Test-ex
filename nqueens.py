import numpy as np
import random
from collections import Counter

class Solver_8_queens:

	board_width = 8
	
	def __init__(self, pop_size = 100, cross_prob=0.50, mut_prob=0.25):
		self.pop_size = pop_size
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob
		self.population=[]
		self.fit_func_popul=[0.1]
		fitness = []
	
	def solve(self, min_fitness=0.9, max_epochs=100):
		population = self.generate_population()
		fit_func_popul = self.fit_func(population)
		epoch_num = 0
		best_fit = max(self.fit_func_popul)
		max_index = self.fit_func_popul.index(best_fit)
		
		while best_fit<min_fitness and epoch_num<max_epochs:
		
			#выбор родителей
			parents = self.selection(self.fit_func_popul)
			#скрещивание
			new_population = self.crossingover(parents)	
			
			#мутируем
			mutated = self.mutation(new_population)
			
			#проверка функции
			fit_popul = fit_func(mutated)
			best_fit = max(fit_popul)
			max_index = fit_popul.index(best_fit)
			
			epoch_num = epoch_num + 1
			
		return best_fit, epoch_num, self.visualization(self.mutated[max_index])
	
	
	def visualization(self, osob):
		s = ''
		for i in range(self.board_width):
			for j in range(self.board_width):
				if osob[i] == j:
					s += 'Q'
				else:
					s += '+'
				s += ' '
			s += '\n'
		return s
	
	
	
	
	def generate_population(self):
		population = np.random.randint(0,self.board_width,(self.pop_size,self.board_width))
		return population
	
	def fit_func(self, population):
		fitness = []
		dop = []
		
		for osob in population:
  			vert = Counter(osob) #вертикаль
  			vert = sum(vert.values())-len(vert.values())
  			diaup = Counter (osob - np.arange(self.board_width))#диагональ вниз	
  			diaup = sum(diaup.values())-len(diaup.values())
  			diadown = Counter (osob + np.arange(self.board_width))#диагональ вверх
  			diadown = sum(diadown.values())-len(diadown.values())
  			fitness.append(1-(vert+diaup+diadown)/self.board_width*2)
			
		return fitness
		
	
	def selection(self,fitness):
		fitness_norm = []
		parents = []
		for i in fitness:
			i = i/sum(self.fit_func_popul)
			fitness_norm.append(i)
			
		randosob = np.random.choice(len(self.fit_func_popul),size = 50, replace=True, p=fitness_norm)
		for i in randosob:
			#parents.append(self.population[i])
			parents.append(i)
		return parents
	
	def crossingover(self,parents):
		new_population = []
		for i in range(0, len(parents)-1, 2):
			new_population.append(parents[i])
			new_population.append(parents[i+1])
			if random.random() <= self.cross_prob:
				crack = random.randint (1, self.board_width-1)
				parent_1=parents[i]
				parent_2=parents[i+1]
				child_1 = np.hstack((parent_1[0:crack],parent_2[crack:self.board_width]))
				child_2 = np.hstack((parent_2[0:crack],parent_1[crack:self.board_width]))
				new_population.append(child_1)
				new_population.append(child_2)
				
		return new_population
		
	def mutation(self,new_population):
		mutated = []
		for i in new_population:
			if random.random() <= self.mut_prob:
				mutagen = random.randint(0,self.board_width-1)
				mutated.append(i)
				i[mutagen] = random.randint(0,self.board_width-1)
		new_population = np.vstack((new_population, mutated))
		return new_population
				

