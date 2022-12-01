import unittest
import paramiko
import pytest
import datetime

output_file = 'vm_details.txt'

class SimpleWidgetTestCase(unittest.TestCase):

    #setup will run first 
    def setUp(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect(hostname='192.168.234.129', username='dhruv', password='root')
        
    #test cases goes here with 'test' prefix
    # run this marked testcase: (pytest -v -m "cli")
    @pytest.mark.cli
    def test_cpu_num(self):
    	log_out = ''
    	
    	## number of CPUs
    	stdin, stdout, stderr = self.ssh.exec_command('lscpu | grep -e ^CPU\(s\)')
    	out = stdout.readline().split()
    	self.assertEqual(out[-1],'2')
    	
    	log_out = str(datetime.datetime.now()) + ' ' + out[-1]
    	
    	## memory available: if  more than 50%
    	stdin, stdout, stderr = self.ssh.exec_command('free -m | grep Mem:')
    	out = stdout.readline().split()
    	self.assertGreaterEqual(out[-1],str(0.5*int(out[1])))
    	
    	log_out += ' ' + out[-1]
    	
    	## CPU %idle: if more than 90%
    	stdin, stdout, stderr = self.ssh.exec_command('sudo apt install sysstat; mpstat | grep -e .[0-9]$')
    	out = stdout.readline().split()
    	self.assertGreaterEqual(float(out[-1]),90)
    	
    	log_out += ' ' + out[-1] + '\n'
    	
    	## writing the log: (Timestamp num_cpu mem_avail %idle)
    	with open(output_file, "a") as file:
    	    file.write(log_out)
    	    
    #this will run after the test cases
    def tearDown(self):
        self.ssh.close()

if __name__ == '__main__':
    unittest.main()
