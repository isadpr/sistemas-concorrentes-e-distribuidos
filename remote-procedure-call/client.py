import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print("2 + 3 =", proxy.add(2, 3))
print("7 - 5 =", proxy.subtract(7, 5))
print("4 * 6 =", proxy.multiply(4, 6))
print("8 / 2 =", proxy.divide(8, 2))
print("5 / 0 =", proxy.divide(5, 0))