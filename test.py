"""
Author: FYWindIsland
Date: 2021-08-10 19:17:29
LastEditTime: 2021-08-12 18:55:51
LastEditors: FYWindIsland
Description: 
I'm writing SHIT codes
"""
import re

message = "[CQ:reply,id=-771042982]测试"
text = re.findall("](.*)", message)

print(text)
