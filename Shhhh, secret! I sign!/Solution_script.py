import random
import binascii
import binhex
"""
Тест Миллера-Рабина на простоту для проверки больших чисел на простоту. Параметры p и q.
"""
def  Miller_Rabin_test(n):
	s = 0
	x = n - 1
	while x % 2 != 1:
		s = s + 1#Вычисляем параметр s
		x = x // 2
	r = (n - 1) // (2 ** s)#Вычисляем параметр r
	b = []#Создаем лист для хранения последовательности b-элементов
	for i in range(0, 2):#повторяем t раз
		f = random.randint(2,n-2)#Выбираем число a из заданного промежутка
		b.append(pow(f,r,n))#Вычисляем 0 элемент последовательности
		for j in range(1, s+1):
			b.append(pow(b[j-1], 2, n))
		tst = False

		for m in range (0, s):
			if b[m] == 1:
				if b[m-1] != (n-1) and m !=0:
					return (0)
		if b[s] != 1:
			return (0)
	return (n)

def GenerateKey(p, g, y,k):
	flag = False
	while(flag == False):
		p = random.getrandbits(64)
		if (Miller_Rabin_test(p) == p):
			flag = True
	g = random.randint(1, p-1)
	k = random.randint(1, p-1)
	y = pow(g,k,p)
	return p,g,y,k


def Signature(msecret, mopen, k, p, g):
	a = pow(g, msecret, p)
	b = ((mopen - k*a)//msecret)%p
	return(a,b)

def egcd(cipher, modulo):
	if cipher == 0:
		return (modulo, 0, 1)
	else:
		g, x, y = egcd(modulo % cipher, cipher)
		return (g, y - (modulo // cipher) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(cipher, modulo):
	if (cipher < 0):
		cipher = cipher + modulo
	g, x, _ = egcd(cipher, modulo)
	if g == 1:
		return x % modulo
	else:
		return 0

"""  Параметры открытого и секретного ключа  """
p = 9973171988044726919
g = 0
y = 0
k = 9844832249766286560
a = 6397188859273851158
b = 8226101400993076321
mopen = 418547722601
"""                                          """
msecret = int(binascii.hexlify(("ClapC/").encode()), 16) #взаимно просто с р-1, секретное значение(флаг)
#mopen = int(binascii.hexlify((input("Your message for signature: ")).encode()), 16)#открытое сообщение
print("Flag: ", msecret)
#print("Message: ", mopen)
"""
for i in range (0,100):
	p,g,y,k = GenerateKey(p,g,y,k)
	print("Key: ", p,g,y,k)
	msecret1 = mulinv(msecret, p-1)
	#tmsecret = mulinv(msecret, p)
	#tmopen = mulinv(mopen, p)
	print("msecret1=",msecret1)

	#if (msecret1 != 0 and tmsecret!=0 and tmopen != 0): break
	a = pow(g, msecret, p)
	b = ((mopen - k*a)*msecret1)%(p-1)
	print("Signature: ",a,b)
	#(a,b) - signature

	b1 = mulinv(b, p-1)
	print("b1", b1)
	flag = (b1 * (mopen - k*a))%(p-1)
	print("Flag! : ", flag)
	print("i=", i)
	if(flag!=0 and flag==msecret): break
"""

b1 = mulinv(b, p-1)
print("b1", b1)
flag = (b1 * (mopen - k*a))%(p-1)
print("Flag! : ", hex(flag))
print(hex(p))