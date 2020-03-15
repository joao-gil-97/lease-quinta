import argparse
import requests
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


from requests.exceptions import HTTPError

IP_PORT='http://192.168.2.6:80'
ACTION_ACQUIRE_LEASE='tryAcquireLease'
ACTION_HISTORY='history'
ACTION_CHECK_LEASE='checkLease'
ACTION_REMOVE_LEASE='removeLease'

scheduler = BackgroundScheduler()
scheduler.start()

def heart_beat(request):
	response = requests.post(f'{IP_PORT}/{action}', json=request)
	response.raise_for_status()
	print(response.text)
		
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('user', action='store',
						help='The user who will acquire the lease')

	parser.add_argument( '-a', action='store',
						required=True,
						dest='action',
						choices=[ACTION_ACQUIRE_LEASE, ACTION_HISTORY, ACTION_CHECK_LEASE,ACTION_REMOVE_LEASE],
						help='Type of action the user wants to perform')
	parser.add_argument( '-k', action='store_true',
						default=False,
						dest='keep_acquiring',
						help='Refresh the lease when it expires')
	parser.add_argument( '-d', action='store_true',
						default=False,
						dest='debug',
						help='Debug Mode')


	args = parser.parse_args()

	user = args.user
	action = args.action
	keep_acquiring = args.keep_acquiring
	is_debug = args.debug
	try:
		if action == ACTION_ACQUIRE_LEASE:
			if is_debug:
				duration = '0:1'
				params_json={'machines':['s1','s2'], 'time':duration, 'notes':'Notas', 'owner':'jojo'}
			else:
				print('Insert a comma separated list of machines that you want to set the lease')
				machines = input().split(',')
				print('Insert the amount of time that your lease will last\nEx: 1:0 for 1h 00m lease, 0:10 for 0h 10m lease')
				duration = input().strip()
				print('Insert a text note that will summarize the lease')
				notes = input().strip()
				params_json={'machines':machines, 'time':duration, 'notes':notes, 'owner':user}

			response = requests.post(f'{IP_PORT}/{action}', json=params_json)
			response.raise_for_status()
			if keep_acquiring:
				print(response.text)
				h, m = duration.split(':')
				params_json['time'] = '24:0'
				acquire_lease_seconds = datetime.now() + timedelta(hours=int(h), minutes=int(m)) - timedelta(seconds=5)
				scheduler.add_job(heart_beat, 'date', [params_json], run_date=acquire_lease_seconds)
				while True:
					time.sleep(60)
		else:
			response = requests.get(f'{IP_PORT}/{action}')
	
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
	except (KeyboardInterrupt, SystemExit):
		requests.get(f'{IP_PORT}/removeLease')
		scheduler.shutdown()
	except Exception as err:
		print(f'Other error occurred: {err}')
	else:
		print(response.text)
		print('Success!')
