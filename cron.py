from crontab import CronTab

script = '/home/pi/projects/light_switch/crontest'
cmt = 'cron_test'

def createJob():
	cron = CronTab()
	job = cron.new(command=script, comment=cmt)
	job.minute.every(1)
	cron.write()
	
def destroyJob():
	cron = CronTab()
	iter = cron.find_comment(cmt)
	try:
		job = iter.next()
		while len(job) > 0:
			cron.remove(job)
			job = iter.next()
	except StopIteration:
		pass
	cron.write()

if __name__ == '__main__':
	#createJob()
	destroyJob()
