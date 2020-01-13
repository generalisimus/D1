import requests  
import sys
  
auth_params = {    
    'key': "e7d55e563fdeca3f5065ab8d311d17f1",    
    'token': "06e853ead14353156cee10bed3a4b39a04459fca9db907b27418d123f0ecc5dd", }  
  
base_url = "https://api.trello.com/1/{}"  
board_id = "5df135f087f9e5647f9abc87"

def create_column(column_name):
	return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()

def column_check(column_name):
	column_id = None
	column_data = requests.get(base_url.format('boards') + "/" + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		if column['name'] == column_name:
			column_id = column['id']
			return column_id

def read():
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

	for column in column_data:
		task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		print(column['name'] + " " + str(len(task_data)))
		
		if not task_data:
			print('\t' + 'Нет задач!')
			continue
		for task in task_data:
			print('\t' + task['name'])

def create(name, column_name):
	column_id = column_check(column_name)
	if column_id is None:
		column_id = create_column(column_name)["id"]
	requests.post(base_url.format('cards'), data={"name": name, 'idList': column_id, **auth_params})

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    for column in column_data:    
        if column['name'] == column_name:    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		read()
	elif sys.argv[1] == 'create':
		create(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == 'create_column':
		create_column(sys.argv[2])
	elif sys.argv[1] == 'move':
		move(sys.argv[2], sys.argv[3])
