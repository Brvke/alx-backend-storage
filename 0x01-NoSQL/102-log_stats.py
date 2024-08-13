#!/usr/bin/env python3
""" a script to find stats in logs.nginx collection """
from pymongo import MongoClient
from collections import Counter


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    col = client.logs.nginx

    print(f'{col.count_documents({})} logs')
    print('Methods:')
    print(f'\tmethod GET: {col.count_documents({"method": "GET"})}')
    print(f'\tmethod POST: {col.count_documents({"method": "POST"})}')
    print(f'\tmethod PUT: {col.count_documents({"method": "PUT"})}')
    print(f'\tmethod PATCH: {col.count_documents({"method": "PATCH"})}')
    print(f'\tmethod DELETE: {col.count_documents({"method": "DELETE"})}')
    print(f'{col.count_documents({"path": "/status"})} status check')

    ip_counts = Counter(doc['ip'] for doc in col.find({}, {'ip': 1}))
    top_ips = ip_counts.most_common(10)
    print('IPs:')
    for ip, count in top_ips:
        print(f'\t{ip}: {count}')

