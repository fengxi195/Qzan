import requests as req
import threading,queue,time,re

class Qzan(object):
	def __init__(self):
		self.start_time = time.time()
		self.QQ_queue = queue.Queue()
		with open('账号.txt','r') as f:
			self.zhanghao = f.readlines()
		with open('接口.txt', 'r') as f:
			self.jk_url = set(f.readlines())
		self.header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
		}
	def __del__(self):
		end_time = time.time()
		print('经过了{}分钟，终于执行完了'.format(float((end_time - self.start_time) / 60)))

	def main(self):
		while not self.QQ_queue.empty():
			zh = str(self.QQ_queue.get())
			self.QQ_queue.task_done()
			for x in self.jk_url:
				url = x.replace('\n', '').replace(' ','') + zh
				print('当前存活线程数：', threading.active_count())
				try:
					dj = req.get(url, timeout=8,headers=self.header)
				except Exception as e:
					print('请求超时')
				else:
					dj.encoding = 'utf-8'
					# print(dj.text.replace('\n', ''))
					print(dj.url)
					if re.findall('!DOCTYPE',dj.text):
						print("下单失败")
					else:
						print(dj.text.replace('\n',''))
						# print("下单成功")
	def run(self):
		thread_list = []
		QQ_list = self.zhanghao[0].split(',')
		for x in QQ_list:
			self.QQ_queue.put(x)
			data = threading.Thread(target=self.main)
			thread_list.append(data)
		for d in thread_list:
			d.setDaemon(False)
			d.start()
		for d in thread_list:
			d.join()

if __name__ == '__main__':
	qz = Qzan()
	qz.run()