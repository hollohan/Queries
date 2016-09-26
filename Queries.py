import pymysql.cursors

class Queries():
	def __init__(self, db, host='localhost', user='root', password='toor'):
		self.conn = pymysql.connect(
			host = 'localhost',
			user = 'root',
			password = 'toor',
			db = db)        
		self.cursor = self.conn.cursor()

	def run_query(self, q_string):
		'''
			executes q_string in DB assigned to self
		'''
		conn = self.conn
		cursor = self.cursor
		cursor.execute(q_string)
		results = self.cursor.fetchall()
		conn.commit()

		return results
		
	def close(self): self.conn.close()
	
	def select(self, fields, frm, whr=0):
		'''
			executes select query			
			fields = fields to return, ['first','last','etc',...] 
			frm = table to select from 'tableA'
			whr = criteria {'id':25,'username':'hollohae'}
			! does not accept *, all field names must be chosen explicitly
			
		'''
		q_string = 'SELECT '
		# add fields to q_string
		fields_str = ','.join(fields) # format list into comma seperated string
		q_string += fields_str + ' '
		
		# add table to q_string
		q_string += 'FROM ' + frm
		
		# add criteria to q_string
		if whr:
			criteria = []
			for c in whr:
				if type(whr[c]) is int: # check if into for correct SQL formatting
					criteria.append('%s=%s' % (c, whr[c]))
				else: # if not int is string
					criteria.append('%s="%s"'  % (c, whr[c]))
			criteria = ' AND '.join(criteria)
			q_string += ' WHERE ' + criteria
		
		print '[executing] ' + q_string
		results = self.run_query(q_string)
		results = self.objectize(results, fields)
		return results

	def objectize(self, results, fields):
		'''
			results = tuples, output from run_query
			fields = list, fields tha were queries in run_query
			returns {field:result,field:result,...} for each thing in results
		'''
		newResults = []
		for result in results:
			newObj = {}
			for i in range(len(fields)):
				newObj[fields[i]] = result[i]
			newResults.append(newObj)
				
		return newResults
		
	def insert(self, table, values):
		'''
			executes insert into statement
			table = str, table to insert into
			valus = obj, fields and values to inser, {'first':'eric','last':'hollohan'}
		'''
		q_string = 'INSERT INTO  '
		
		# add table to q_string
		q_string += table + ' '

		# add fields and values
		f = [x for x in values] # puts all fields into one list
		v = [str(values[x]) if type(values[x]) is int else '"%s"' % values[x] for x in values] # puts all values into one list
		f = ','.join(f)
		v = ','.join(v)
		q_string += '(%s) VALUES (%s)' % (f, v)
		
		print '[executing] ' + q_string
		self.run_query(q_string)
	
	def update(self, table, values, whr=0):	
		'''
			updates table with values where criteria
			table = str, table to update
			values = {field:value}, fields/values to update
			whr = {field:val}, match criteria, where ...
		'''
		q_string = 'UPDATE '
		
		# add table
		q_string += table + ' '
		
		# add values
		q_string += 'SET '
		values = ['%s=%i' % (x, values[x]) if type(values[x]) is int else '%s="%s"' % (x, values[x]) for x in values]
		q_string += ','.join(values)
		
		# add criteria
		if whr:
			criteria = []
			for c in whr:
				if type(whr[c]) is int: # check if into for correct SQL formatting
					criteria.append('%s=%s' % (c, whr[c]))
				else: # if not int is string
					criteria.append('%s="%s"'  % (c, whr[c]))
			criteria = ' AND '.join(criteria)
			q_string += ' WHERE ' + criteria
		
		print '[executing] ' + q_string
		self.run_query(q_string)
			
if __name__=='__main__':
	q = Queries('testDB')
	q.update('tableB',{'first':'macers','last':'kitters'},{'num':12345})
	q.close()
