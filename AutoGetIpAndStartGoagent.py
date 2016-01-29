 # -*- coding: gbk -*-       <--------------����gbk
import io,sys,os,urllib2,shutil,time
# ȫ�ֱ���
# �Ա��Ľӿ��Ƕ�̬��ҳ�����������󣬸���chinaz
#GET_ISP_TYPE_URL = 'http://ip.taobao.com/ipSearch.php'
#GET_ISP_TYPE_URL = 'http://ip.chinaz.com/'
GET_ISP_TYPE_URL = 'http://ip.chinaz.com/getip.aspx'
ISP_TYPE_DIANXIN = '����'
IPS_TYPE_TIETONG = '��ͨ'
# ���ſ���ip�ļ�
GITHUB_DIANXIN_RAW_FILE = 'https://raw.githubusercontent.com/out0fmemory/GoAgent-Always-Available/master/%E7%94%B5%E4%BF%A1%E5%AE%BD%E5%B8%A6%E9%AB%98%E7%A8%B3%E5%AE%9A%E6%80%A7Ip.txt'
BACKUP_SITE_DIANXIN_RAW_FILE = 'http://yanke.info/ip/dianxin_ip.txt'

# ��ͨ����ip�ļ�
GITHUB_TIETONG_RAW_FILE = 'https://raw.githubusercontent.com/out0fmemory/GoAgent-Always-Available/master/%E9%93%81%E9%80%9A%E5%AE%BD%E5%B8%A6%E9%AB%98%E7%A8%B3%E5%AE%9A%E6%80%A7Ip.txt'
BACKUP_SITE_TIETONG_RAW_FILE = 'http://yanke.info/ip/tietong_ip.txt'

# �����������Դ���
NET_RETRY_CNT = 3
PROXY_PROP = 'proxy.ini'
PROXY_PROP_BACKUP = 'proxy.bak'
PROXY_PROP_TEM = 'proxy.tem'
GOOGLE_CN_TAG = '[google_cn]'
GOOGLE_HK_TAG = '[google_hk]'
HOSTS_TAG = 'hosts = '
SEPIRATOR_TAG = '.'
GOAGENT_EXE_FILE = 'goagent.exe'
	
# ��ȡ��Ӫ������	
def getIpType():
	try:
		getIpurl = GET_ISP_TYPE_URL
		fd = urllib2.urlopen(getIpurl)
		Ipdata = fd.read()
		Ipdata = Ipdata.decode('utf-8').encode('gbk')
		ispType = ISP_TYPE_DIANXIN
		if IPS_TYPE_TIETONG in Ipdata:
			print "��Ӫ��Ϊ" + IPS_TYPE_TIETONG
			ispType = IPS_TYPE_TIETONG
		elif ISP_TYPE_DIANXIN in Ipdata:
			print "��Ӫ��Ϊ" + ISP_TYPE_DIANXIN
		else :
			print "��Ӫ��Ϊ������Ĭ��ʹ�õ���"
		return ispType
	except Exception, e:
		return None

# ��ȡgithub�Ͽ���ip��ַ	
def getAvailableGoagentIp(ispType):
	try:
		# ����github�ϵ�ip��ַ�ļ�
		print "����github�ϵĿ���ip"
		url = GITHUB_DIANXIN_RAW_FILE
		if ispType == IPS_TYPE_TIETONG:
			url = GITHUB_TIETONG_RAW_FILE
		fd = urllib2.urlopen(url,timeout=5)
		content = fd.read()
		print '����ip�б�' + content
		return content
	except Exception, e:
		return None

def getAvailableGoagentIpWithBackupSite(ispType):
	try:
		# ����yanke.info�ϵ�ip��ַ�ļ�
		print "����yanke.info�ϵĿ���ip"
		url = BACKUP_SITE_DIANXIN_RAW_FILE
		if ispType == IPS_TYPE_TIETONG:
			url = BACKUP_SITE_TIETONG_RAW_FILE
		fd = urllib2.urlopen(url,timeout=10)
		content = fd.read()
		print '����ip�б�' + content
		return content
	except Exception, e:
		return None


def localFileReplace(ipList):
	# �ȱ��������ļ�
	shutil.copy(PROXY_PROP, PROXY_PROP_BACKUP)
	# ���Ҳ��滻�����ļ�
	isInHostCn = 0
	isInHostHk = 0
	inFile = open(PROXY_PROP,"r")
	out = open(PROXY_PROP_TEM,"w")
	line = inFile.readline()
	while line:
		#print line
		if line.find(GOOGLE_CN_TAG) != -1:
			isInHostCn = 1
		elif line.find(GOOGLE_HK_TAG) != -1:
			isInHostHk = 1
		if isInHostCn == 1:
			if HOSTS_TAG in line and SEPIRATOR_TAG in line:
				print "�滻ǰ " + GOOGLE_CN_TAG + line
				isInHostCn = 0
				line = HOSTS_TAG + ipList + '\n'
		elif isInHostHk == 1:
			if HOSTS_TAG in line and SEPIRATOR_TAG in line:
				print "�滻ǰ " + GOOGLE_HK_TAG + line
				isInHostHk = 0
				line = HOSTS_TAG  + ipList + '\n'
		out.write(line)
		line = inFile.readline()
	inFile.close()
	out.flush()
	out.close()
	shutil.copy(PROXY_PROP_TEM, PROXY_PROP)	
# ͨ��gscan��ȡ����ip
def gscanIp():
	#os.chdir(exe_path)
	os.system('cd gscan && gscan.exe -iprange="./my.conf"')
	fp = open('gscan\google_ip.txt','r')
	content = fp.readline()
   	fp.close
   	return content
# ��ȡ�ļ��޸�ʱ��
def getFileModifyTime():
	t = time.ctime(os.path.getmtime("e:/MQDwO"))#time.ctime(os.stat("e:/MQDwO").st_mtime) #�ļ����޸�ʱ��
	print t
	return 
# ��ȡ��һ������ip
def getFirstStartUpIp():
	return getAvailableIp()
# ��ȡ�Ѿ�ɨ��õ��ϴ���github�Լ����÷�������ip�б�
def getAvailableIp():
	i = 0
	ispType = None
	while i < NET_RETRY_CNT and ispType == None:
		ispType = getIpType()
		i = i + 1
	if ispType == None:
		ispType = ISP_TYPE_DIANXIN
	i = 0
	ipList = None
	while i < NET_RETRY_CNT and ipList == None:
		ipList = getAvailableGoagentIp(ispType)
		if ipList == None:
			ipList = getAvailableGoagentIpWithBackupSite(ispType)
		i = i + 1
	if ipList == None:
		print '��ȡ����ipʧ��'
	return ipList
# �ܵ�	
def startGoagentWithIpAutoGet():
	i = 0
	ispType = None
	while i < NET_RETRY_CNT and ispType == None:
		ispType = getIpType()
		i = i + 1
	if ispType == None:
		ispType = ISP_TYPE_DIANXIN
	i = 0
	ipList = None
	while i < NET_RETRY_CNT and ipList == None:
		ipList = getAvailableGoagentIp(ispType)
		if ipList == None:
			ipList = getAvailableGoagentIpWithBackupSite(ispType)
		i = i + 1
	if ipList == None:
		print '��ȡ����ipʧ��'
		return
	#localFileReplace(ipList)
	getFileModifyTime()
	localetime = time.localtime()
	print localetime
	ips = gscanIp()
	print ips
	#����goagent
	os.startfile(GOAGENT_EXE_FILE)
if __name__=="__main__": 
	startGoagentWithIpAutoGet()