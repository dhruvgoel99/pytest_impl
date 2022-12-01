import unittest
import paramiko
import pytest
import datetime

output_file = 'vm_details.txt'
timestamp = str(datetime.datetime.now())

class TestSimpleWidget(unittest.TestCase):

    #setup will run first 
    def setUp(self):
    	self.out = None
    	self.ssh = paramiko.SSHClient()
    	self.ssh.load_system_host_keys()
    	self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	self.ssh.connect(hostname='192.168.234.129', username='dhruv', password='root', port=22)
        
    #test cases goes here with 'test' prefix
    # run this marked testcase: (pytest -v -m "cli")
    # other test cases: (pytest -v -m "not cli")
    @pytest.mark.cli
    def test_cpu_num(self):
    	## number of CPUs
    	stdin, stdout, stderr = self.ssh.exec_command('lscpu | grep -e ^CPU\(s\)')
    	out = stdout.readline().split()
    	self.assertEqual(out[-1],'2')
    	self.out = timestamp+' CPU_NUM: '+out[-1]+'\n'
    	
    def test_mem_avail(self):
    	## memory available: if  more than 50%
    	stdin, stdout, stderr = self.ssh.exec_command('free -m | grep Mem:')
    	out = stdout.readline().split()
    	self.assertGreaterEqual(out[-1],str(0.5*int(out[1])))
    	self.out = timestamp+' MEM_AVAIL: '+out[-1]+'\n'
    	
    def test_cpu_idle(self):
    	## CPU %idle: if more than 90%
    	stdin, stdout, stderr = self.ssh.exec_command('sudo apt install sysstat; mpstat | grep -e .[0-9]$')
    	out = stdout.readline().split()
    	self.assertGreaterEqual(float(out[-1]),90)
    	self.out = timestamp+' CPU_IDLE: '+out[-1]+'\n'
    	    	    
    #this will run after the test cases
    def tearDown(self):
    	with open(output_file, "a") as file:
    	    file.write(self.out)
    	file.close()
    	self.ssh.close()

if __name__ == '__main__':
    header = '===Test===\n'
    with open(output_file, "a") as file:
    	file.write(header)
    file.close()
    unittest.main()
